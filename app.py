from flask import Flask, jsonify, request, send_file
from datetime import date, datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from bson import ObjectId
from io import BytesIO
import pandas as pd
import http.client
import json
import logging

from messagesConfig import chatbotMessages
from messagesConfig import reducedMessageCodes
from messagesConfig import specialMessageCodes

app = Flask(__name__)

appDBPath = "mongodb://localhost:27017/"
appDB = "meta_db_100J"

mongoDBDomain = 'mongodb://localhost:27017/'
mongoDBPath = 'meta_db_100J'

metaToken = "EAAWXJp8ZCZCyABO7eqsGWDJih9F1ZAQGcXrK5DCxgbQjugPgvPiPKYwhCpcL6VGTI3M9DbfSzJClPTuXKS6KKhmsxNqknbI6ajV0GoLMKaKx3sOUWikq23FYORYmoQE0V9sjLb2Wj8PeCJSuftjCCxbCInAF89IT6If8KayZC7EiPKBfTFvVhwlvj6T6o7GNbCHvXZACJcq2lc8z7KpcbbzB8AQZDZD"
webhookToken = "CHATBOTTOKENTEST"

metaDomain = "graph.facebook.com"
metaPath = "/v20.0/374877792366425/messages"

blogDomain = "amun.bo"
blogPath = "/wp-json/juevesAccion/v1/posts-categoria/100-jueves-accion"

gamlpDomain = "131.0.0.17"
gamlpPort = 8008
gamlpPathGetToken = "/wsPC/obtTokenGamlp"
gamlpPathGetCiudadano = "/wsPC/obtCiudadano"
gamlpUser = "gamlpforo"
gamlpPass = "g4m4lpf0r0of2022"
gamlpToken = ""

client = MongoClient('mongodb://localhost:27017/')
db = client['meta_db_100J']

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
logging.getLogger("pymongo").setLevel(logging.WARNING)

session_store = {}
# ======= ======= ======= ROUTING SECTION ======= ======= =======
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if(request.method == 'GET'):
        challenge = verificar_token(request)
        return challenge
    elif(request.method == 'POST'):
        response = recibir_mensaje(request)
        return response
    
@app.route('/api/download-excel', methods=['GET'])
def download_excel():
    collection = db['data']
    
    data = list(collection.find({}, {'_id': 0}))
    
    if not data:
        return jsonify({"error": "No data available"}), 404
    
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='data.xlsx')

# ======= ======= ======= ======= ======= ======= =======
# ======= ======= ======= FUNCTIOS SECTIONS ======= ======= =======
# ======= ======= CLEANUP EXPIRED MESSAGE SESSIONS ======= =======
def cleanup_expired_sessions():
    app.logger.debug("======= CLEANNING UP INITED =======")
    current_time = datetime.now()
    expired_users = []
    for phoneNumber, userData in session_store.items():
        expiration_time = userData["lastAnswerDatetime"] + timedelta(minutes=15)
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
            connection.request("POST", metaPath, data, headers)
            response = connection.getresponse()
        except Exception as e:
            app.logger.error(f"Error en el envío de mensaje: {str(e)}")
            #addMessageLog(json.dumps(e))
        finally:
            connection.close()

        del session_store[phoneNumber]
# ======= ======= ======= ======== =======
# ======= ======= IS JSON FUN ======= =======
def is_json(string):
    try:
        json.loads(string)
        return True
    except ValueError:
        return False
# ======= ======= ======= ======== =======
# ======= ======= JSON SERIALIZER FUN ======= =======
def json_serializer(data):
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, list):
        return [json_serializer(item) for item in data]
    if isinstance(data, dict):
        return {key: json_serializer(value) for key, value in data.items()}
    return data
# ======= ======= ======= ======== =======
# ======= ======= VERITY TOKEN FUN ======= =======
def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

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

    messageScopeTypeToData = messageScopeType if (messageScopeType != "button") else ("interactive")

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
    # ======= ======= =======
    dataToReturn[messageScopeTypeToData] = messageContent
    return dataToReturn
# ======= ======= ======= ======== =======
# ======= ======= ======= ======== =======
def create_new_session_user(phoneNumber):
    userData = {
        "flowMessageCode": "",
        "ci": "",
        "name": "",
        "lastName1": "",
        "lastName2": "",
        "reqAction": "",
        "location": "",
        "media": "",
        "lastAnswerDatetime":datetime.now()
    }
    session_store[phoneNumber] = userData
# ======= ======= ======= ======== =======
# ======= ======= ======= ======== ======= ======= =======
# ======= ======= ======= RECEIVE MESSAGE FUNCTION ======= ======= =======
def recibir_mensaje(req):
    try:
        req = request.get_json()

        entry = req["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        messageObject = value["messages"]

        if(messageObject):
            messages = messageObject[0]
            if("type" in messages):
                phoneNumber = messages["from"]
                tipo = messages["type"]
                if(phoneNumber not in session_store):
                    create_new_session_user(phoneNumber)

                phoneNumberData = session_store.get(phoneNumber, None)

                app.logger.debug("============")
                app.logger.debug("PRE MESSAGE CODE: "+phoneNumberData["flowMessageCode"])
                app.logger.debug("============")

                #addMessage(json.dumps(messages))
                
                # ======= SAVING SPECIAL DATA SENDED =======
                if( phoneNumberData["flowMessageCode"]=="1211" ):
                    text = messages["interactive"]["button_reply"]["id"]
                    phoneNumberData["reqAction"] = "Deshierbe" if (text[-1] == "1") else (phoneNumberData["reqAction"])
                    phoneNumberData["reqAction"] = "Limpieza de aceras" if (text[-1] == "2") else (phoneNumberData["reqAction"])
                    phoneNumberData["reqAction"] = "Limpieza de cunetas" if (text[-1] == "3") else (phoneNumberData["reqAction"])

                elif( phoneNumberData["flowMessageCode"]=="121111" ):
                    text = messages["text"]["body"]
                    phoneNumberData["location"] = text

                elif( phoneNumberData["flowMessageCode"]=="121111111" ):
                    text = messages["interactive"]["button_reply"]["id"]
                    phoneNumberData["media"] = "Imagen enviada" if (text[-1] == "1") else (phoneNumberData["media"])
                    phoneNumberData["media"] = "Sin imagen" if (text[-1] == "2") else (phoneNumberData["media"])
                # ======= ======= =======
                # ======= CURRENT FLOW MESSAGE UPDATE =======
                if( phoneNumberData["flowMessageCode"]=="12" ):
                    text = messages["text"]["body"]
                    if((len(text) <= 12) and (text.isdigit())):
                        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"1"

                        headers = {
                            "Content-Type" : "application/json"
                        }
                        data = {
                            "usuario": gamlpUser,
                            "clave": gamlpPass
                        }
                        data = json.dumps(data)
                        connection = http.client.HTTPConnection(gamlpDomain, gamlpPort)
                        try:
                            connection.request("POST", gamlpPathGetToken, data, headers)
                            response = connection.getresponse()
                            if(response.status == 200):
                                data = response.read().decode('utf-8')
                                json_data = json.loads(data)
                                gamlpToken = json_data["token"]

                                dataGetCiudadano = {
                                    "ci": text
                                }
                                headers = {
                                    "Content-Type" : "application/json",
                                    "Authorization": "Bearer "+gamlpToken
                                }
                                dataGetCiudadano = json.dumps(dataGetCiudadano)
                                connection.request("POST", gamlpPathGetCiudadano, dataGetCiudadano, headers)
                                response = connection.getresponse()
                                if(response.status == 200):
                                    data = response.read().decode('utf-8')
                                    if(is_json(data)):
                                        json_data = json.loads(data)
                                        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"1"
                                        
                                        phoneNumberData["ci"] = text
                                        phoneNumberData["name"] = json_data["success"]["nombres"]
                                        phoneNumberData["lastName1"] = json_data["success"]["paterno"]
                                        phoneNumberData["lastName2"] = json_data["success"]["materno"]
                                    else:
                                        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"        
                                else:
                                    phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"
                            else:
                                phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"
                                print(f"Error en la solicitud: {response.status} {response.reason}")
                        except Exception as e:
                            phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"
                            app.logger.error(f"Error en el envío de mensaje: {str(e)}")
                        finally:
                            connection.close()

                    else:
                        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"

                elif(tipo == "interactive"):
                    text = messages["interactive"]["button_reply"]["id"]
                    phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+text[-1]

                elif("text" in messages):
                    text = messages["text"]["body"]
                    phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"1"
                # ======= ======= =======
                # ======= UPDATE FLOW MESSAGE CODE =======
                phoneNumberData["flowMessageCode"] = reduceMessageCode(phoneNumberData["flowMessageCode"])
                app.logger.debug("============")
                app.logger.debug("POST MESSAGE CODE: "+phoneNumberData["flowMessageCode"])
                app.logger.debug("============")
                # ======= ======= =======
                # ======= UPDATE DATA IN REDIS =======
                phoneNumberData["lastAnswerDatetime"] = datetime.now()
                session_store[phoneNumber] = phoneNumberData
                # ======= ======= =======

                enviar_mensajes_whatsapp(text, phoneNumber)

        return jsonify({'message':'EVENT RECEIVED'})

    except Exception as e:
        app.logger.debug(e)
        return jsonify({'message':'EVENT RECEIVED'})
# ======= ======= ======= ======= ======= ======= =======
# ======= ======= ======= SEND MESSAGE FUNCTION ======= ======= =======
def enviar_mensajes_whatsapp(texto, phoneNumber):
    global metaToken
    global metaDomain
    global metaPath

    global chatbotMessages
    global specialMessageCodes
    
    phoneNumberData = session_store.get(phoneNumber, None)

    dataList = []

    # ======= ======= PROCESSING MESSAGE ======= =======
    headers = {
        "Content-Type" : "application/json",
        "Authorization": "Bearer "+metaToken
    }
    data = generateMessageData(phoneNumber, chatbotMessages, "processing")
    data = json.dumps(data)

    connection = http.client.HTTPSConnection(metaDomain)
    try:
        connection.request("POST", metaPath, data, headers)
        response = connection.getresponse()
    except Exception as e:
        app.logger.debug("Error envio mensaje")
    finally:
        connection.close()
    # ======= ======= ======= ======= =======
    # ======= ======= CANCELAR MESSAGE ======= =======
    if(("cancelar") in (texto.lower())):
        phoneNumberData["flowMessageCode"] = "1"
        data = generateMessageData(phoneNumber, chatbotMessages, "cancel")
        dataList.append(data)
    # ======= ======= ======= ======= =======
    # ======= ======= TEST MESSAGE ======= =======
    if(("test") in (texto.lower())):
        data = generateMessageData(phoneNumber, chatbotMessages, "test")
        dataList.append(data)
    # ======= ======= ======= ======= =======
    # ======= ======= SEND COMMOND FORMAT MESSAGE ======= =======
    elif( phoneNumberData["flowMessageCode"] not in specialMessageCodes ):
        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"])
        dataList.append(data)
    # ======= ======= ======= ======= =======
    # ======= ======= SPECIAL MESSAGES ======= =======
    elif( phoneNumberData["flowMessageCode"]=="1" ):
        # ======= BLOG IMG SECTION =======
        blogLastPost = []

        conn = http.client.HTTPSConnection(blogDomain)
        conn.request("GET", blogPath)
        response = conn.getresponse()
        if(response.status == 200):
            data = response.read().decode('utf-8')
            json_data = json.loads(data)
            blogLastPost = json_data[0]
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phoneNumber,
                "type": "image",
                "image": {
                    "link": blogLastPost["featured_image"], 
                    "caption": blogLastPost["title"]+"\n"+blogLastPost["date"]+"\n"+blogLastPost["link"]
                }
            }
            dataList.append(data)
        else:
            print(f"Error en la solicitud: {response.status} {response.reason}")
        conn.close()
        # ======= ======= =======
        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"])
        dataList.append(data)

    elif( phoneNumberData["flowMessageCode"]=="11" ):
        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"]+"t")
        dataList.append(data)
        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"]+"b")
        dataList.append(data)

    elif( phoneNumberData["flowMessageCode"]=="1211" ):
        customText = chatbotMessages[phoneNumberData["flowMessageCode"]]["content"][0]
        fullName = phoneNumberData["name"]+" "+phoneNumberData["lastName1"]+" "+phoneNumberData["lastName2"]
        customText = customText.replace("[Nombre]", fullName)

        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"], customText)
        dataList.append(data)

    elif( (phoneNumberData["flowMessageCode"]=="12111") or (phoneNumberData["flowMessageCode"]=="12112") or (phoneNumberData["flowMessageCode"]=="12113") ):
        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"])
        dataList.append(data)
        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"][0:-1]+"11"
        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"])
        dataList.append(data)

    elif( phoneNumberData["flowMessageCode"]=="12111111111" ):
        customText = chatbotMessages[phoneNumberData["flowMessageCode"]]["content"][0]
        
        customText = customText.replace("[Numero]", phoneNumberData["ci"])
        fullName = phoneNumberData["name"]+" "+phoneNumberData["lastName1"]+" "+phoneNumberData["lastName2"]
        customText = customText.replace("[Nombre]", fullName)
        customText = customText.replace("[Accion]", phoneNumberData["reqAction"])
        customText = customText.replace("[Ubicacion]", phoneNumberData["location"])
        customText = customText.replace("[Imagen]", phoneNumberData["media"])

        try:
            newActionRegister = {
                "phoneNumber":phoneNumber,
                "fullName":fullName,
                "reqAction":phoneNumberData["reqAction"],
                "location":phoneNumberData["location"],
                "ci":phoneNumberData["ci"],
                "date":datetime.combine(date.today(), datetime.min.time())
            }
            collection = db['data']
            collection.insert_one(newActionRegister)
        except Exception as e:
            app.logger.debug("======= ERROR GUARDANDO MENSAJE =======")
            app.logger.debug(e)

        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"], customText)
        dataList.append(data)

        phoneNumberData["flowMessageCode"] = ""
        
    # ======= ======= ======= ======= =======
    # ======= ======= ======= ======= =======
    else:
        data = generateMessageData(phoneNumber, chatbotMessages, "invalid")
        dataList.append(data)
    # ======= ======= ======= ======= =======

    for dataItem in dataList:
        dataItem = json.dumps(dataItem)
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "Bearer "+metaToken
        }

        connection = http.client.HTTPSConnection(metaDomain)
        try:
            connection.request("POST", metaPath, dataItem, headers)
            response = connection.getresponse()
        except Exception as e:
            app.logger.error(f"Error en el envío de mensaje: {str(e)}")
            #addMessageLog(json.dumps(e))
        finally:
            connection.close()
# ======= ======= ======= ======== ======= ======= =======
# ======= ======= ======= APP INIT SECTION ======= ======= =======
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=cleanup_expired_sessions, trigger="interval", minutes=1)
    scheduler.start()
    app.run(host='0.0.0.0',port=80,debug=True)
# ======= ======= ======= ======= ======= ======= =======
