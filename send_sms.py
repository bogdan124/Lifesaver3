import os
from twilio.rest import TwilioRestClient

account = "ACc91587ee64e71f9508256557c2ede901"
token = "07bb06566e217647879579d7f915a7f8"
client = TwilioRestClient(account,token)

message = client.messages.create(to="+40766659724", from_="+15182558827",
                                 body="Hello there")
##200 mesaje
