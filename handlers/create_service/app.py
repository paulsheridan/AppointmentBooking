import json
import uuid

from pydantic import TypeAdapter
from typing import List

from service import DailySchedule, Service, create_service


def lambda_handler(message, context):
    user_id = message["requestContext"]["authorizer"]["claims"]["sub"]
    request_data = json.loads(message["body"])

    service = Service(service_id=uuid.uuid4(), user_id=user_id, **request_data)
    create_service(service)

    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(service.model_dump(exclude={"user_id"})),
    }
