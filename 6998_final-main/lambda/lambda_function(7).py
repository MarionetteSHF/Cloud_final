import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

#always start with the lambda_handler
def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    t2 = dynamodb.Table("Items")
    if (event['item_id']):
        item_id = str(event['item_id'])
        # make the connection to dynamodb
        cur=t2.get_item(Key={"item_id":item_id})
        print(cur)
        if 'Item' not in cur:
            return {}
        return cur['Item']
    else: 
        table = dynamodb.Table("Items")
        data = table.scan()
        items = data['Items']
        this_category = []
        for item in items:
            if item['type'] == str(event["category"]).lower():
                this_category.append(item)
        print(this_category)
        # return {
        # 'statusCode': 200,
        # 'body':this_category
        # }
        return this_category
        
        # return {
        # 'statusCode': 200,
        # 'headers': {
        #     'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Accept,x-amz-meta-customLabels',
        #     'Access-Control-Allow-Origin': '*',
        #     'Access-Control-Allow-Methods': 'OPTIONS,PUT,GET'
        # },
        # 'body': this_category
        # }