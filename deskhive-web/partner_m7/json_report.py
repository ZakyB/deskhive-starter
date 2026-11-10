"""Lab 2 — Export actual monthly DeskHive booking usage as JSON text."""

def export_usage_report(month: str) -> str:
    """Return a JSON string for YYYY-MM in Europe/Paris timezone.

    Shape: {month, total_bookings, spaces: [{code, city, bookings, hours}]}
    Include only spaces with bookings starting in the requested month.
    Hours are decimal strings with 2 fractional digits. Sort rows by code.
    No database writes; invalid month raises ValueError.
    """
    # TODO M7-LAB2: query bookings, aggregate hours and serialize with json.
    raise NotImplementedError('M7 Lab 2: export_usage_report')
