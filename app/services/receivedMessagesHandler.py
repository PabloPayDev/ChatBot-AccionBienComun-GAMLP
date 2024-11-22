# ======= ======= ======== RECEIVED MESSAGES HANDLER ======= ======= =======
# THIS FILE IS WHERE IS LOCATED ALL THE FUNCTIONS THAT HELP IN
# THA DATA PROCESS
# ======= ======= ======== ======= ======= ======= =======
from flask import jsonify, request, current_app
from datetime import datetime
import base64
import http.client
import urllib.request
import json
import os

from ..helpers import create_new_session_user, reduceMessageCode
from .sendMessagesHandler import sendMessage

from ..messagesConfig import chatbotMessages, messagesExpectedAnswer

gamlpToken = ""

# ======= ======= ======= RECEIVE MESSAGE FUNCTION ======= ======= =======
def onReceivedMessage(req):
    imageDirPath = current_app.config['IMAGE_DIR_PATH']

    metaToken = current_app.config['META_TOKEN']

    metaDomain = current_app.config['META_DOMAIN']

    gamlpDomain = current_app.config['GAMLP_DOMAIN']
    gamlpPort = current_app.config['GAMLP_PORT']
    gamlpPathGetToken = current_app.config['GAMLP_PATH_GET_TOKEN']
    gamlpPathGetCiudadano = current_app.config['GAMLP_PATH_GET_CIUDADANO']
    gamlpPathCreateCiudadano = current_app.config['GAMLP_PATH_CREATE_CIUDADANO']
    gamlpUser = current_app.config['GAMLP_USER']
    gamlpPass = current_app.config['GAMLP_PASS']

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
                if(phoneNumber not in current_app.config['SESSIONS_STORE']):
                    create_new_session_user(phoneNumber)

                phoneNumberData = current_app.config['SESSIONS_STORE'].get(phoneNumber, None)

                current_app.logger.debug("============")
                current_app.logger.debug("PRE MESSAGE CODE: "+phoneNumberData["flowMessageCode"])
                current_app.logger.debug("============")
                
                # ======= SPECIAL MESSAGES SECTION SECTIONS =======

                # ======= ======= =======
                # ======= VALIDATION SECTIONS =======
                phoneNumberData["specialMessage"] = ""
                if(phoneNumberData["flowMessageCode"]):
                    tipoFormated = (tipo) if(tipo != "interactive") else(messages["interactive"]["type"])
                    if( (phoneNumberData["flowMessageCode"] == "1211111111") and (tipoFormated == "image")):
                        current_app.logger.debug("===== EXPECTED =====")
                    elif(tipoFormated == messagesExpectedAnswer[chatbotMessages[phoneNumberData["flowMessageCode"]]["type"]]):
                        current_app.logger.debug("===== EXPECTED =====")
                    else:
                        current_app.logger.debug("====== UNEXPECTED ====")
                        phoneNumberData["invalidMessageCount"] += 1
                        phoneNumberData["specialMessage"] = "invalid"
                        text = ""

                # ======= ======= =======
                if(phoneNumberData["specialMessage"] != "invalid"):
                    # ======= SAVING SPECIAL DATA SENDED =======
                    if( phoneNumberData["flowMessageCode"]=="1211" ):
                        text = messages["interactive"]["button_reply"]["id"]
                        phoneNumberData["reqAction"] = "Deshierbe" if (text[-1] == "1") else (phoneNumberData["reqAction"])
                        phoneNumberData["reqAction"] = "Limpieza de aceras" if (text[-1] == "2") else (phoneNumberData["reqAction"])
                        phoneNumberData["reqAction"] = "Limpieza de cunetas" if (text[-1] == "3") else (phoneNumberData["reqAction"])

                    elif( phoneNumberData["flowMessageCode"]=="121111" ):
                        text = messages["text"]["body"]
                        phoneNumberData["location"] = text

                    elif( phoneNumberData["flowMessageCode"]=="12111111" ):
                        phoneNumberData["latitude"] = messages["location"]["latitude"]
                        phoneNumberData["longitude"] = messages["location"]["longitude"]

                    elif( phoneNumberData["flowMessageCode"]=="121111111" ):
                        text = messages["interactive"]["button_reply"]["id"]
                        phoneNumberData["media"] = "Imagen enviada" if (text[-1] == "1") else (phoneNumberData["media"])
                        phoneNumberData["media"] = "Sin imagen" if (text[-1] == "2") else (phoneNumberData["media"])

                    elif( phoneNumberData["flowMessageCode"]=="1211111111" ):
                        imageId = messages["image"]['id']
                        imageUrl = "/v20.0/"+imageId
                        if not os.path.exists(imageDirPath):
                            os.makedirs(imageDirPath)
                        conn = http.client.HTTPSConnection(metaDomain)
                        headers = {
                            "Authorization": "Bearer "+metaToken
                        }
                        conn.request("GET", imageUrl, headers=headers)
                        response = conn.getresponse()
                        if(response.status == 200):
                            imageData = json.loads(response.read())
                            imageDataUrl = imageData["url"]
                            file_path = os.path.join(imageDirPath, imageId+'.jpg')
                            try:
                                requestImg = urllib.request.Request(imageDataUrl, headers=headers)
                                with urllib.request.urlopen(requestImg) as responseImg:
                                    imageRes = responseImg.read()
                                    with open(file_path, 'wb') as f:
                                        f.write(imageRes)
                                        phoneNumberData["mediaId"] = imageDirPath+'/'+imageId+'.jpg'
                            except Exception as e:
                                print(f"Download image error: {str(e)}")
                        else:
                            current_app.logger.debug(imageUrl)
                            print(f"Getting image error: {response.status} - {response.reason}")

                    elif( phoneNumberData["flowMessageCode"]=="12121" ):
                        text = messages["interactive"]["list_reply"]["id"][:-1]
                        phoneNumberData["issued"] = text

                    elif( phoneNumberData["flowMessageCode"]=="121211" ):
                        text = messages["text"]["body"]
                        phoneNumberData["lastName1"] = text

                    elif( phoneNumberData["flowMessageCode"]=="1212111" ):
                        text = messages["text"]["body"]
                        phoneNumberData["lastName2"] = text

                    elif( phoneNumberData["flowMessageCode"]=="12121111" ):
                        text = messages["text"]["body"]
                        phoneNumberData["name"] = text

                    elif( phoneNumberData["flowMessageCode"]=="121211111" ):
                        text = messages["text"]["body"]
                        phoneNumberData["email"] = text

                    elif( phoneNumberData["flowMessageCode"]=="1212111111" ):
                        text = messages["text"]["body"]
                        phoneNumberData["password"] = text
                    # ======= ======= =======
                    # ======= CURRENT FLOW MESSAGE UPDATE =======
                    if( phoneNumberData["flowMessageCode"]=="12" ):
                        text = messages["text"]["body"]
                        phoneNumberData["ci"] = text
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

                                    headers = {
                                        "Content-Type" : "application/json",
                                        "Authorization": "Bearer "+gamlpToken
                                    }
                                    dataGetCiudadano = {
                                        "ci": text
                                    }
                                    dataGetCiudadano = json.dumps(dataGetCiudadano)
                                    connection.request("POST", gamlpPathGetCiudadano, dataGetCiudadano, headers)
                                    response = connection.getresponse()
                                    if(response.status == 200):
                                        data = response.read().decode('utf-8')
                                        if("success" in data):
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
                                current_app.logger.error(f"Error en el envío de mensaje: {str(e)}")
                            finally:
                                connection.close()

                        else:
                            phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"
                    
                    elif( phoneNumberData["flowMessageCode"]=="1212111111" ):
                        text = messages["text"]["body"]
                        auth = f"gamlpforo:g4m4lpf0r0of2022"
                        auth_bytes = auth.encode('utf-8')
                        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
                        headers = {
                            "Content-Type" : "application/json",
                            "Authorization": f"Basic {auth_base64}"
                        }
                        data = {
                            "ci":phoneNumberData["ci"],
                            "expedido":phoneNumberData["issued"],
                            "nombres":phoneNumberData["name"],
                            "paterno":phoneNumberData["lastName1"],
                            "materno":phoneNumberData["lastName2"],
                            "telefono":"",
                            "movil":phoneNumber,
                            "correo":phoneNumberData["email"],
                            "sistema":"WEB_FORO",
                            "contrasenia":phoneNumberData["password"]
                        }
                        data = json.dumps(data)
                        connection = http.client.HTTPConnection(gamlpDomain, gamlpPort)
                        try:
                            connection.request("POST", gamlpPathCreateCiudadano, data, headers)
                            response = connection.getresponse()
                            if(response.status == 200):
                                response = response.read().decode('utf-8')
                                response = json.loads(response)
                                if( "success" in response):
                                    phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"1"
                                else:
                                    phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"
                            else:
                                phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"

                        except Exception as e:
                            phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"2"
                            current_app.logger.error(f"Error en el envío de mensaje: {str(e)}")

                    elif(tipo == "interactive"):
                        tipo_interactivo = messages["interactive"]["type"]
                        text = messages["interactive"][tipo_interactivo]["id"]
                        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+text[-1]

                    elif(tipo == "location"):
                        text = ""
                        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"1"

                    elif(tipo == "image"):
                        text = ""
                        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"1"

                    elif("text" in messages):
                        text = messages["text"]["body"]
                        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"1"
                    # ======= ======= =======
                # ======= UPDATE FLOW MESSAGE CODE =======
                phoneNumberData["flowMessageCode"] = reduceMessageCode(phoneNumberData["flowMessageCode"])
                current_app.logger.debug("============")
                current_app.logger.debug("POST MESSAGE CODE: "+phoneNumberData["flowMessageCode"])
                current_app.logger.debug("============")
                # ======= ======= =======
                # ======= UPDATE DATA IN REDIS =======
                phoneNumberData["lastAnswerDatetime"] = datetime.now()
                current_app.config['SESSIONS_STORE'][phoneNumber] = phoneNumberData
                # ======= ======= =======

                sendMessage(text, phoneNumber)

        return jsonify({'message':'EVENT RECEIVED'})

    except Exception as e:
        current_app.logger.debug(e)
        return jsonify({'message':'EVENT RECEIVED'})
# ======= ======= ======= ======= ======= ======= =======