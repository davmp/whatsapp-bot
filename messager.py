import os
import aiohttp
from dotenv import load_dotenv
from twilio.rest import Client


class Messager:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']

    async def send_message(self, body, to, from_="whatsapp:+14155238886"):
        auth = aiohttp.BasicAuth(
            login=self.account_sid, password=self.auth_token)
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(
                login=self.account_sid, password=self.auth_token)) as session:
            return await session.post(
                f'https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json',
                data={'From': from_, 'To': to, 'Body': body})
