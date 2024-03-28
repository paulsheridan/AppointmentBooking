import calendar

from datetime import date, datetime, timedelta
from collections import namedtuple
from typing import Optional, List
from pydantic import BaseModel

from service import get_service, Service
from appointment import list_appointments, Appointment


Range = namedtuple("Range", ["start", "end"])


class Window(BaseModel):
    start: datetime
    end: datetime


class Availability(BaseModel):
    date: datetime
    windows: Optional[List[Window]]


def get_availability(
    user_id: str, service_id: str, month: Optional[int] = None
) -> list:
    available_times: list = []

    service: Service = get_service(user_id, service_id)
    earliest, latest = determine_date_range(service, month)
    appointments: list[Appointment] = list_appointments(user_id, earliest, latest)

    cal = calendar.Calendar()
    for day in cal.itermonthdates(earliest.year, earliest.month):
        if day < earliest or day > latest:
            continue
        # TODO: Is there a way to make this a pointer again? That would limit the time complexity
        today_appointments = [appt for appt in appointments if appt.start.date() == day]
        today_slots = calc_day_availability(service, today_appointments, day)

        if len(today_slots["windows"]) > 0:
            available_times.append(today_slots)

    return available_times


def calc_day_availability(service: Service, appointments: list[Appointment], day: date):
    office_hours = service.get_daily_schedule(day.weekday())
    today_slots: dict = {"date": day, "windows": []}
    if not office_hours:
        return today_slots

    appt_index = 0
    window_start = datetime.combine(day, office_hours.open)
    window_end = (
        window_start + timedelta(minutes=service.duration) - timedelta(minutes=1)
    )

    while window_end < datetime.combine(day, office_hours.close):
        if not appointments or appt_index >= len(appointments):
            today_slots["windows"].append({"start": window_start, "end": window_end})
            window_start = window_end + timedelta(minutes=1)
            # TODO: DRY this out
            window_end = (
                window_start
                + timedelta(minutes=service.duration)
                - timedelta(minutes=1)
            )
        else:
            r1 = Range(
                start=window_start,
                end=window_end,
            )
            r2 = Range(
                start=appointments[appt_index].start,
                end=appointments[appt_index].end,
            )
            if r1.end < r2.start:
                today_slots["windows"].append(
                    {"start": window_start, "end": window_end}
                )
                window_start = window_end + timedelta(minutes=1)
            elif r2.end < r1.start:
                today_slots["windows"].append(
                    {"start": window_start, "end": window_end}
                )
                window_start = window_end + timedelta(minutes=1)
                appt_index += 1
            else:
                window_start = r2.end + timedelta(minutes=1)
                appt_index += 1
            window_end = (
                window_start
                + timedelta(minutes=service.duration)
                - timedelta(minutes=1)
            )
    return today_slots


def determine_date_range(
    service: Service, month: Optional[str] = None
) -> tuple[str, str]:
    earliest: date = max(date.today(), service.start.date())
    if not month:
        latest: date = min(
            date(
                earliest.year,
                earliest.month,
                calendar.monthrange(earliest.year, earliest.month)[-1],
            ),
            service.end.date(),
        )
        return earliest, latest

    year, month = map(int, month.split("-"))
    if (
        month < earliest.month
        or year < earliest.year
        or month > service.end.month
        or year > service.end.year
    ):
        raise IndexError
    earliest = max(earliest, date(year, month, 1))
    latest = min(
        date(year, month, calendar.monthrange(year, month)[-1]), service.end.date()
    )
    return earliest, latest
