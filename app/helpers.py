# ======= ======= ======== HELPERS FILE ======= ======= =======
# THIS FILE IS WHERE IS LOCATED ALL THE FUNCTIONS THAT HELP IN
# THAT DATA PROCESS
# ======= ======= ======== ======= ======= ======= =======
from flask import jsonify, current_app
from datetime import datetime, timedelta
import http.client
import json

from .messagesConfig import chatbotMessages
from .messagesConfig import reducedMessageCodes

# ======= ======= ======= FUNCTIOS SECTIONS ======= ======= =======
# ======= ======= CLEANUP EXPIRED MESSAGE SESSIONS ======= =======
def cleanup_expired_sessions(app_scope):
    with app_scope.app_context():
        metaToken = app_scope.config['META_TOKEN']
        metaDomain = app_scope.config['META_DOMAIN']
        metaMessagesPath = app_scope.config['META_MESSAGES_PATH']
        
        current_time = datetime.now()
        expired_users = []


        for phoneNumber, userData in app_scope.config['SESSIONS_STORE'].items():
            timeDelta = (10) if (userData["specialState"] != "12") else (60)
            expiration_time = userData["lastAnswerDatetime"] + timedelta(minutes=timeDelta)
            if (current_time >= expiration_time):
                expired_users.append(phoneNumber)

        for phoneNumber in expired_users:
            data = generateMessageData(phoneNumber, chatbotMessages, "timeout")
            data = json.dumps(data)
            headers = {
                "Content-Type" : "application/json",
                "Authorization": "Bearer "+metaToken
            }

            connection = http.client.HTTPSConnection(metaDomain)
            try:
                connection.request("POST", metaMessagesPath, data, headers)
                response = connection.getresponse()
            except Exception as e:
                app_scope.logger.error(f"Error en el envío de mensaje: {str(e)}")
                #addMessageLog(json.dumps(e))
            finally:
                connection.close()

            del app_scope.config['SESSIONS_STORE'][phoneNumber]
# ======= ======= ======= ======== =======
# ======= ======= VERITY TOKEN FUN ======= =======
def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    webhookToken = current_app.config['WEBHOOK_TOKEN']

    if(challenge and (token == webhookToken)):
        return challenge
    else:
        return jsonify({'error':'Token Invalido'}),401
# ======= ======= ======= ======== =======
# ======= ======= REDUCE MESSAGE CODE ======= =======
def reduceMessageCode(messageCode):
    global reducedMessageCodes
    messageCode = messageCode if(messageCode not in reducedMessageCodes) else(reducedMessageCodes[messageCode])

    return messageCode

# ======= ======= ======= ======== =======
# ======= ======= GENERATE MESSAGE DATA ======= =======
def generateMessageData(phoneNumber, messageList, messageCode, customText=None):
    messageScope = messageList[messageCode]
    messageScopeType = messageScope["type"]
    messageScopeContent = messageScope["content"]

    messageFinalText = messageScopeContent[0] if(not customText) else (customText)

    messageScopeTypeToData = messageScopeType if (messageScopeType == "text") else ("interactive")

    # ======= DATA DEFINITION =======
    dataToReturn = {
        "messaging_product": "whatsapp",    
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": messageScopeTypeToData
    }
    # ======= ======= =======
    # ======= CONTENT DEFINITION =======
    messageContent = {}
    if( messageScopeType == "text" ):
        messageContent = { 
            "preview_url": False,
            "body": messageFinalText
        }

    elif( messageScopeType == "button" ):
        buttonsInContent = []

        for data in messageScopeContent:
            if isinstance(data, list):
                dataToAdd = {
                    "type": "reply",
                    "reply":{
                        "id": data[0],
                        "title": data[1]
                    }
                }
                buttonsInContent.append(dataToAdd)

        messageContent = {
            "type": messageScopeType,
            "body":{
                "text": messageFinalText
            },
            "footer":{
                "text": messageScopeContent[1]
            },
            "action":{
                "buttons":buttonsInContent
            }
        }

    elif( messageScopeType == "list" ):
        buttonsInContent = []

        for data in messageScopeContent:
            if isinstance(data, list):
                dataToAdd = {
                    "id": data[0],
                    "title": data[1],
                    "description":data[2]
                }
                
                buttonsInContent.append(dataToAdd)

        messageContent = {
            "type": messageScopeType,
            "body":{
                "text": messageFinalText
            },
            "footer":{
                "text": messageScopeContent[1]
            },
            "action":{
                "button":messageScopeContent[2],
                "sections":[
                    {
                        "title": "",
                        "rows": buttonsInContent
                    }
                ]
            }
        }

    elif( messageScopeType == "location_request_message" ):
        messageContent = { 
            "type": messageScopeType,
            "body": {
                "text": messageFinalText
            },
            "action":{
                "name": "send_location"
            }
        }
    # ======= ======= =======
    dataToReturn[messageScopeTypeToData] = messageContent
    return dataToReturn
# ======= ======= ======= ======== =======
# ======= ======= ======= ======== =======
def create_new_session_user(phoneNumber):
    userData = {
        "flowMessageCode": "",
        "specialState": "",
        "invalidMessageCount": 0,
        "ci": "",
        "name": "",
        "lastName1": "",
        "lastName2": "",
        "reqAction": "",
        "location": "",
        "media": "",
        "mediaId":"",
        "latitude":0,
        "longitude":0,
        "lastAnswerDatetime":datetime.now()
    }
    current_app.config['SESSIONS_STORE'][phoneNumber] = userData
# ======= ======= ======= ======== =======
# ======= ======= ======= ======== =======
def strInSublist(str, listScope):
    for item in listScope:
        if(isinstance(item, list)):
            if(str in item):
                return True
    return False
# ======= ======= ======= ======== =======
# ======= ======= ======= ======== ======= ======= =======
