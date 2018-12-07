import sys
from flask import Flask, request, render_template
from utils import wit_response
from pymessenger import Bot, Element, Button

from pprint import pprint


app = Flask(__name__)

# Facebook apps link:   https://developers.facebook.com/apps/2222049801408664/dashboard/
FB_ACCESS_TOKEN = "EAAPOUQnZAX9QBAHZCzrEzvohA96SXvq46q6hfooLqYyk7ppi6TCF2YZAZBWS19yx9TpxB6OJM3iC58qsuFNK2Bc0ZArahqVmAT2g1zgFbzUKcYcPR46GMxzWo8cfzNHoLvhFtzdNuYCExVt3OjwTFycGFdyxNjkOfZBdeTfABQpQZDZD"

bot = Bot(FB_ACCESS_TOKEN)

VERIFICATION_TOKEN = "hello"


@app.route('/', methods=['GET'])
def verify():
    # Web hook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return render_template("index.html")


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    # **Necessary Code that extract json data facebook send**
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    # add for image reply
                    elif 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['attachments']

                    else:
                        messaging_text = 'no text'

                    response = None
                    entity, value = wit_response(messaging_text)

                    if entity == 'greetings':
                        response = " অাপনি কেমন আছেন"
                        bot.send_text_message(sender_id, response)

                    elif entity == 'services':
                        response = " আমাদের অনেক রকমের সেবা আছে, তবে ফাইল চেক করাতে টাকা লাগে না । "
                        bot.send_text_message(sender_id, response)

                    elif entity == 'assist':
                        response = " বলুন আপনাকে কিভাবে সাহায্য করতে পারি । "
                        bot.send_text_message(sender_id, response)

                    elif entity == 'recommend':
                        response = " আপনি কাজের জন্য না পরাশুনা করতে যাবেন । "
                        bot.send_text_message(sender_id, response)

                    elif entity == 'business':
                        response = " আপনি কোন দেশে যাবেন ? "
                        bot.send_text_message(sender_id, response)

                    elif entity == 'location':
                        response = " নিজের লিংকে একটা ফর্ম আছে সেটি পুরন করুন । https://sites.google.com/view/human-migration-services/"
                        bot.send_text_message(sender_id, response)

                    elif entity == 'yes':
                        response = "নিজের লিংকে একটা ফর্ম আছে সেটি পুরন করুন । https://sites.google.com/view/human-migration-services/ "
                        bot.send_text_message(sender_id, response)

                    elif entity == 'Address':
                        response = " আপনি ঢাকা না চিটাগাং আফিসে আসতে চান ।"
                        bot.send_text_message(sender_id, response)

                    elif entity == 'Dhaka_office_address':
                        response = " 121/C, Gulshan Avenue, Dhaka-1212"
                        bot.send_text_message(sender_id, response)

                    elif entity == 'thanks':
                        response = " ভাল থাকবেন ।"
                        bot.send_text_message(sender_id, response)

                    if response == None:
                        response = " "
                        bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    # previously it was print now I just Use Petty Print
    pprint(message)
    sys.stdout.flush()

@app.route('/Privacy-Policy')
def privacy_policy():
    return render_template("Privacy-Policy.html")


if __name__ == "__main__":
    app.run(port=80, use_reloader=True)
