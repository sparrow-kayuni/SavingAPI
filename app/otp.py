import os
from twilio.rest import Client

class OTPVerificationClient:

    def __init__(self):
        self.account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        self.auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        self.verify_sid = 'VAf569353857e560c11aa580940430b1f3'

        self.client = Client(self.account_sid, self.auth_token)

    def send_otp(self, phone_number):
        
        return self.client.verify.v2.services(self.verify_sid) \
            .verifications.create(to=phone_number, channel='sms')
        

    def verify_otp(self, phone_number, otp):

        return self.client.verify.v2.services(self.verify_sid) \
            .verification_checks.create(to=phone_number, code=otp)