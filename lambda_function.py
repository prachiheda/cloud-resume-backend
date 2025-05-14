import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('cloud-resume-challenge-managed2')

def lambda_handler(event, context):
    print(f"Received event: {event}")

    if event.get('rawPath') == '/favicon.ico':
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Request for favicon ignored'})
        }

    # Try to retrieve the item
    response = table.get_item(Key={'viewCountKey': '1'})
    item = response.get('Item')

    if item is None:
        # Initialize the counter
        count = 1
        table.put_item(Item={'viewCountKey': '1', 'count': Decimal(count)})
    else:
        # Increment existing count
        count = int(item['count']) + 1
        table.update_item(
            Key={'viewCountKey': '1'},
            UpdateExpression='SET #v = :val',
            ExpressionAttributeNames={'#v': 'count'},
            ExpressionAttributeValues={':val': Decimal(count)}
        )

    return {
        'statusCode': 200,
        'body': json.dumps({'count': count})
    }
