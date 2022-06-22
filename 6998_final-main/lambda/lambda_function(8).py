import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
"""
Allen changed Users table to User_new at 2:43AM 5/9/2022
"""
#always start with the lambda_handler
def lambda_handler(event, context):
    print(event)
    user_name = event['user_name']
    # make the connection to dynamodb
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # select the table
    table = dynamodb.Table("User_new")
    # get item from database
    item = table.get_item(Key={"user_name": user_name})
    # wishlist = item['Item']['wish_list']
    # print(item['Item']['wish_list'])
    return item