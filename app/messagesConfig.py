# ======= ======= MESSAGES DICTIONARY BY CODE ======= =======
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
            "❌. Parece que la información ingresada no es válida. Por favor, asegúrate de proporcionar datos correctos."
        ] 
    },
    "invalidNom": { 
        "type": "text", 
        "content": [
            "❌. Por favor, ingresa un nombre válido. Solo se admiten letras."
        ] 
    },
    "invalidPat": { 
        "type": "text", 
        "content": [
            "❌. Por favor, ingresa un apellido paterno válido. Solo se admiten letras."
        ] 
    },
    "invalidMat": { 
        "type": "text", 
        "content": [
            "❌. Por favor, ingresa un apellido materno válido. Solo se admiten letras."
        ] 
    },
    "invalidEmail": { 
        "type": "text", 
        "content": [
            "❌. Por favor, ingresa un correo electrónico válido. Asegúrate de que tenga un formato correcto (por ejemplo, usuario@dominio.com)."
        ] 
    },
    "conversationOut": { 
        "type": "text", 
        "content": [
            "❌. Estoy aquí para ayudarte, pero parece que hemos recibido información incorrecta varias veces. Si no puedes continuar, te sugiero que nos llames al 155 para más ayuda"
        ] 
    },
    "cancel": { 
        "type": "text", 
        "content": ["❌. Operacion cancelada, volviendo al menu."] 
    },
    "timeout": { 
        "type": "text", 
        "content": ["❌. Tiempo de respuesta expirado, operacion cancelada."] 
    },
    "0": {
        "type": "button",
        "content": [
            "¡Hola! Bienvenido/a ATENAS MARIN al proyecto “100 jueves de Acción por el Bien Común”. ¿En qué puedo ayudarte hoy?",
            "Selecciona una de las opciones.",
            ["btnOpt01", "Hacer una solicitud"],
            ["btnOpt02", "Hacer seguimiento"]
        ]
    },
    "1": {
        "type": "button",
        "content": [
            "¡Hola! Bienvenido/a al proyecto 100 jueves de Acción por el Bien Común. Estoy aquí para ayudarte a contribuir a nuestra comunidad. 😊",
            "Selecciona una de las opciones.",
            ["btnOpt11", "Saber del programa"],
            ["btnOpt12", "Hacer solicitud"],
            ["btnOpt13", "Otra consulta"]
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
            ["btnOpt21", "Hacer solicitud"],
            ["btnOpt22", "No, gracias."],
            ["btnOpt23", "Otra Consulta"]
        ]
    },
    "112": { 
        "type": "text", 
        "content": ["Gracias por tu interés en los '100 Jueves de Acción por el Bien Común'. ¡Hasta pronto!"] 
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
            ["btnOpt31", "Deshierbe"],
            ["btnOpt32", "Limpieza de Aceras"],
            ["btnOpt33", "Limpieza de Cunetas"]
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
            "Para ayudarnos a identificar el lugar exacto, ¿podrías compartirnos la ubicación georreferenciada del sitio?",
            "Selecciona una de las opciones.",
            ["btnOpt41", "Enviar Ubicacion"],
            ["btnOpt42", "No tengo ubicacion"]
        ]
    },
    "12111111": { 
        "type": "location_request_message", 
        "content": ["Por favor, envíenos la ubicacion georeferenciada presionando el siguiente boton."] 
    },
    "121111111": {
        "type": "button",
        "content": [
            "Si tienes alguna fotografía o video del lugar, sería genial que los compartas con nosotros para que podamos entender mejor la situación.",
            "Selecciona una de las opciones.",
            ["btnOpt51", "Enviar fotografia"],
            ["btnOpt52", "No tengo fotografias"]
        ]
    },
    "1211111111": { 
        "type": "text", 
        "content": ["Por favor, envíenos la foto o video."] 
    },
    "12111111111": { 
        "type": "text", 
        "content": ["¡Perfecto! [Nombre] aquí tienes un resumen de tu solicitud:\n\n ● Acción solicitada: [Accion]\n ● C.I.: [Numero]\n ● Nombre: [Nombre]\n ● Ubicación: [Ubicacion]\n ● Foto: [Imagen]"] 
    },
    "1212": {
        "type": "button",
        "content": [
            "No encontramos tu C.I. en nuestros registros. ¿Te gustaría registrarte?",
            "Selecciona una de las opciones.",
            ["btnOpt61", "Sí, registrar"],
            ["btnOpt62", "No, gracias"]
        ]
    },
    "12121": { 
        "type": "list", 
        "content": [
            "Por favor, ingresa los siguientes datos para registrarte.\n\n Expedido",
            "Selecciona una de las opciones.",
            "Ver extenciones.",
            ["LPZ1", "LPZ", "Expedido en La Paz"],
            ["CBB1", "CBB", "Expedido en Cochabamba"],
            ["SCZ1", "SCZ", "Expedido en Santa Cruz"],
            ["CHQ1", "CHQ", "Expedido en Chuquisaca"],
            ["TJA1", "TJA", "Expedido en Tarija"],
            ["PTS1", "PTS", "Expedido en Potosí"],
            ["ORU1", "ORU", "Expedido en Oruro"],
            ["BNI1", "BNI", "Expedido en Beni"],
            ["PND1", "PND", "Expedido en Pando"]
        ]
    },
    "121211": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Apellido Paterno"] 
    },
    "1212111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Apellido Materno"] 
    },
    "12121111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Nombres"] 
    },
    "121211111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Correo Electronico"] 
    },
    "1212111111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Contraseaña a utilizar"] 
    },
    "12121111111": { 
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
# ======= ======= ======= ======= =======
# ======= ======= REDUCED MESSAGES EQUIVALENCE ======= =======
reducedMessageCodes = {
    "111": "12",
    "122": "12",
    "12122": "112",
    "12111112":"121111111",
    "1211111112":"12111111111",
    "12121111111": "1211",
    "12121111112": "112",
    "113": "13"
}
# ======= ======= ======= ======= =======
# ======= ======= MESSAGES WHIT SPECIAL ANSWERS ======= =======
specialMessageCodes = [
    "1",
    "11",
    "1211",
    "12111",
    "12112",
    "12113",
    "12121111111",
    "12111111111"
]
# ======= ======= ======= ======= =======
# ======= ======= MESSAGES WHIT SPECIAL ANSWERS ======= =======
endConversationMessages = [
    "13",
    "112",
    "12111111111"
]
# ======= ======= ======= ======= =======
# ======= ======= MESSAGES SPECTED ANSWERS ======= =======
messagesExpectedAnswer = {
    "text" : "text",
    "button" : "button_reply",
    "list" : "list_reply",
    "location_request_message" : "location",
}
# ======= ======= ======= ======= =======
