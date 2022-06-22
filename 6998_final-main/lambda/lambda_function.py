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
    item=table.get_item( Key={"user_name": user_name})
    # print(item)
    if 'wish_list' in item['Item']:
        wishlist = item['Item']['wish_list']
    else:
        wishlist = []
    print(wishlist)
    print("+++")
    # if 1 in wishlist:
    if item_id not in wishlist:
        wishlist.append(item_id)

    print(wishlist)
    response = table.update_item(
        Key={"user_name": user_name},
        UpdateExpression="set wish_list=:wish",
        ExpressionAttributeValues={':wish': wishlist},
        ReturnValues="UPDATED_NEW")
    # except:
    #     print("Couldn't update")
    # else:
    print(response)
    print( response['Attributes'])
    return {
        'statusCode': 200,
        'body': json.dumps('Success add item to wishlist!')
    }
