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

metaToken = "EAAWXJp8ZCZCyABO0RydY5yYIQA6uZBGhJwEbZB7rFcbkOiQA9n89jZB9pnxxGaZB6C1Yau4RkuGLZBT3CYzrNW7ApAZCKKTgjqJc3Q4npVNekcqsbqMEpINY4kxf0OXfQfsWt3cnHSGggWceSwXifV6ZBHOrm0f9IocUWYJZB35xAesZBwSouYInZCuYjxQE0bGZB5WJDIWQk6GSqbJgHjWkoRaUR3acl"
webhookToken = "CHATBOTTOKENTEST"

metaDomain = "graph.facebook.com"
metaPath = "/v20.0/374877792366425/messages"

blogDomain = "lapaz.bo"
blogPath = "/wp-json/catastroPlugin/v1/posts-categoria/catastroChatbot"

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


flow1 = [
    "¡Hola! Bienvenido/a al proyecto 100 jueves de Acción por el Bien Común. Estoy aquí para ayudarte a contribuir a nuestra comunidad. 😊",
    "Selecciona una de las opciones.",
    [
        "btnOpt1",
        "1️⃣. Informacion"
    ],
    [
        "btnOpt2",
        "2️⃣. Solicitud"
    ],
    [
        "btnOpt3",
        "3️⃣. Consulta"
    ]
]
flow2 = [
    "Como fue tu experiencia general en la atencion?",
     "Ver opciones",
     "Selecciona una de las opciones",
    [
        "btnOpt1",
        "1️⃣. Muy mala"
    ],
    [
        "btnOpt2",
        "2️⃣. Mala"
    ],
    [
        "btnOpt3",
        "3️⃣. Media"
    ]
]

flow3 = [
    "El tiempo de espera fue:",
    "Ver opciones",
    "Selecciona una de las opciones",
    [
        "btnOpt1",
        "1️⃣. Muy lento."
    ],
    [
        "btnOpt2",
        "2️⃣. Lento"
    ],
    [
        "btnOpt3",
        "3️⃣. Medio"
    ]
]

flow4 = [
    "Desea agregar una nota sobre su experiencia? \n\n Ej: Buena actitud del operador de plataforma."
]

flow5 = [
    "Gracias por su retroalimentacion",
    [
        "btnOpt1",
        "1️⃣. Finalizar"
    ]
]

flowInvalid = [
    "Su respuesta no es valida, porfavor ingrese lo que se especifica."
]

chatbotFlowMessages = [
    flow1,
    flow2,
    flow3,
    flow4,
    flow5,
    flowInvalid
]
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

def recibir_mensaje(req):
    try:
        req = request.get_json()

        entry = req["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        objeto_mensaje = value["messages"]

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

                        enviar_mensajes_whatsapp(text, numero)

                    if(tipo_interactivo == "list_reply"):
                        text = messages["interactive"]["list_reply"]["id"]
                        numero = messages["from"]

                        enviar_mensajes_whatsapp(text, numero)

                if("text" in messages):
                    text = messages["text"]["body"]
                    numero = messages["from"]

                    enviar_mensajes_whatsapp(text, numero)

        return jsonify({'message':'EVENT RECEIVED'})

    except Exception as e:
        app.logger.debug('Error: Recibir mensaje')
        return jsonify({'message':'EVENT RECEIVED'})
    
flowStep = 0
def enviar_mensajes_whatsapp(texto, numero):
    global metaToken
    global metaDomain
    global metaPath

    global chatbotFlowMessages
    global flowStep

    app.logger.debug(texto)
    app.logger.debug(("test") in (texto.lower()))
    # ======= ======= ======= TEST MESSAGE ======= ======= =======
    if(("test") in (texto.lower())):
        app.logger.debug("In")
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": "Hola, Bienvenido"
            }
        }
    # ======= ======= ======= ======= ======= ======= =======
    # ======= ======= ======= SALUDO BLOG Y BUTTONS INICIALES ======= ======= =======
    elif("hola" in (texto.lower())):
        data = {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": numero,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body":{
                    "text": chatbotFlowMessages[0][0]
                },
                "footer":{
                    "text": chatbotFlowMessages[0][1]
                },
                "action":{
                    "buttons":[
                        {
                            "type": "reply",
                            "reply":{
                                "id": chatbotFlowMessages[0][2][0],
                                "title": chatbotFlowMessages[0][2][1]
                            }
                        },
                        {
                            "type": "reply",
                            "reply":{
                                "id": chatbotFlowMessages[0][3][0],
                                "title": chatbotFlowMessages[0][3][1]
                            }
                        },
                        {
                            "type": "reply",
                            "reply":{
                                "id": chatbotFlowMessages[0][4][0],
                                "title": chatbotFlowMessages[0][4][1]
                            }
                        }
                    ]                    
                }                
            }
        }
    # ======= ======= ======= ======= ======= ======= =======
    # ======= ======= ======= ENVIAR IMAGEN BLOG ======= ======= =======
    elif("img" in (texto.lower())):
        blogLastPost = []

        conn = http.client.HTTPSConnection(blogDomain)
        conn.request("GET", blogPath)
        response = conn.getresponse()
        if(response.status == 200):
            data = response.read().decode('utf-8')
            json_data = json.loads(data)
            blogLastPost = json_data[0]
            app.logger.debug("======= =======")
            app.logger.debug(blogLastPost)
            app.logger.debug("======= =======")
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
        else:
            print(f"Error en la solicitud: {response.status} {response.reason}")
        conn.close()
    # ======= ======= ======= ======= ======= ======= =======
    # ======= ======= ======= ======= ======= ======= =======
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
    # ======= ======= ======= ======= ======= ======= =======

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
        #addMessageLog(json.dumps(e))
    finally:
        connection.close()
# ======= ======= ======= ======= ======= ======= =======
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
