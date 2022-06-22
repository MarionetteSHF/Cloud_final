import json
import boto3
def lambda_handler(event, context):
    # TODO implement
    print(event)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('User_new')
    # {
    #   "username": "al",
    #   "phone": "12311",
    #   "email": "hhh@hhh",
    #   "password":"678usf"
    # }
    # NOTE: user_id is string type 
    print
    data1 = table.scan()
    items = data1['Items']
    # this_category = []
    count=0
    for item in items:
        if int(item['user_id']) >int(count):
            count=item['user_id']
    count=int(count)+1 
    table.put_item(
        Item={
            'user_name': event['username'],
            'user_id' : str( count),
            'phone': event['phone'],
            'email': event['email'],
            'wish_list':[ ], 
            "post_list":[ ]
        }
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda: New user is added!')
    }
