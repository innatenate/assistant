import smtplib, ssl
import universal
from twilio.rest import Client

sid = "AC3add3dbed314212e5a0db599eaa46d7c"
token = "cd06a3541a43c2381907f153901533ef"
client = Client(sid, token)


def report(args):
    priority = args[0]
    effect = args[1]
    traceback = args[2]
    if "WaitTimeOutError" in str(effect) or ("google" in str(effect) or "google" in str(traceback)) or "UnknownValueError" in str(effect):
        print('no')
        return

    message = client.messages.create(
      body=f"   \r|:|P{str(priority)}|:| \r{str(effect)} \r|:|Traceback|:| \r{str(traceback)}",
      from_="+12549024763",
      to="+19189024763")

    message.sid

    print(str(message))
