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

metaToken = "EAAWXJp8ZCZCyABO4kxNUBkBqomYIYojJ42HwYvhOVg5LCvlP77UHkXeDLsDC2ICChMKOucGgYfgkChPuLQOQZA0coGVBkFji9CT52cmCJoMzb2za68GiHZBGLEKZAqeOY5MLGy907zpDcNxoy8yHaJTIURqr1tnml3ZB1A9xpkb3VQfbZB6oTu7ZCQOlqSPGuNxH1OqNgQfjegZC6EIHXEdAGP16CDwZDZD"
webhookToken = "CHATBOTTOKENTEST"

metaDomain = "graph.facebook.com"
metaPath = "/v20.0/374877792366425/messages"

blogDomain = "lapaz.bo"
blogPath = "/wp-json/catastroPlugin/v1/posts-categoria/catastroChatbot"

logging.basicConfig(level=logging.DEBUG)

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
blogLastPost = []

conn = http.client.HTTPSConnection(blogDomain)
conn.request("GET", blogPath)
response = conn.getresponse()
if(response.status == 200):
    data = response.read().decode('utf-8')
    json_data = json.loads(data)
    blogLastPost = json_data[0]
else:
    print(f"Error en la solicitud: {response.status} {response.reason}")
conn.close()

flow0 = [
    (blogLastPost["title"]+"\n"+blogLastPost["date"]+"\n"+blogLastPost["link"]),
    blogLastPost["featured_image"]
]

flow1 = [
    "¡Hola! Bienvenido/a al proyecto “100 jueves de Acción por el Bien Común”. Estoy aquí para ayudarte a contribuir a nuestra comunidad. 😊",
    "Selecciona una de las opciones.",
    [
        "btnOpt1",
        "1️⃣. Quiero saber más sobre el programa"
    ],
    [
        "btnOpt2",
        "2️⃣. Quiero hacer una solicitud"
    ],
    [
        "btnOpt3",
        "3️⃣. Tengo otra consulta"
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
    global flowStep

    app.logger.debug(texto)
    app.logger.debug(flowStep)

    if(("test") in (texto.lower())):
        flowStep = 1
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
    # ======= ======= ======= ENVIAR IMAGEN BLOG ======= ======= =======
    elif(("hola" in (texto.lower()))and(flowStep==0)):
        
        dataBlog = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": numero,
            "type": "image",
            "image": {
                "id" : "img1", 
                "link": "https://lapaz.bo/wp-content/uploads/2024/08/ccc0.png", 
                "caption": "Horarios de atención  Plataformas de la ACM"
            }
        }
        headersBlog = {
            "Content-Type" : "application/json",
            "Authorization": "Bearer "+metaToken
        }
        connection = http.client.HTTPSConnection(metaDomain)
        try:
            connection.request("POST", metaPath, dataBlog, headersBlog)
            response = connection.getresponse()
            print(response.status, response.reason)
        except Exception as e:
            addMessageLog(json.dumps(e))
        finally:
            connection.close()

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
                        }
                    ]                    
                }                
            }
        }
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

    data = json.dumps(data)
    headers = {
        "Content-Type" : "application/json",
        "Authorization": "Bearer "+metaToken
    }

    connection = http.client.HTTPSConnection("graph.facebook.com")
    try:
        connection.request("POST", "/v20.0/374877792366425/messages", data, headers)
        response = connection.getresponse()
        print(response.status, response.reason)
    except Exception as e:
        addMessageLog(json.dumps(e))
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
