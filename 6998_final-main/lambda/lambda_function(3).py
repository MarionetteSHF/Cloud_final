import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
# import logger
#always start with the lambda_handler
def lambda_handler(event, context):
    print(event)
    user_name = str(event['user_name'])
    item_id = str(event['item_id'])
    # make the connection to dynamodb
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # select the table
    table = dynamodb.Table("User_new")
    item = table.get_item( Key={"user_name": user_name})
    # print(item)
    post_list=item['Item']['post_list']
    print( post_list)
    print("+++")
    post_list.remove(item_id)
    print(  post_list)
    response = table.update_item(
    Key={"user_name": user_name},
    UpdateExpression="set post_list=:post",
    ExpressionAttributeValues={':post': post_list},
    ReturnValues="UPDATED_NEW")
    table1 = dynamodb.Table("Items")
    response1 = table1.delete_item(
            Key={
                "item_id": item_id
            })
            
    return {
        'statusCode': 200,
        'body': json.dumps('successfully delete from post_list')
    }
