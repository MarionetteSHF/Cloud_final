import json
import boto3
import uuid
from datetime import datetime
import dateutil.tz

def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Items')
    data = event['form_data']
    image_url = event['image_url']
    eastern = dateutil.tz.gettz('US/Eastern')
    date = datetime.now(tz=eastern).date().strftime("%d/%m/%Y")
    
    data1 = table.scan()
    items = data1['Items']
    this_category = []
    count=0
    for item in items:
        if int(item['item_id']) >int(count):
            count=item['item_id']
            
    count=int(count)+1 
    
    
    table.put_item(
        Item={
            # 'item_id': str(uuid.uuid4()),
            'item_id': str(count),
            'name': data['title'],
            'price': data['price'],
            'number': data['number'],
            'type': str(data['category']).lower(),
            'description': data['description'],
            'user_name': event['username'],
            'posted_at': date,
            'image_url': image_url
            # 'status':event['status'],
            # 'neededItem': event[' viewcount'],
            # 'Comment':{'serial':event['comment']['serial'],
            #     'date':event['comment']['serial'],
            #     'content':event['comment']['content']
                
            })
            
            
    table1 = dynamodb.Table('User_new')
    item=table1.get_item( Key={"user_name":  event['username']})
    post_list=item['Item']['post_list']
    print(post_list)
    post_list.append(str(count))
    response = table1.update_item(
        Key={"user_name": event['username']},
        UpdateExpression="set post_list=:post",
        ExpressionAttributeValues={':post': post_list},
        ReturnValues="UPDATED_NEW")
    print(response)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }