import calendar
from datetime import datetime

from data.models.feature import Feature


def get_max_days(year: int, month: int) -> int:
    """
    Returns the maximum number of days in a given month and year.

    Parameters:
    - year: The year (e.g., 2024)
    - month: The month (1 = January, 2 = February, ..., 12 = December)

    Returns:
    - The maximum number of days in the specified month
    """
    _, num_days = calendar.monthrange(year, month)
    return num_days


def get_year_month(feature: Feature) -> str:
    date_obj = datetime.strptime(feature.sample_date, '%Y-%m-%d %H:%M:%S')
    return date_obj.strftime('%Y-%m')
