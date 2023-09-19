import os 
from mtnmomo.collection import Collection

api_secret = os.environ.get('API_SECRET')
user_id = os.environ.get('USER_ID')
primary_key = os.environ.get("PRIMARY_KEY")

client = Collection({
    "ENVIRONMENT": 'sandbox',
    "COLLECTION_USER_ID": user_id,
    "COLLECTION_API_SECRET": api_secret,
    "COLLECTION_PRIMARY_KEY": primary_key,
})

print(client.getBalance())

headers = {
            "X-Target-Environment": client.config.environment,
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": primary_key
        }

phoneNo = '075127525'

base_url = 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/accountholder/msisdn/'

res = client.request(url=base_url + f'{phoneNo}/basicuserinfo', headers=headers, method='GET')

print(res.json())

res = client.requestToPay(mobile='0765127525', amount='15', external_id=user_id, payee_note='dd', payer_message='dd', currency='EUR')

print(res)