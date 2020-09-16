import json
import os
import requests

BOT_ID = os.environ['TELEGRAM_BOT_ID']
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
BASE_URL = f"https://api.telegram.org/{BOT_ID}:{TOKEN}"


def lambda_handler(event, context):
    '''
    Manage SNS event message and create the request
    to the telegram bot.
    '''
    try:
        # Get data from SNS event message
        sns_event = event['Records'][0]['Sns']
        sns_event_msg = json.loads(sns_event['Message'])
        sns_ns = sns_event_msg['NewStateValue']
        dv = sns_event_msg['Trigger']['Dimensions'][0]['value']
        # Create message for telegram
        todo = 'sendMessage'
        msg = f'Monitoring status for resource: {dv}. New State is: {sns_ns}'
        url = f"{BASE_URL}/{todo}?chat_id={CHAT_ID}&text={msg}"
        # Send request to the telegram bot
        requests.get(url)
    except Exception as e:
        print(e)

    return {"statusCode": 200}
