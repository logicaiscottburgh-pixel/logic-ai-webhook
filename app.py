import os
from flask import Flask, request
import requests
app = Flask(__name__)
VERIFY_TOKEN = "logic_ai_scottburgh_2024"
PHONE_NUMBER_ID = "1284869951381853"
def send_whatsapp_message(to, message):
    token = os.getenv("WHATSAPP_TOKEN")
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {token}","Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp","to": to,"type": "text","text": {"body": message}}
    requests.post(url, headers=headers, json=data)
def get_logic_ai_reply(t):
    t=t.lower()
    if "hi" in t or "hello" in t:
        return "Hello! Welcome to *Logic AI* - Scottburgh's First AI Company.\n\nWe build 24/7 WhatsApp AI Assistants.\n\nReply:\n1 SERVICES\n2 DEMO\n3 PRICE\n4 BOOK"
    elif "service" in t or t=="1":
        return "*Logic AI Services*\n24/7 AI replies\nAnswers FAQs\nCaptures Leads\nTakes Bookings\nSpeaks Any Language\n\nReply DEMO or PRICE"
    elif "price" in t or t=="3":
        return "*Pricing*\nStarter R1500/mo\nPro R2500/mo\nNo setup fee for first 10 founders!\n\nReply BOOK"
    elif "demo" in t or t=="2":
        return "*Live Demo* Try: Do you have rooms for tonight for 2 people?"
    else:
        return "Thanks! Type: SERVICES, PRICE, or DEMO"
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"),200
    return "fail",403
@app.route('/webhook', methods=['POST'])
def webhook():
    data=request.get_json()
    try:
        for entry in data.get("entry",[]):
            for change in entry.get("changes",[]):
                for msg in change.get("value",{}).get("messages",[]):
                    if msg.get("type")=="text":
                        send_whatsapp_message(msg.get("from"), get_logic_ai_reply(msg.get("text",{}).get("body","")))
    except: pass
    return "OK",200
@app.route('/')
def home(): return "Logic AI LIVE"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT",10000)))
