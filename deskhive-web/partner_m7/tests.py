"""M7 acceptance tests: independent of student implementations."""
import json
from datetime import datetime
from decimal import Decimal
from xmlrpc.client import dumps, loads, Fault
from django.test import TestCase
from django.utils import timezone
from zoneinfo import ZoneInfo
from spaces.models import Space
from bookings.models import Booking, Member
from bookings.services import save_booking
from .xml_import import import_corporate_contacts
from .json_report import export_usage_report

TZ = ZoneInfo('Europe/Paris')
START = '2030-01-15T10:00:00+01:00'
END = '2030-01-15T11:00:00+01:00'

class PartnerXmlRpcTests(TestCase):
    def rpc(self, method, *args):
        response = self.client.post('/rpc/availability/',
            data=dumps(args, methodname=method, allow_none=False).encode('utf-8'),
            content_type='text/xml')
        self.assertEqual(response.status_code, 200, response.content)
        params, _ = loads(response.content)
        return params[0]

    def test_partner_lists_available_spaces_from_real_catalogue(self):
        result = self.rpc('list_available_spaces', START, END)
        self.assertIsInstance(result, list)
        codes = {row['code'] for row in result}
        self.assertIn('lyo-desk', codes)
        desk = next(row for row in result if row['code'] == 'lyo-desk')
        self.assertEqual(desk['city'], 'Lyon')
        self.assertEqual(desk['hourly_rate'], str(Space.objects.get(code='lyo-desk').hourly_rate))

    def test_partner_reflects_bookings_and_returns_boolean(self):
        s = Space.objects.get(code='lyo-desk')
        self.assertTrue(self.rpc('get_space_availability', 'lyo-desk', START, END))
        save_booking(space=s, full_name='Test', email='test@example.test',
            start=datetime.fromisoformat(START), end=datetime.fromisoformat(END))
        self.assertFalse(self.rpc('get_space_availability', 'lyo-desk', START, END))
        codes = {row['code'] for row in self.rpc('list_available_spaces', START, END)}
        self.assertNotIn('lyo-desk', codes)

    def test_partner_rejects_invalid_input_without_state_change(self):
        before = Booking.objects.count()
        with self.assertRaises(Fault):
            self.rpc('get_space_availability', 'unknown-space', START, END)
        with self.assertRaises(Fault):
            self.rpc('list_available_spaces', 'not-a-datetime', END)
        self.assertEqual(Booking.objects.count(), before)

class CorporateImportExportTests(TestCase):
    GOOD = b'<corporate_contacts><contact><full_name>Test User</full_name><email>TEST@example.test</email></contact></corporate_contacts>'

    def test_import_contacts_into_existing_member_model(self):
        count = import_corporate_contacts(self.GOOD)
        self.assertEqual(count, 1)
        self.assertEqual(Member.objects.get().email, 'test@example.test')
        self.assertEqual(import_corporate_contacts(self.GOOD), 0)
        self.assertEqual(Member.objects.count(), 1)

    def test_invalid_xml_is_atomic_and_cannot_expand_entities(self):
        before = Member.objects.count()
        for payload in [
            b'<corporate_contacts><contact><full_name>A</full_name></contact></corporate_contacts>',
            b'<corporate_contacts><contact><full_name>A</full_name><email>a@example.test</email></contact><contact><full_name>B</full_name><email>invalid</email></contact></corporate_contacts>',
            b'<!DOCTYPE doc [<!ENTITY x SYSTEM "file:///etc/passwd">]><corporate_contacts>&x;</corporate_contacts>',
        ]:
            with self.subTest(payload=payload[:40]):
                with self.assertRaises(ValueError):
                    import_corporate_contacts(payload)
                self.assertEqual(Member.objects.count(), before)

    def test_usage_report_is_valid_json_and_reflects_actual_bookings(self):
        s = Space.objects.get(code='lyo-desk')
        save_booking(space=s, full_name='Usage Tester', email='usage@example.test',
            start=datetime.fromisoformat(START), end=datetime.fromisoformat(END))
        raw = export_usage_report('2030-01')
        report = json.loads(raw)
        self.assertEqual(report['month'], '2030-01')
        self.assertEqual(report['total_bookings'], 1)
        row = next(r for r in report['spaces'] if r['code'] == 'lyo-desk')
        self.assertEqual(row['bookings'], 1)
        self.assertEqual(Decimal(row['hours']), Decimal('1.00'))
        self.assertEqual(row['city'], 'Lyon')
        self.assertEqual(json.loads(export_usage_report('2030-02'))['total_bookings'], 0)

    def test_usage_report_rejects_bad_month(self):
        for bad in ['2030-13', '2030-1', 'oops']:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                export_usage_report(bad)
