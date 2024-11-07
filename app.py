from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
from datetime import datetime
import http.client
import json
import logging

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['meta_db_100J']

metaToken = "EAAWXJp8ZCZCyABOZCg3wHvSCd51Qu53YugEM3ixZADjGsXpQhSWHZBLMPtsxN8GyGcSERhXkGub9GJgEShKrPggO7qFu6ZAzX5sO4alQhDlmz5dhk2iBMH1TqqZAs9EdCVZBtomAXslvbVZACn5fqKYmd7CKgA8amVoB6vnlZCwE2l9mmALMwfOAQ4A8TwWTmf71VAUWZCZBa3pnNJL60rsxaZCOonasl"
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

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# ======= ======= ======= ROUTING SECTION ======= ======= =======
@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if(request.method == 'GET'):
        challenge = verificar_token(request)
        return challenge
    elif(request.method == 'POST'):
        response = recibir_mensaje(request)
        return response

@app.route('/api/data', methods=['GET'])
def get_data():
    collection = db['data']
    data = list(collection.find({}))
    return jsonify(json_serializer(data))

@app.route('/api/data', methods=['POST'])
def add_data():
    new_data = request.json
    collection = db['data']
    collection.insert_one(new_data)
    return jsonify(json_serializer(new_data)), 201
# ======= ======= ======= ======= ======= ======= =======
# ======= ======= TEXT TO USE ======= =======
chatbotMessages = {
    "test": { 
        "type": "text", 
        "content": [
            "Test Message"
        ] 
    },
    "processing": { 
        "type": "text", 
        "content": [
            "⏰. Procesando..."
        ] 
    },
    "invalid": { 
        "type": "text", 
        "content": [
            "Parece que la información ingresada no es válida. Por favor, asegúrate de proporcionar datos correctos.",
            "Estoy aquí para ayudarte, pero parece que hemos recibido información incorrecta varias veces. Si no puedes continuar, te sugiero que nos llames al 155 para más ayuda"
        ] 
    },
    "cancel": { 
        "type": "text", 
        "content": ["Operacion cancelada, volviendo al menu."] 
    },
    "1": {
        "type": "button",
        "content": [
            "¡Hola! Bienvenido/a al proyecto 100 jueves de Acción por el Bien Común. Estoy aquí para ayudarte a contribuir a nuestra comunidad. 😊",
            "Selecciona una de las opciones.",
            ["btnOpt1", "1️⃣. Informacion"],
            ["btnOpt2", "2️⃣. Solicitud"],
            ["btnOpt3", "3️⃣. Consulta"]
        ]
    },
    "11t": {
        "type": "text",
        "content": [
            "El programa ‘100 Jueves de Acción por el Bien Común’ busca mejorar los espacios públicos a través de acciones como deshierbe, limpieza de aceras y cunetas. ¡Participa haciendo una solicitud!",
        ]
    },
    "11b": {
        "type": "button",
        "content": [
            "¿Te gustaría hacer una solicitud para mejorar tu entorno?",
            "Selecciona una de las opciones.",
            ["btnOpt1", "1️⃣. Hacer solicitud"],
            ["btnOpt2", "2️⃣. No, gracias."],
            ["btnOpt3", "3️⃣. Otra Consulta"]
        ]
    },
    "112": { 
        "type": "text", 
        "content": ["Gracias por tu interés en los '100 Jueves de Acción por el Bien Común'. ¡Hasta pronto!"] 
    },
    "113": { 
        "type": "text", 
        "content": ["Para consultas generales, por favor, comunícate con nuestra línea gratuita al 155. ¡Estamos para ayudarte!"] 
    },
    "12": { 
        "type": "text", 
        "content": ["Por favor, ingresa tu Cédula de Identidad (C.I.) para continuar."] 
    },
    "1211": {
        "type": "button",
        "content": [
            "¡Gracias, [Nombre]! Ahora, elige una de las siguientes acciones para llevar a cabo",
            "Selecciona una de las opciones.",
            ["btnOpt1", "1️⃣. Deshierbe"],
            ["btnOpt2", "2️⃣. Limp. Aceras"],
            ["btnOpt3", "3️⃣. Limp. Cunetas"]
        ]
    },
    "12111": { 
        "type": "text", 
        "content": ["¡Genial, deshierbar es una excelente manera de embellecer nuestra comunidad!"] 
    },
    "12112": { 
        "type": "text", 
        "content": ["¡Perfecto, mantener las aceras limpias es crucial para una ciudad segura y acogedora!"] 
    },
    "12113": { 
        "type": "text", 
        "content": ["¡Excelente, limpiar las cunetas ayuda a prevenir inundaciones y a mantener nuestras calles en buen estado!"] 
    },
    "121111": { 
        "type": "text", 
        "content": ["¿Dónde te gustaría que realizáramos esta acción? Por favor, describe la ubicación del lugar con la mayor precisión posible (por ejemplo, Zona y calle/avenida.)"] 
    },
    "1211111": {
        "type": "button",
        "content": [
            "Si tienes alguna fotografía o video del lugar, sería genial que los compartas con nosotros para que podamos entender mejor la situación.",
            "Selecciona una de las opciones.",
            ["btnOpt1", "1️⃣. Enviar Foto/Video"],
            ["btnOpt2", "2️⃣. No enviar"]
        ]
    },
    "12111111": { 
        "type": "text", 
        "content": ["¡Perfecto! [Nombre] aquí tienes un resumen de tu solicitud:\n\n ● Acción solicitada: [Deshierbe, limpieza de aceras o cunetas]\n ● C.I.: [Número]\n ● Nombre: [Nombre del ciudadano]\n ● Ubicación: [Dirección ingresada]\n ● Foto: [Imagen adjunta/Sin imagen adjunta]"] 
    },
    "1212": {
        "type": "button",
        "content": [
            "No encontramos tu C.I. en nuestros registros. ¿Te gustaría registrarte?",
            "Selecciona una de las opciones.",
            ["btnOpt1", "1️⃣. Sí, registrar"],
            ["btnOpt2", "2️⃣. No, gracias"]
        ]
    },
    "12121": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Apellido Paterno"] 
    },
    "121211": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Apellido Materno"] 
    },
    "1212111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Nombres"] 
    },
    "12121111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Correo Electronico"] 
    },
    "121211111": { 
        "type": "text", 
        "content": ["¡Listo! Ahora continuemos con tu solicitud."] 
    },
    "122": { 
        "type": "text", 
        "content": ["Por favor ingresa un Cédula de Identidad (C.I.) valido y sin extension."] 
    },
    "13": { 
        "type": "text", 
        "content": ["Para consultas generales, por favor, comunícate con nuestra línea gratuita al 155. ¡Estamos para ayudarte!"] 
    }
}

reducedMessageCodes = {
    "111": "12",
    "122": "12",
    "12122": "112",
    "1212111111": "1211",
    "113": "13",
}

specialMessageCodes = [
    "1",
    "11",
    "1211",
    "12111",
    "12112",
    "12113"
]
# ======= ======= ======= ======= =======
# ======= ======= ======= FUNCTIOS SECTIONS ======= ======= =======
def is_json(string):
    try:
        json.loads(string)
        return True
    except ValueError:
        return False
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
# ======= ======= ======= ======== ======= ======= =======
number = ""
ci = ""
name = ""
lastName1 = ""
lastName2 = ""
reqAction = ""
location = ""
media = ""

flowMessageCode = ""
# ======= ======= ======= RECEIVE MESSAGE FUNCTION ======= ======= =======
def recibir_mensaje(req):
    global flowMessageCode

    global name
    global lastName1
    global lastName2

    try:
        req = request.get_json()

        entry = req["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        objeto_mensaje = value["messages"]
    
        app.logger.debug("PRE MESSAGE CODE: "+flowMessageCode)

        if(objeto_mensaje):
            messages = objeto_mensaje[0]
            if("type" in messages):
                numero = messages["from"]
                tipo = messages["type"]
                #addMessage(json.dumps(messages))

                if(flowMessageCode=="12"):
                    text = messages["text"]["body"]
                    if((len(text) <= 12) and (text.isdigit())):
                        flowMessageCode = flowMessageCode+"1"

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
                                app.logger.debug("TOKEN GETTED")
                                data = response.read().decode('utf-8')
                                json_data = json.loads(data)
                                gamlpToken = json_data["token"]

                                try:
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
                                        app.logger.debug("CI RESP")
                                        data = response.read().decode('utf-8')
                                        if(is_json(data)):
                                            app.logger.debug("VALID CI")
                                            json_data = json.loads(data)
                                            flowMessageCode = flowMessageCode+"1"
                                            
                                            name = json_data["success"]["nombres"]
                                            lastName1 = json_data["success"]["paterno"]
                                            lastName2 = json_data["success"]["materno"]
                                        else:
                                            flowMessageCode = flowMessageCode+"2"        
                                    else:
                                        flowMessageCode = flowMessageCode+"2"
                                except Exception as e:
                                    flowMessageCode = flowMessageCode+"2"
                                    app.logger.error(f"Error en el envío de mensaje: {str(e)}")
                            else:
                                flowMessageCode = flowMessageCode+"2"
                                print(f"Error en la solicitud: {response.status} {response.reason}")
                        except Exception as e:
                            flowMessageCode = flowMessageCode+"2"
                            app.logger.error(f"Error en el envío de mensaje: {str(e)}")
                            #addMessageLog(json.dumps(e))
                        finally:
                            connection.close()

                    else:
                        flowMessageCode = flowMessageCode+"2"

                elif(tipo == "interactive"):
                    text = messages["interactive"]["button_reply"]["id"]
                    flowMessageCode = flowMessageCode+text[-1]

                elif("text" in messages):
                    text = messages["text"]["body"]
                    flowMessageCode = flowMessageCode+"1"

                enviar_mensajes_whatsapp(text, numero)

        return jsonify({'message':'EVENT RECEIVED'})

    except Exception as e:
        app.logger.debug('Error: Recibir mensaje')
        return jsonify({'message':'EVENT RECEIVED'})
# ======= ======= ======= ======= ======= ======= =======
# ======= ======= ======= SEND MESSAGE FUNCTION ======= ======= =======
def enviar_mensajes_whatsapp(texto, numero):
    global metaToken
    global metaDomain
    global metaPath

    global chatbotMessages
    global specialMessageCodes
    global flowMessageCode

    global name
    global lastName1
    global lastName2

    dataList = []
    flowMessageCode = reduceMessageCode(flowMessageCode)
    app.logger.debug("POST MESSAGE CODE: "+flowMessageCode)

    # ======= ======= PROCESSING MESSAGE ======= =======
    headers = {
        "Content-Type" : "application/json",
        "Authorization": "Bearer "+metaToken
    }
    data = generateMessageData(numero, chatbotMessages, "processing")
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
        flowMessageCode = "1"
        data = generateMessageData(numero, chatbotMessages, "cancel")
        dataList.append(data)
    # ======= ======= ======= ======= =======
    # ======= ======= TEST MESSAGE ======= =======
    if(("test") in (texto.lower())):
        data = generateMessageData(numero, chatbotMessages, "test")
        dataList.append(data)
    # ======= ======= ======= ======= =======
    # ======= ======= RECUPERAR CIUDADANO INFO SECTION ======= =======
    elif("consulta" in (texto.lower())):
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

                nombres = "Default"

                try:
                    dataGetCiudadano = {
                        "ci": "6834512"
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
                        json_data = json.loads(data)
                        nombres = json_data["success"]["nombres"]+" "+json_data["success"]["paterno"]+" "+json_data["success"]["materno"]
        
                        data = {
                            "messaging_product": "whatsapp",    
                            "recipient_type": "individual",
                            "to": numero,
                            "type": "text",
                            "text": {
                                "preview_url": False,
                                "body": nombres
                            }
                        }
                        dataList.append(data)

                except Exception as e:
                    app.logger.error(f"Error en el envío de mensaje: {str(e)}")
            else:
                print(f"Error en la solicitud: {response.status} {response.reason}")
        except Exception as e:
            app.logger.error(f"Error en el envío de mensaje: {str(e)}")
            #addMessageLog(json.dumps(e))
        finally:
            connection.close()
    # ======= ======= ======= ======= =======
    # ======= ======= SEND COMMOND FORMAT MESSAGE ======= =======
    elif( flowMessageCode not in specialMessageCodes ):
        data = generateMessageData(numero, chatbotMessages, flowMessageCode)
        dataList.append(data)
    # ======= ======= ======= ======= =======
    # ======= ======= SPECIAL MESSAGES ======= =======
    elif( flowMessageCode=="1" ):
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
                "to": numero,
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
        data = generateMessageData(numero, chatbotMessages, flowMessageCode)
        dataList.append(data)

    elif( flowMessageCode=="11" ):
        data = generateMessageData(numero, chatbotMessages, flowMessageCode+"t")
        dataList.append(data)
        data = generateMessageData(numero, chatbotMessages, flowMessageCode+"b")
        dataList.append(data)

    elif( flowMessageCode=="1211" ):
        customText = chatbotMessages[flowMessageCode]["content"][0]
        fullName = name+" "+lastName1+" "+lastName2
        customText = customText.replace("[Nombre]", fullName)

        data = generateMessageData(numero, chatbotMessages, flowMessageCode, customText)
        dataList.append(data)

    elif( (flowMessageCode=="12111") or (flowMessageCode=="12112") or (flowMessageCode=="12113") ):
        data = generateMessageData(numero, chatbotMessages, flowMessageCode)
        dataList.append(data)
        flowMessageCode = flowMessageCode+"1"
        data = generateMessageData(numero, chatbotMessages, flowMessageCode)
        dataList.append(data)
        
    # ======= ======= ======= ======= =======
    # ======= ======= ======= ======= =======
    else:
        data = generateMessageData(numero, chatbotMessages, "invalid")
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
    app.run(host='0.0.0.0',port=80,debug=True)
    """
    data = [
        ['Nombre', 'Edad', 'Ciudad'],
        ['Alice', 30, 'Nueva York'],
        ['Bob', 25, 'Los Ángeles'],
        ['Charlie', 35, 'Chicago']
    ]

    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_excel('datos.xlsx', index=False)
    """
# ======= ======= ======= ======= ======= ======= =======
