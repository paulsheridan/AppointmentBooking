import boto3
import os

def get_dynamodb_table():
    region = os.environ.get("AWS_REGION")
    aws_environment = os.environ.get("AWSENV")
    table_name = os.environ.get("TABLE_NAME")

    if aws_environment == "AWS_SAM_LOCAL":
        table_resource = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
    else:
        table_resource = boto3.resource("dynamodb", region_name=region)

    return table_resource.Table(table_name)
