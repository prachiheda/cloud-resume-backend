import os

# Mock AWS credentials for moto
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_SECURITY_TOKEN'] = 'testing'
os.environ['AWS_SESSION_TOKEN'] = 'testing'

import boto3
from moto import mock_aws
from decimal import Decimal
import pytest
from lambda_function import lambda_handler

@mock_aws
def test_lambda_handler_increment():
    # Set up the mock DynamoDB table
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.create_table(
        TableName='cloud-resume-challenge-managed2',
        KeySchema=[
            {
                'AttributeName': 'viewCountKey',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'viewCountKey',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.wait_until_exists()

    # Insert a test item
    table.put_item(Item={'viewCountKey': '1', 'count': Decimal('1')})

    # Mock event
    event = {
        'rawPath': '/'
    }

    # Call the lambda_handler function
    result = lambda_handler(event, None)

    # Assert the returned count is incremented
    assert result == 2

    # Fetch the updated item from DynamoDB
    response = table.get_item(Key={'viewCountKey': '1'})
    updated_count = int(response['Item']['count'])

    # Assert the count in DynamoDB is incremented
    assert updated_count == 2

@mock_aws
def test_lambda_handler_favicon():
    # Set up the mock DynamoDB table (though it won't be used)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    dynamodb.create_table(
        TableName='cloud-resume-challenge-managed2',
        KeySchema=[
            {
                'AttributeName': 'viewCountKey',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'viewCountKey',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Mock event for favicon
    event = {
        'rawPath': '/favicon.ico'
    }

    # Call the lambda_handler function
    result = lambda_handler(event, None)

    # Assert the response is correct
    assert result == {
        'statusCode': 200,
        'body': '{"message": "Request for favicon ignored"}'
    }
