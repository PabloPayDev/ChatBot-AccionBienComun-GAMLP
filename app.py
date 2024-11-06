from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
from datetime import datetime
import http.client
import ssl
import json
import logging

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['meta_db_100J']

metaToken = "EAAWXJp8ZCZCyABO1c4XBjpfadxepyGEOQoT6MZALqxqrxPFq8JC92GvQjDKt0A9pBpHBWSxGcSkqqIAZB3FW7HeC1Lw0ts6jbw9vXJo3TZCwn0dHZA6a3uBnoeecCBlXUA8bZBZA6E8btx7aKToA0wVrhD11VyMu2bgJswN3Xj7umJNpJzHe7mROoztZBoZC7a8oHkNOmXsxk4IULPGVP1yxd5CUTt"
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
messageProcessing = { 
    "type": "text", 
    "content": [
        "⏰. Procesando..."
    ] 
}
messageInvalid = { 
    "type": "text", 
    "content": [
        "Parece que la información ingresada no es válida. Por favor, asegúrate de proporcionar datos correctos.",
        "Estoy aquí para ayudarte, pero parece que hemos recibido información incorrecta varias veces. Si no puedes continuar, te sugiero que nos llames al 155 para más ayuda"
    ] 
}
message001 = {
    "type": "button",
    "content": [
        "¡Hola! Bienvenido/a al proyecto 100 jueves de Acción por el Bien Común. Estoy aquí para ayudarte a contribuir a nuestra comunidad. 😊",
        "Selecciona una de las opciones.",
        ["btnOpt1", "1️⃣. Informacion"],
        ["btnOpt2", "2️⃣. Solicitud"],
        ["btnOpt3", "3️⃣. Consulta"]
    ]
}
message002 = {
    "type": "button",
    "content": [
        "El programa ‘100 Jueves de Acción por el Bien Común’ busca mejorar los espacios públicos a través de acciones como deshierbe, limpieza de aceras y cunetas. ¡Participa haciendo una solicitud!",
        "¿Te gustaría hacer una solicitud para mejorar tu entorno?",
        "Selecciona una de las opciones.",
        ["btnOpt1", "1️⃣. Hacer solicitud"],
        ["btnOpt2", "2️⃣. No, gracias."],
        ["btnOpt3", "3️⃣. Otra Consulta"]
    ]
}
message003 = { 
    "type": "text", 
    "content": ["Gracias por tu interés en los '100 Jueves de Acción por el Bien Común'. ¡Hasta pronto!"] 
}
message004 = { 
    "type": "text", 
    "content": ["Para consultas generales, por favor, comunícate con nuestra línea gratuita al 155. ¡Estamos para ayudarte!"] 
}
message005 = { 
    "type": "text", 
    "content": ["Por favor, ingresa tu Cédula de Identidad (C.I.) para continuar."] 
}
message006 = { 
    "type": "text", 
    "content": ["Por favor ingresa un Cédula de Identidad (C.I.) valido y sin extension."] 
}
message007 = {
    "type": "button",
    "content": [
        "¡Gracias! Ahora, elige una de las siguientes acciones para llevar a cabo",
        "Selecciona una de las opciones.",
        ["btnOpt1", "1️⃣. Deshierbe"],
        ["btnOpt2", "2️⃣. Limp. Aceras"],
        ["btnOpt3", "3️⃣. Limp. Cunetas"]
    ]
}
message008 = { 
    "type": "text", 
    "content": ["¡Genial, deshierbar es una excelente manera de embellecer nuestra comunidad!"] 
}
message009 = { 
    "type": "text", 
    "content": ["¡Perfecto, mantener las aceras limpias es crucial para una ciudad segura y acogedora!"] 
    }
message010 = { 
    "type": "text", 
    "content": ["¡Excelente, limpiar las cunetas ayuda a prevenir inundaciones y a mantener nuestras calles en buen estado!"] 
}
message011 = { 
    "type": "text", 
    "content": ["¿Dónde te gustaría que realizáramos esta acción? Por favor, describe la ubicación del lugar con la mayor precisión posible (por ejemplo, Zona y calle/avenida.)"] 
}
message012 = {
    "type": "button",
    "content": [
        "Si tienes alguna fotografía o video del lugar, sería genial que los compartas con nosotros para que podamos entender mejor la situación.",
        "Selecciona una de las opciones.",
        ["btnOpt1", "1️⃣. Enviar Foto/Video"],
        ["btnOpt2", "2️⃣. No enviar"]
    ]
}
message013 = { 
    "type": "text", 
    "content": ["¡Perfecto! [Nombre del ciudadano] aquí tienes un resumen de tu solicitud:\n\n ● Acción solicitada: [Deshierbe, limpieza de aceras o cunetas]\n ● C.I.: [Número]\n ● Nombre: [Nombre del ciudadano]\n ● Ubicación: [Dirección ingresada]\n ● Foto: [Imagen adjunta/Sin imagen adjunta]"] 
}
message014 = {
    "type": "button",
    "content": [
        "No encontramos tu C.I. en nuestros registros. ¿Te gustaría registrarte?",
        "Selecciona una de las opciones.",
        ["btnOpt1", "1️⃣. Sí, registrar"],
        ["btnOpt2", "2️⃣. No, gracias"]
    ]
}
message015 = { 
    "type": "text", 
    "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Apellido Paterno"] 
}
message016 = { 
    "type": "text", 
    "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Apellido Materno"] 
}
message017 = { 
    "type": "text", 
    "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Nombres"] 
}
message018 = { 
    "type": "text", 
    "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Correo Electronico"] 
}
message019 = { 
    "type": "text", 
    "content": ["¡Listo! Ahora continuemos con tu solicitud."] 
}
message020 = { 
    "type": "text", 
    "content": ["Para consultas generales, por favor, comunícate con nuestra línea gratuita al 155. ¡Estamos para ayudarte!"] 
}

# SAME CODES 12=111, 112=12122, 1211=1212111111, 13=113
chatbotMessages = {
    "processing": messageProcessing,
    "invalid": messageInvalid,
    "1": message001,
    "11": message002,
    "112": message003,
    "113": message004,
    "12": message005,
    "1211": message007,
    "12111": message008,
    "12112": message009,
    "12113": message010,
    "121111": message011,
    "1211111": message012,
    "12111111": message013,
    "1212": message014,
    "12121": message015,
    "121211": message016,
    "1212111": message017,
    "12121111": message018,
    "121211111": message019,
    "122": message006,
    "13": message020,
}
# ======= ======= ======= ======= =======
# ======= ======= ======= SOME FUNCTIONS SECTION ======= ======= =======
def json_serializer(data):
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, list):
        return [json_serializer(item) for item in data]
    if isinstance(data, dict):
        return {key: json_serializer(value) for key, value in data.items()}
    return data

def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if(challenge and (token == webhookToken)):
        return challenge
    else:
        return jsonify({'error':'Token Invalido'}),401

flowMessageCode = ""
# ======= ======= ======= RECEIVE MESSAGE FUNCTION ======= ======= =======
def recibir_mensaje(req):
    global flowMessageCode
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
                tipo = messages["type"]
                #addMessage(json.dumps(messages))

                if(tipo == "interactive"):
                    tipo_interactivo = messages["interactive"]["type"]
                    if(tipo_interactivo == "button_reply"):
                        text = messages["interactive"]["button_reply"]["id"]
                        numero = messages["from"]
                        flowMessageCode = flowMessageCode+text[-1]

                        enviar_mensajes_whatsapp(text, numero)

                    if(tipo_interactivo == "list_reply"):
                        text = messages["interactive"]["list_reply"]["id"]
                        numero = messages["from"]

                        enviar_mensajes_whatsapp(text, numero)

                if("text" in messages):
                    text = messages["text"]["body"]
                    numero = messages["from"]
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
    global flowMessageCode

    dataList = []
    app.logger.debug("POST MESSAGE CODE: "+flowMessageCode)

    # ======= ======= PROCESSING MESSAGE ======= =======
    data = {
        "messaging_product": "whatsapp",    
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": "⏰. Procesando..."
        }
    }
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
        app.logger.debug("Error envio mensaje")
    finally:
        connection.close()
    # ======= ======= ======= ======= =======
    # ======= ======= TEST MESSAGE ======= =======
    if(("test") in (texto.lower())):
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Test message"
            }
        }
        dataList.append(data)
    # ======= ======= ======= ======= =======
    # ======= ======= SALUDO BLOG Y BUTTONS INICIALES ======= =======
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
        
    # ======= ======= ======= ======= =======
    # ======= ======= RECUPERAR CIUDADANO INFO SECTION ======= =======
    elif("consulta" in (texto.lower())):
        app.logger.debug('IN')
        data = {
            "usuario": gamlpUser,
            "clave": gamlpPass
        }
        headers = {
            "Content-Type" : "application/json"
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
                        nombres = json_data["success"]["nombres"]+json_data["success"]["paterno"]+json_data["success"]["materno"]
        
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
    # ======= ======= ======= ======= =======
    else:
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": chatbotFlowMessages[5][0]
            }
        }
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
# ======= ======= ======= ======= ======= ======= =======
def generateMessageData(phoneNumber, messageList, messageCode, textIndex=None):
    messageScope = messageList[messageCode]
    messageScopeType = messageScope["type"]
    messageScopeContent = messageScope["content"]

    # ======= DATA DEFINITION =======
    dataToReturn = {
        "messaging_product": "whatsapp",    
        "recipient_type": "individual",
        "to": phoneNumber,
        "type": messageScopeType
    }
    # ======= ======= =======
    # ======= CONTENT DEFINITION =======
    messageContent = {}
    if( messageScopeType == "text" ):
        messageContent = {
            "preview_url": False,
            "body": messageScopeContent[textIndex]
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
            "type": "button",
            "body":{
                "text": messageScopeContent[0]
            },
            "footer":{
                "text": messageScopeContent[1]
            },
            "action":{
                "buttons":buttonsInContent
            }
        }
    # ======= ======= =======
    dataToReturn[messageScopeType] = messageContent
    return dataToReturn

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
