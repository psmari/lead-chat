
from flask import Flask, request
import requests
from datetime import datetime, timedelta
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

import database.connection
from database.lead import Lead
from database.chat import Chat
from database.messages import Messages
from mongoengine.queryset.visitor import Q

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    response = ''
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    phone = request.values.get('WaId', '').lower()
    incoming_msg = request.values.get('Body', '')
    lead = verifyIfLeadExist(phone)
   
    if (lead):
        lastChat = verifyLastChat(lead.id)
       
        incoming_msg = incoming_msg.lower()
       
       
        if(lastChat and lastChat.date > datetime.now() - timedelta(days=1) and lastChat.send.type != 'over'):   
            if 'falar' in incoming_msg and 'especialista' in incoming_msg:
                response =  Messages.objects(Q(type="over") & Q(number="1"))[0]
                msg.body(response.text+"=Olá%20sou%20a%20"+lead.name+"%20Estava%20conversando%20com%20a%20Bastet")
                responded = True
                saveChat(response.id,incoming_msg,lead.id) 
                 
            elif(lastChat.send.type == 'options' and lastChat.send.number == "2"):
                if 'frase' in incoming_msg or '1' in incoming_msg:
                    # retorne uma citação 
                    r = requests.get('https://api.quotable.io/random')
                    if r.status_code == 200:
                        data = r.json()
                        response = f'{data["content"]} ({data["author"]})'
                    else:
                        response = 'Não consegui recuperar uma citação neste momento, desculpe.'
                    msg.body(response)
                    responded = True
                if 'gato' in incoming_msg or 'gata' in incoming_msg or '2' in incoming_msg:
                    # retorne uma foto de gato
                    msg.media('https://cataas.com/cat')
                    responded = True
                if not responded:
                    response = 'Eita, não consegui entender, desculpe!'
                    msg.body(response)
            elif(lastChat.send.type == 'options' and lastChat.send.number == "1"):
                incoming_msg = incoming_msg.lower()
                if 'falar' in incoming_msg or 'especialista' in incoming_msg or '1' in incoming_msg:
                    response =  Messages.objects(Q(type="over") & Q(number="1"))[0]
                    msg.body(response.text+"=Olá%20sou%20a%20"+lead.name+"%20Estava%20conversando%20com%20a%20Bastet")
                    responded = True
                    saveChat(response.id,incoming_msg,lead.id) 
                if 'remarcar' in incoming_msg or 'reunião' in incoming_msg or '2' in incoming_msg:
                    response = Messages.objects(Q(type="meeting") & Q(number="2"))[0]
                    msg.body(response.text)
                    responded = True
                    saveChat(response.id,incoming_msg,lead.id) 
                if 'frase' in incoming_msg or '3' in incoming_msg:
                    # retorne uma citação 
                    r = requests.get('https://api.quotable.io/random')
                    if r.status_code == 200:
                        data = r.json()
                        response = f'{data["content"]} ({data["author"]})'
                    else:
                        response = 'Não consegui recuperar uma citação neste momento, desculpe.'
                    msg.body(response)
                    responded = True
                if 'gato' in incoming_msg or 'gata' in incoming_msg or '4' in incoming_msg:
                    # retorne uma foto de gato
                    msg.media('https://cataas.com/cat')
                    responded = True
                if not responded:
                    response = 'Eita, não consegui entender, desculpe!'
                    msg.body(response)
                   
            elif(lastChat.send.type == 'form'):
                if(lastChat.send.number == '1'):
                    response = Messages.objects(Q(type="form") & Q(number="2"))[0]
                    msg.body(response.text)     
                    saveChat(response.id,incoming_msg,lead.id)
                    Lead.objects(id=lead.id).update_one(set__name=incoming_msg)
                elif(lastChat.send.number == '2'):
                    response = Messages.objects(Q(type="form") & Q(number="3"))[0]
                    msg.body(response.text)        
                    saveChat(response.id,incoming_msg,lead.id)
                    Lead.objects(id=lead.id).update_one(set__email=incoming_msg.strip())
                elif(lastChat.send.number == '3'):
                    if '1' in incoming_msg or 'logo' in incoming_msg: 
                        response = Messages.objects(Q(type="logo") & Q(number="1"))[0]
                        saveChat(response.id,incoming_msg,lead.id)
                    elif '2' in incoming_msg or 'site' in incoming_msg:
                        response = Messages.objects(Q(type="site") & Q(number="1"))[0]
                        saveChat(response.id,incoming_msg,lead.id)
                    else:
                        response = 'Eita, não consegui entender, desculpe!'
                    msg.body(response.text)        
            elif(lastChat.send.type == 'logo'):
                if(lastChat.send.number == '1'):
                    incoming_msg = incoming_msg.lower()
                    if 'sim' in incoming_msg or '1':
                        response = Messages.objects(Q(type="logo") & Q(number="2"))[0]
                        msg.body(response.text)     
                        saveChat(response.id,incoming_msg,lead.id)
                    elif 'não' in incoming_msg or '2':
                        response = "Entendi, então vai ser um grande desafio para os nossos especialistas :)\nAdoramos isso ^^"
                        msg.body(response.text)     
                        saveChat(response.id,incoming_msg,lead.id)
                        response2 = Messages.objects(Q(type="logo") & Q(number="3"))[0]
                        msg2 = resp.message()
                        msg2.body(response2.text)        
                        saveChat(response2.id,incoming_msg,lead.id)
                       
                elif(lastChat.send.number == '2'):
                    response = Messages.objects(Q(type="logo") & Q(number="3"))[0]
                    msg.body(response.text)        
                    saveChat(response.id,incoming_msg,lead.id)
                    Lead.objects(id=lead.id).update_one(set__brand=incoming_msg)
                elif(lastChat.send.number == '3'):
                    response = Messages.objects(Q(type="logo") & Q(number="4"))[0]
                    msg.body(response.text)        
                    saveChat(response.id,incoming_msg,lead.id)
                elif(lastChat.send.number == '4'):
                    checkMeeting(incoming_msg, msg,resp,lead)
            elif(lastChat.send.type == 'site'):
                if(lastChat.send.number == '1'):
                    incoming_msg = incoming_msg.lower()
                    if 'sim' in incoming_msg or '1':
                        response = Messages.objects(Q(type="site") & Q(number="4"))[0]
                        msg.body(response.text)     
                        saveChat(response.id,incoming_msg,lead.id)
                    elif 'não' in incoming_msg or '2':
                        response = Messages.objects(Q(type="site") & Q(number="2"))[0]
                        msg.body(response.text)     
                        saveChat(response.id,incoming_msg,lead.id)
             
                elif(lastChat.send.number == '2'):
                    response = Messages.objects(Q(type="site") & Q(number="3"))[0]
                    msg.body(response.text)        
                    saveChat(response.id,incoming_msg,lead.id)
                    
                elif(lastChat.send.number == '3'):
                    checkMeeting(incoming_msg, msg,resp,lead)
                elif(lastChat.send.number == '4'):
                    checkMeeting(incoming_msg, msg,resp,lead)
            elif(lastChat.send.type == 'meeting'):
                if 'sim' in incoming_msg or '1':
                    response = Messages.objects(Q(type="over") & Q(number="2"))[0]
                    msg.body(response.text)     
                    saveChat(response.id,incoming_msg,lead.id)
                elif 'não' in incoming_msg or '2':
                    response = Messages.objects(Q(type="over") & Q(number="3"))[0]
                    msg.body(response.text)     
                    saveChat(response.id,incoming_msg,lead.id)
        else:
            response = Messages.objects(Q(type="greetings") & Q(number="2"))[0]
            msg.body(response.text+lead.name)
            saveChat(response.id,incoming_msg,lead.id)
            response2 = Messages.objects(Q(type="options") & Q(number="1"))[0]
            msg2 = resp.message()
            msg2.body(response2.text)        
            saveChat(response2.id,incoming_msg,lead.id)
     
    else:
        lead = saveLead(phone, request.values.get('ProfileName', ''))
        response = Messages.objects(Q(type="greetings") & Q(number="1"))[0]
        msg.body(response.text)
        saveChat(response.id,incoming_msg,lead.id)
        response2 = Messages.objects(Q(type="form") & Q(number="1"))[0]
        msg2 = resp.message()
        msg2.body(response2.text)        
        saveChat(response2.id,incoming_msg,lead.id)

    return str(resp)

def verifyLastChat(search):
    try:
        lastChat = Chat.objects(lead_id=search).order_by('-date')[0] 
    except Chat.DoesNotExist:
        lastChat = None
    return lastChat
    

def verifyIfLeadExist(search):
    try:
        lead = Lead.objects.get(phone=search)
    except Lead.DoesNotExist:
        lead = None
    return lead

def saveChat(send_id,receive,lead_id):
    chat = Chat(send=send_id)
    chat.receive = receive
    chat.date = datetime.now()
    chat.lead_id = lead_id
    chat.save()

def saveLead(phone,name):
    lead = Lead(phone= phone)
    lead.username_whats = name
    lead.name = name
    lead.save()
    return lead

def checkMeeting(incoming_msg,msg,resp,lead):
    response = "Insira essa identificação "+str(lead.id)+" no terceiro campo do 'preencha seus dados' do calendly\n\n\n"
    msg.body(response)
    response1 = Messages.objects(Q(type="meeting") & Q(number="1"))[0]
    msg1 = resp.message()
    msg1.body(response1.text)        
    saveChat(response1.id,incoming_msg,lead.id)
    response2 = Messages.objects(Q(type="meeting") & Q(number="3"))[0]
    msg2 = resp.message()
    msg2.body(response2.text)


if __name__ == '__main__':
   app.run()
