# ======= ======= ======== SEND MESSAGES HANDLER ======= ======= =======
# THIS FILE IS WHERE IS LOCATED ALL THE FUNCTIONS THAT HELP IN
# THA DATA PROCESS
# ======= ======= ======== ======= ======= ======= =======
from flask import current_app
from datetime import date, datetime
import http.client
import json

from ..helpers import generateMessageData, reduceMessageCode

from ..messagesConfig import chatbotMessages
from ..messagesConfig import specialMessageCodes

# ======= ======= ======= SEND MESSAGE FUNCTION ======= ======= =======
def sendMessage(texto, phoneNumber):
    metaToken = current_app.config['META_TOKEN']
    metaDomain = current_app.config['META_DOMAIN']
    metaMessagesPath = current_app.config['META_MESSAGES_PATH']

    blogDomain = current_app.config['BLOG_DOMAIN']
    blogPath = current_app.config['BLOG_PATH']

    db = current_app.config['MONGO_DB']

    global chatbotMessages
    global specialMessageCodes
    
    phoneNumberData = current_app.config['SESSIONS_STORE'].get(phoneNumber, None)

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
        connection.request("POST", metaMessagesPath, data, headers)
        response = connection.getresponse()
    except Exception as e:
        current_app.logger.debug("Error envio mensaje")
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

            dateObj = datetime.strptime(blogLastPost["date"], "%Y-%m-%d %H:%M:%S")
            formatedDate = dateObj.strftime("%A, %d de %B de %Y")
            daysNames = {
                'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 
                'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 
                'Sunday': 'Domingo'
            }
            monthsNames = {
                'January': 'enero', 'February': 'febrero', 'March': 'marzo', 
                'April': 'abril', 'May': 'mayo', 'June': 'junio', 'July': 'julio', 
                'August': 'agosto', 'September': 'septiembre', 'October': 'octubre', 
                'November': 'noviembre', 'December': 'diciembre'
            }
            formatedDate = formatedDate.replace(
                dateObj.strftime("%A"), daysNames[dateObj.strftime("%A")]
            )
            formatedDate = formatedDate.replace(
                dateObj.strftime("%B"), monthsNames[dateObj.strftime("%B")]
            )

            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": phoneNumber,
                "type": "image",
                "image": {
                    "link": blogLastPost["featured_image"], 
                    "caption": blogLastPost["title"]+"\n"+formatedDate+"\n"+blogLastPost["link"]
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
                "ci":phoneNumberData["ci"],
                "reqAction":phoneNumberData["reqAction"],
                "location":phoneNumberData["location"],
                "latitude":phoneNumberData["latitude"],
                "longitude":phoneNumberData["longitude"],
                "mediaId":phoneNumberData["mediaId"],
                "date":datetime.combine(date.today(), datetime.min.time())
            }
            collection = db['data']
            collection.insert_one(newActionRegister)
        except Exception as e:
            current_app.logger.debug("======= ERROR GUARDANDO MENSAJE =======")
            current_app.logger.debug(e)

        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"], customText)
        dataList.append(data)

        phoneNumberData["flowMessageCode"] = ""

    elif( phoneNumberData["flowMessageCode"]=="12121111111"):
        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"])
        dataList.append(data)
        phoneNumberData["flowMessageCode"] = phoneNumberData["flowMessageCode"]+"1"
        phoneNumberData["flowMessageCode"] = reduceMessageCode(phoneNumberData["flowMessageCode"])
        data = generateMessageData(phoneNumber, chatbotMessages, phoneNumberData["flowMessageCode"])
        dataList.append(data)
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
            connection.request("POST", metaMessagesPath, dataItem, headers)
            response = connection.getresponse().read().decode('utf-8')
        except Exception as e:
            current_app.logger.error(f"Error en el envío de mensaje: {str(e)}")
            #addMessageLog(json.dumps(e))
        finally:
            connection.close()
# ======= ======= ======= ======== ======= ======= =======