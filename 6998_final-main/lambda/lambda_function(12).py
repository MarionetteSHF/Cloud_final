import json
import boto3
import os
import logging
import json
import logging

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    bot = boto3.client('s3')
    
    # boto = boto3.session.Session('','',region_name='us-east-1')
    # TODO implement
    
    info = event['Records'][0]['s3']
    bucket_name = info['bucket']['name']
    file_name = info['object']['key']
    headObject = bot.head_object(Bucket=bucket_name, Key=file_name)
    # metaData = headObject['Metadata']
    # custom_label = metaData['customlabels']
    # print(custom_label)
    
    # logger.info(event)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table("Items")
    # logger(event["Records"][0]["s3"]["object"]["key"])
    image_url="https://final-item-photos.s3.amazonaws.com/"+event["Records"][0]["s3"]["object"]["key"]
    print( image_url)
    #     if ( event['item_id'] ):
    # item_id = str(event['item_id'])
    # # make the connection to dynamodb
    response = table.update_item(
    Key={ "item_id":"7"},
    UpdateExpression="set image_url =:val",
    ExpressionAttributeValues={':val': image_url},
    ReturnValues="UPDATED_NEW")
    print(ExpressionAttributeValues)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
