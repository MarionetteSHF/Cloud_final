import json
from boto3.dynamodb.conditions import Key, Attr
import boto3

def lambda_handler(event, context):
    # TODO implement]
    print(event)
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Items')
    data = event['form_data']
    item_id = str(event['item_id'])
    print(item_id)
    response= table.update_item(
        Key= {
            "item_id": item_id
        },
        #  'name' =:n , 
        UpdateExpression= "set #na = :name_, price =:p, #num =:number_, #ty =:type_, description =:d",
        ExpressionAttributeValues = {
            ':name_': data['title'],
            ':p': data['price'],
            ':number_': data['number'],
            ':type_': data['category'].lower(),
            ':d': data['description']
            
        },
        ExpressionAttributeNames={
            "#na": "name",
            '#num': "number",
            '#ty': "type"
        },
        ReturnValues="UPDATED_NEW"
        )
    print( response['Attributes'])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
