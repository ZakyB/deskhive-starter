# DeskHive M7 — Parsing XML and JSON with Python

The `m7-xml-json` branch includes **fully corrected M6 and earlier modules**.
Do not redo M6. Continue from your existing fork of `deskhive-starter`.

## Lab 1 — Exposing DeskHive Availability to a Partner Agency via XML-RPC

Edit only `deskhive-web/partner_m7/xmlrpc_api.py`.
The URL `/rpc/availability/` and its XML-RPC dispatcher are already wired up.
Implement two read-only XML-RPC methods:

- `list_available_spaces(start_iso, end_iso)` returns a list of XML-RPC-safe
  dictionaries with `code`, `name`, `city`, `kind`, `hourly_rate` (price as string).
- `get_space_availability(code, start_iso, end_iso)` returns a Boolean.

Dates are offset-aware ISO-8601 values (for example `2030-01-15T10:00:00+01:00`).
Use the existing `Space` model, `bookings.services.is_available`,
`bookings.intervals.local_interval` and `deskhive_core.booking.validate_booking`.
Invalid intervals or unknown codes raise `ValueError` (the XML-RPC gateway
returns an XML-RPC Fault). No new database, mutations or new business rules.
The gateway is **classroom-only**, read-only, and not a production security design.

Endpoint: `POST /rpc/availability/` with `text/xml` XML-RPC content.
The HTTP status of an XML-RPC Fault is normally 200; the fault is in the XML body.
Check: `python check.py --m7-lab1`.

## Lab 2 — Importing Corporate Client Data in XML and Exporting Usage Reports in JSON

Edit only `deskhive-web/partner_m7/xml_import.py` and
`deskhive-web/partner_m7/json_report.py`.

- Implement `import_corporate_contacts(xml_bytes) -> int` using ElementTree for
  **small trusted local files**. The supplied fixture is at
  `deskhive-web/partner_m7/fixtures/corporate_contacts.xml`.
  Import contacts into the **existing** `bookings.Member` model; no new
  corporate-client model or migration. Required XML tags are
  `corporate_contacts/contact/full_name` and `corporate_contacts/contact/email`.
  Normalize email to lowercase; reject malformed XML, missing/invalid fields,
  duplicate emails inside one file, DTD/entity declarations. Make imports atomic,
  and avoid duplicating already existing members. Return count newly created.
- Implement `export_usage_report(month) -> str` with standard `json`.
  Accept `YYYY-MM`, use Europe/Paris for monthly boundaries, and count bookings
  **whose start** falls in the requested month. Return JSON with keys `month`,
  `total_bookings`, `spaces` (sorted by space code). Each space entry contains
  `code`, `city`, `bookings`, `hours` (decimal string, 2 digits after the dot).
  No database writes.

Check: `python check.py --m7-lab2`.
Run `python check.py --m7` for both labs, followed by `python check.py --all`
for regression checks. Execute from repository root with `.venv` Python.

## Setup

Use the `m7-xml-json` branch **from your own fork**, keeping prior work safe.
From the repository root on Windows, for example:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .\deskhive-core
.\.venv\Scripts\python.exe check.py --m6
.\.venv\Scripts\python.exe check.py --m7-lab1
```

For macOS/Linux, use `./.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.
M6 should already pass. M7 acceptance tests fail until the TODOs are completed.
Do not edit test files to make failures disappear.
