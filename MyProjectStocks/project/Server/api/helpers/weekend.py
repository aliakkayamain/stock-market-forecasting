from datetime import  timedelta

def is_weekend(date):
    """Tarihin hafta sonu olup olmadığını kontrol eder."""
    return date.weekday() >= 5  # Cumartesi (5) veya Pazar (6)

def get_previous_business_day(date):
    """Bir önceki iş gününü döner (hafta sonu günlerini atlayarak)."""
    while is_weekend(date):
        date -= timedelta(days=1)
    return date

def get_next_business_day(date):
    """Bir sonraki iş gününü döner (hafta sonu günlerini atlayarak)."""
    date += timedelta(days=1)
    while is_weekend(date):
        date += timedelta(days=1)
    return date