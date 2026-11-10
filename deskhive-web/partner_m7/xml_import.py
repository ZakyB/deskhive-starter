"""Lab 2 — Parse a trusted local corporate-contact XML file into Member."""
from bookings.models import Member

def import_corporate_contacts(xml_bytes: bytes) -> int:
    """Import contacts; return number of newly created Members.

    XML format: <corporate_contacts><contact><full_name>...</full_name>
    <email>...</email></contact>...</corporate_contacts>.
    Normalize email to lowercase. Existing emails are not duplicated.
    Reject bad XML, missing/invalid fields and duplicate emails in one file;
    do not partially import an invalid document. No schema/model migration.
    This classroom lab accepts small, locally trusted XML inputs only.
    """
    # TODO M7-LAB2: validate document, parse ElementTree and persist atomically.
    raise NotImplementedError('M7 Lab 2: import_corporate_contacts')
