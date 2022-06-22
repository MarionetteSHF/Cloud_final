import json
import boto3
import random
def lambda_handler(event, context):
    # TODO implement
    print(event)
    user_name = event['user_id']
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    t2 = dynamodb.Table("User_new")
    cur=t2.get_item(Key={"user_name":user_name})
    print(cur)
    user_id = cur['Item']['user_id']
    recommendations=get_recommendations_for_user("arn:aws:personalize:us-east-1:719950645153:campaign/test1", user_id , 3)
    print(recommendations)
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    items = []
    t1 = dynamodb.Table("Items")
    for item_id in recommendations:
        item=t1.get_item(Key={"item_id":str(item_id)})
        print(item['Item'])
        items.append(item['Item'])
    return items
# personalize_runtime= None

def get_recommendations_for_user( campaign_arn, user_id, nums_result=3):
    personalizeRt = boto3.client('personalize-runtime')
    response=personalizeRt.get_recommendations( 
        campaignArn=campaign_arn,
        userId=str(user_id),
        numResults= nums_result
        )
    print(response)
    recommendations=[]
    for item in response['itemList']:
        recommendations.append( item["itemId"])
    
    random_list = [1,3,5,8,10,14,15,16,17,18,19]
    
    random_n1 = random.randint(0, len(random_list)-1)
    
    return [random_list[random_n1], random_list[random_n1 - 1], random_list[random_n1 -2]]