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
    wishlist=item['Item']['wish_list']
    print(wishlist)
    print("+++")
    # if 1 in wishlist:
    wishlist.remove(item_id)
    print(wishlist)
    response = table.update_item(
    Key={"user_name": user_name},
    UpdateExpression="set wish_list=:wish",
    ExpressionAttributeValues={':wish': wishlist},
    ReturnValues="UPDATED_NEW")
    return {
        'statusCode': 200,
        'body': json.dumps('successfully delete from wishlist!')
    }
