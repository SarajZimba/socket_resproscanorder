import os
import firebase_admin
from firebase_admin import credentials, messaging

# Get the directory path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to "fb.json"
json_path = os.path.join(current_dir, "fb.json")
# print(f"json path is {json_path}")

cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred)


def send_notification(token, title, body, holder):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=holder,
            token=token
        )
        response = messaging.send(message)
        if response and 'error' in response:
            # Handle error
            print('Error sending message:', response['error'])
        else:
            # Message sent successfully
            print('Message sent successfully:', response)
    except Exception as e:
        print(e)

    # print('Successfully sent message:', response)

# This function is used for the sending notifications 
