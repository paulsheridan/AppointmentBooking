import json
import uuid

from pydantic import TypeAdapter
from typing import List

from service import DailySchedule, Service, create_service


def lambda_handler(message, context):
    request_data = json.loads(message["body"])

    service = Service(
        service_id=uuid.uuid4(),
        user_id=request_data["user_id"],
        name=request_data["name"],
        active=request_data["active"],
        duration=request_data["duration"],
        max_per_day=request_data["max_per_day"],
        start=request_data["start"],
        end=request_data["end"],
        schedule=request_data["schedule"],
    )

    create_service(service)

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(service.model_dump(exclude={"user_id"})),
    }
