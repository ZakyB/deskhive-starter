"""Lab 1 — Complete the XML-RPC partner availability functions."""
from bookings.services import is_available
from spaces.models import Space
from bookings.intervals import local_interval
from deskhive_core.booking import validate_booking

def list_available_spaces(start_iso: str, end_iso: str) -> list[dict]:
    """Return available spaces as XML-RPC-safe dictionaries.

    Output fields: code, name, city, kind, hourly_rate (decimal as str).
    Dates must be offset-aware ISO-8601 strings; validate using the existing
    DeskHive interval rules. No writes. Invalid input raises ValueError.
    """
    # TODO M7-LAB1: parse/validate the dates and query actual available spaces.
    raise NotImplementedError('M7 Lab 1: list_available_spaces')

def get_space_availability(code: str, start_iso: str, end_iso: str) -> bool:
    """Return availability for an existing Space.code and interval.

    Unknown codes / invalid date ranges raise ValueError.
    """
    # TODO M7-LAB1: find the space by code and reuse availability rules.
    raise NotImplementedError('M7 Lab 1: get_space_availability')
