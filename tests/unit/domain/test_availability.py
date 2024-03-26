import pytest
import json
import datetime

from domain.service import get_service, Service
from domain.appointment import Appointment
from domain.availability import (
    get_availability,
    determine_date_range,
    calc_day_availability,
)


@pytest.fixture
def test_service_long():
    svc_data = {
        "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
        "service_id": "99c3fe67-a0f3-4e82-9b7d-ade93407aa29",
        "name": "Tattoo Consult",
        "active": False,
        "duration": 30,
        "max_per_day": 2,
        "start": "2024-04-01T00:00",
        "end": "2024-07-28T00:00",
        "schedule": {
            0: {"open": "09:00:00", "close": "16:00:00"},
            2: {"open": "09:00:00", "close": "16:00:00"},
            4: {"open": "09:00:00", "close": "16:00:00"},
            5: {"open": "11:00:00", "close": "14:00:00"},
        },
    }
    service = Service.model_validate(svc_data)
    return service


@pytest.fixture
def test_service_short():
    svc_data = {
        "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
        "service_id": "99c3fe67-a0f3-4e82-9b7d-ade93407aa29",
        "name": "Tattoo Consult",
        "active": False,
        "duration": 30,
        "max_per_day": 2,
        "start": "2024-05-12T00:00",
        "end": "2024-05-21T00:00",
        "schedule": {
            0: {"open": "09:00:00", "close": "16:00:00"},
            2: {"open": "09:00:00", "close": "16:00:00"},
            4: {"open": "09:00:00", "close": "16:00:00"},
            5: {"open": "11:00:00", "close": "14:00:00"},
        },
    }
    service = Service.model_validate(svc_data)
    return service


@pytest.fixture
def test_service_short_hrs():
    svc_data = {
        "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
        "service_id": "99c3fe67-a0f3-4e82-9b7d-ade93407aa29",
        "name": "Tattoo Consult",
        "active": False,
        "duration": 30,
        "max_per_day": 2,
        "start": "2024-05-12T00:00",
        "end": "2024-05-21T00:00",
        "schedule": {
            0: {"open": "11:00:00", "close": "14:00:00"},
            2: {"open": "11:00:00", "close": "14:00:00"},
            4: {"open": "11:00:00", "close": "14:00:00"},
            5: {"open": "11:00:00", "close": "14:00:00"},
        },
    }
    service = Service.model_validate(svc_data)
    return service


def test_get_date_window_returns_correct_date_passed(test_service_long):
    service = test_service_long
    earliest, latest = determine_date_range(service, "06-2024")
    assert earliest == datetime.date(2024, 6, 1)
    assert latest == datetime.date(2024, 6, 30)


def test_get_date_window_returns_no_date_passed(test_service_long):
    service = test_service_long
    earliest, latest = determine_date_range(service)
    assert earliest == datetime.date(2024, 4, 1)
    assert latest == datetime.date(2024, 4, 30)


def test_get_date_window_returns_correct_start_end_within_month(test_service_short):
    service = test_service_short
    earliest, latest = determine_date_range(service)
    assert earliest == datetime.date(2024, 5, 12)
    assert latest == datetime.date(2024, 5, 21)


def test_get_date_window_after_service_start_date_passed(test_service_long):
    service = test_service_long
    with pytest.raises(IndexError):
        determine_date_range(service, "06-2025")


def test_get_date_window_before_service_start_date(test_service_long):
    service = test_service_long
    with pytest.raises(IndexError):
        determine_date_range(service, "06-2023")


def test_get_date_window_just_before_service_start_date(test_service_long):
    service = test_service_long
    with pytest.raises(IndexError):
        determine_date_range(service, "03-2024")


def test_get_date_window_returns_no_date_passed(test_service_long):
    service = test_service_long
    earliest, latest = determine_date_range(service)
    assert earliest == datetime.date(2024, 4, 1)
    assert latest == datetime.date(2024, 4, 30)


def test_calc_day_availability_with_only_early_late_appts(test_service_short_hrs):
    service = test_service_short_hrs
    json_appts = [
        {
            "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
            "client_email": "tattoofiend@email.com",
            "start": "2024-04-08T06:15",
            "end": "2024-04-08T07:14",
            "confirmed": True,
            "canceled": False,
        },
        {
            "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
            "client_email": "tattoofiend@email.com",
            "start": "2024-04-08T14:15",
            "end": "2024-04-08T16:14",
            "confirmed": True,
            "canceled": False,
        },
    ]
    test_appts = [Appointment.model_validate(item) for item in json_appts]
    test_avail = calc_day_availability(service, test_appts, datetime.date(2024, 4, 3))
    assert test_avail == {
        "date": datetime.date(2024, 4, 3),
        "times": [
            {
                "end": datetime.datetime(2024, 4, 3, 11, 29),
                "start": datetime.datetime(2024, 4, 3, 11, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 11, 59),
                "start": datetime.datetime(2024, 4, 3, 11, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 12, 29),
                "start": datetime.datetime(2024, 4, 3, 12, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 12, 59),
                "start": datetime.datetime(2024, 4, 3, 12, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 13, 29),
                "start": datetime.datetime(2024, 4, 3, 13, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 13, 59),
                "start": datetime.datetime(2024, 4, 3, 13, 30),
            },
        ],
    }


def test_calc_day_availability_with_existing_appts(test_service_short_hrs):
    service = test_service_short_hrs
    json_appts = [
        {
            "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
            "client_email": "tattoofiend@email.com",
            "start": "2024-04-08T06:15",
            "end": "2024-04-08T07:14",
            "confirmed": True,
            "canceled": False,
        },
        {
            "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
            "client_email": "tattoofiend@email.com",
            "start": "2024-04-08T12:00",
            "end": "2024-04-08T12:59",
            "confirmed": True,
            "canceled": False,
        },
        {
            "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
            "client_email": "tattoofiend@email.com",
            "start": "2024-04-08T14:15",
            "end": "2024-04-08T16:14",
            "confirmed": True,
            "canceled": False,
        },
    ]
    test_appts = [Appointment.model_validate(item) for item in json_appts]
    test_avail = calc_day_availability(service, test_appts, datetime.date(2024, 4, 8))
    assert test_avail == {
        "date": datetime.date(2024, 4, 8),
        "times": [
            {
                "end": datetime.datetime(2024, 4, 8, 11, 29),
                "start": datetime.datetime(2024, 4, 8, 11, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 8, 11, 59),
                "start": datetime.datetime(2024, 4, 8, 11, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 8, 13, 29),
                "start": datetime.datetime(2024, 4, 8, 13, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 8, 13, 59),
                "start": datetime.datetime(2024, 4, 8, 13, 30),
            },
        ],
    }


def test_calc_day_availability_with_full_schedule(test_service_short_hrs):
    service = test_service_short_hrs
    json_appts = [
        {
            "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
            "client_email": "tattoofiend@email.com",
            "start": "2024-04-08T11:15",
            "end": "2024-04-08T12:14",
            "confirmed": True,
            "canceled": False,
        },
        {
            "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
            "client_email": "tattoofiend@email.com",
            "start": "2024-04-08T13:00",
            "end": "2024-04-08T13:59",
            "confirmed": True,
            "canceled": False,
        },
        {
            "user_id": "2dac127d-13e8-461e-aa6f-eed91d8e2fb5",
            "client_email": "tattoofiend@email.com",
            "start": "2024-04-08T14:00",
            "end": "2024-04-08T16:14",
            "confirmed": True,
            "canceled": False,
        },
    ]
    test_appts = [Appointment.model_validate(item) for item in json_appts]
    test_avail = calc_day_availability(service, test_appts, datetime.date(2024, 4, 8))
    assert test_avail == {
        "date": datetime.date(2024, 4, 8),
        "times": [
            {
                "end": datetime.datetime(2024, 4, 8, 12, 44),
                "start": datetime.datetime(2024, 4, 8, 12, 15),
            }
        ],
    }


def test_calc_day_availability_no_current_appointments(test_service_long):
    service = test_service_long
    test_avail = calc_day_availability(service, [], datetime.date(2024, 4, 3))
    assert test_avail == {
        "date": datetime.date(2024, 4, 3),
        "times": [
            {
                "end": datetime.datetime(2024, 4, 3, 9, 29),
                "start": datetime.datetime(2024, 4, 3, 9, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 9, 59),
                "start": datetime.datetime(2024, 4, 3, 9, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 10, 29),
                "start": datetime.datetime(2024, 4, 3, 10, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 10, 59),
                "start": datetime.datetime(2024, 4, 3, 10, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 11, 29),
                "start": datetime.datetime(2024, 4, 3, 11, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 11, 59),
                "start": datetime.datetime(2024, 4, 3, 11, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 12, 29),
                "start": datetime.datetime(2024, 4, 3, 12, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 12, 59),
                "start": datetime.datetime(2024, 4, 3, 12, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 13, 29),
                "start": datetime.datetime(2024, 4, 3, 13, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 13, 59),
                "start": datetime.datetime(2024, 4, 3, 13, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 14, 29),
                "start": datetime.datetime(2024, 4, 3, 14, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 14, 59),
                "start": datetime.datetime(2024, 4, 3, 14, 30),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 15, 29),
                "start": datetime.datetime(2024, 4, 3, 15, 0),
            },
            {
                "end": datetime.datetime(2024, 4, 3, 15, 59),
                "start": datetime.datetime(2024, 4, 3, 15, 30),
            },
        ],
    }
