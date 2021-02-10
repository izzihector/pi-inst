# -*- coding: utf-8 -*-

from odoo.fields import datetime
from datetime import timedelta
import pytz

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def convert_timezone(from_tz, to_tz, dt):
    from_tz = pytz.timezone(from_tz).localize(
        datetime.strptime(dt, DATETIME_FORMAT))
    to_tz = from_tz.astimezone(pytz.timezone(to_tz))
    return datetime.strptime(to_tz.strftime(DATETIME_FORMAT), DATETIME_FORMAT)


def ks_get_date(ks_date_filter_selection, timezone):
    series = ks_date_filter_selection
    return eval("ks_date_series_" + series.split("_")[0])(series.split("_")[1],
                                                          timezone)


# Last Specific Days Ranges : 7, 30, 90, 365
def ks_date_series_l(ks_date_selection, tz):
    ks_date_data = {}
    date_filter_options = {
        'day': 0,
        'week': 7,
        'month': 30,
        'quarter': 90,
        'year': 365,
        'past': False,
        'future': False
    }
    if ks_date_selection == 'day':
        ks_date_data["selected_end_date"] = convert_timezone(tz, 'UTC', datetime.now().strftime("%Y-%m-%d 23:59:59"))
    else:
        ks_date_data["selected_end_date"] = convert_timezone(
            tz, 'UTC',
            (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 23:59:59"))
    ks_date_data["selected_start_date"] = convert_timezone(tz, 'UTC', (datetime.now() - timedelta(
        days=date_filter_options[ks_date_selection])).strftime("%Y-%m-%d 00:00:00"))
    return ks_date_data


# Current Date Ranges : Week, Month, Quarter, year
def ks_date_series_t(ks_date_selection, tz):
    return eval("ks_get_date_range_from_" + ks_date_selection)("current", tz)


# Previous Date Ranges : Week, Month, Quarter, year
def ks_date_series_ls(ks_date_selection, tz):
    return eval("ks_get_date_range_from_" + ks_date_selection)("previous", tz)


# Next Date Ranges : Day, Week, Month, Quarter, year
def ks_date_series_n(ks_date_selection, tz):
    return eval("ks_get_date_range_from_" + ks_date_selection)("next", tz)


def ks_get_date_range_from_day(date_state, tz):
    ks_date_data = {}

    date = datetime.now()

    if date_state == "previous":
        date = date - timedelta(days=1)
    elif date_state == "next":
        date = date + timedelta(days=1)

    ks_date_data["selected_start_date"] = convert_timezone(tz, 'UTC', datetime(date.year, date.month, date.day).strftime(DATETIME_FORMAT))
    ks_date_data["selected_end_date"] = convert_timezone(tz, 'UTC', (datetime(date.year, date.month, date.day) + timedelta(days=1, seconds=-1)).strftime(DATETIME_FORMAT))
    return ks_date_data


def ks_get_date_range_from_week(date_state, tz):
    ks_date_data = {}

    date = datetime.now()

    if date_state == "previous":
        date = date - timedelta(days=7)
    elif date_state == "next":
        date = date + timedelta(days=7)

    date_iso = date.isocalendar()
    year = date_iso[0]
    week_no = date_iso[1]

    ks_date_data["selected_start_date"] = convert_timezone(tz, 'UTC', datetime.strptime('%s-W%s-1' % (year, week_no - 1), "%Y-W%W-%w").strftime(DATETIME_FORMAT))
    ks_date_data["selected_end_date"] = ks_date_data["selected_start_date"] + timedelta(days=6, hours=23, minutes=59, seconds=59, milliseconds=59)
    return ks_date_data


def ks_get_date_range_from_month(date_state, tz):
    ks_date_data = {}

    date = datetime.now()
    year = date.year
    month = date.month

    if date_state == "previous":
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    elif date_state == "next":
        month += 1
        if month == 13:
            month = 1
            year += 1

    end_year = year
    end_month = month
    if month == 12:
        end_year += 1
        end_month = 1
    else:
        end_month += 1

    ks_date_data["selected_start_date"] = convert_timezone(tz, 'UTC', datetime(year, month, 1).strftime(DATETIME_FORMAT))
    ks_date_data["selected_end_date"] = convert_timezone(tz, 'UTC', (datetime(end_year, end_month, 1) - timedelta(seconds=1)).strftime(DATETIME_FORMAT))
    return ks_date_data


def ks_get_date_range_from_quarter(date_state, tz):
    ks_date_data = {}

    date = datetime.now()
    year = date.year
    quarter = int((date.month - 1) / 3) + 1

    if date_state == "previous":
        quarter -= 1
        if quarter == 0:
            quarter = 4
            year -= 1
    elif date_state == "next":
        quarter += 1
        if quarter == 5:
            quarter = 1
            year += 1

    ks_date_data["selected_start_date"] = convert_timezone(tz, 'UTC', datetime(year, 3 * quarter - 2, 1).strftime(DATETIME_FORMAT))

    month = 3 * quarter
    remaining = int(month / 12)
    ks_date_data["selected_end_date"] = convert_timezone(tz, 'UTC', (datetime(year + remaining, month % 12 + 1, 1) - timedelta(seconds=1)).strftime(DATETIME_FORMAT))

    return ks_date_data


def ks_get_date_range_from_year(date_state, tz):
    ks_date_data = {}

    date = datetime.now()
    year = date.year

    if date_state == "previous":
        year -= 1
    elif date_state == "next":
        year += 1

    ks_date_data["selected_start_date"] = convert_timezone(tz, 'UTC', datetime(year, 1, 1).strftime(DATETIME_FORMAT))
    ks_date_data["selected_end_date"] = convert_timezone(tz, 'UTC', (datetime(year + 1, 1, 1) - timedelta(seconds=1)).strftime(DATETIME_FORMAT))

    return ks_date_data


def ks_get_date_range_from_past(date_state, tz):
    ks_date_data = {}

    date = datetime.now()

    ks_date_data["selected_start_date"] = False
    ks_date_data["selected_end_date"] = date
    return ks_date_data


def ks_get_date_range_from_pastwithout(date_state, tz):
    ks_date_data = {}
    date = (datetime.now() - timedelta(days=1)).replace(hour=23, minute=59, second=59)
    ks_date_data["selected_start_date"] = False
    ks_date_data["selected_end_date"] = convert_timezone(tz, 'UTC', date.strftime(DATETIME_FORMAT))
    return ks_date_data


def ks_get_date_range_from_future(date_state, tz):
    ks_date_data = {}

    date = datetime.now()

    ks_date_data["selected_start_date"] = date
    ks_date_data["selected_end_date"] = False
    return ks_date_data


def ks_get_date_range_from_futurestarting(date_state, tz):
    ks_date_data = {}
    date = (datetime.now() + timedelta(days=1)).replace(hour=00, minute=00, second=00)
    ks_date_data["selected_start_date"] = convert_timezone(tz, 'UTC', date.strftime(DATETIME_FORMAT))
    ks_date_data["selected_end_date"] = False
    return ks_date_data
