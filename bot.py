from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'frase' in incoming_msg:
        # retorne uma citação 
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'Não consegui recuperar uma citação neste momento, desculpe.'
        msg.body(quote)
        responded = True
    if 'gato' in incoming_msg or 'gata' in incoming_msg:
        # retorne uma foto de gato
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('Só conheço frases e gatos famosos, desculpe!')
    return str(resp)

if __name__ == '__main__':
   app.run()
