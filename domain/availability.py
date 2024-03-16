import calendar

from datetime import date, time, datetime, timedelta
from collections import namedtuple

from service import get_service, Service
from appointment import list_appointments, Appointment

Range = namedtuple("Range", ["start", "end"])


def get_availability(user_id: str, service_id: str, month: int, year: int) -> list:
    service: Service = get_service(user_id, service_id)[0]

    # ensure all dates are in the future
    earliest: date = max(date.today(), service.start)
    if not month or not year:
        latest: date = min(
            date(
                earliest.year,
                earliest.month,
                calendar.monthrange(earliest.year, earliest.month)[-1],
            ),
            service.end,
        )
    else:
        if (
            month < earliest.month
            or year < earliest.year
            or month > service.end.month
            or year > service.end.year
        ):
            return []
        else:
            earliest = max(earliest, date(year, month, 1))
            latest = min(
                date(year, month, calendar.monthrange(year, month)[-1]), service.end
            )

    # if start was passed in and it is after
    appointments: list[Appointment] = list_appointments(user_id, earliest, latest)
    appt_pointer: int = 0
    available_times: list = []

    cal = calendar.Calendar()
    # get all days in a given month
    for day in cal.itermonthdates(earliest.month, earliest.year):
        # ignore dates in the past
        if day < earliest:
            continue
        else:
            today_availability: dict = {"date": day, "times": []}
            # if it's an available day
            availability = service.schedule.get(day.weekday(), None)
            if availability:
                while appointments[appt_pointer].start.date() < day:
                    appt_pointer += 1
                start: time = availability.open
                while start < availability.close:
                    r1 = Range(
                        start=start,
                        end=(
                            datetime.combine(day, start)
                            + timedelta(hours=service.duration)
                            - timedelta(minutes=1)
                        ),
                    )
                    r2 = Range(
                        start=appointments[appt_pointer].start,
                        end=appointments[appt_pointer].end,
                    )
                    latest_start = max(r1.start, r2.start)
                    earliest_end = min(r1.end, r2.end)
                    delta = earliest_end - latest_start
                    if delta > 0:
                        start = appointments[appt_pointer].end.time()
                    else:
                        today_availability["times"].append(
                            {"start": r1.start, "end": r1.end}
                        )
                        start = r1.end
        if today_availability["times"] > 0:
            available_times.append(today_availability)
    return available_times
