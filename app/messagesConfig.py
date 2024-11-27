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
    "1": {
        "type": "button",
        "content": [
            "¡Hola! Bienvenido/a al proyecto “100 jueves de Acción por el Bien Común”. ¿En qué puedo ayudarte hoy?",
            "Selecciona una de las opciones.",
            ["btnOpt11", "Hacer una solicitud"],
            ["btnOpt12", "Hacer seguimiento"]
        ]
    },
    "11": {
        "type": "button",
        "content": [
            "¡Hola! Bienvenido/a al proyecto 100 jueves de Acción por el Bien Común. Estoy aquí para ayudarte a contribuir a nuestra comunidad. 😊",
            "Selecciona una de las opciones.",
            ["btnOpt21", "Saber del programa"],
            ["btnOpt22", "Hacer solicitud"],
            ["btnOpt23", "Otra consulta"]
        ]
    },
    "111t": {
        "type": "text",
        "content": [
            "El programa ‘100 Jueves de Acción por el Bien Común’ busca mejorar los espacios públicos a través de acciones como deshierbe, limpieza de aceras y cunetas. ¡Participa haciendo una solicitud!",
        ]
    },
    "111b": {
        "type": "button",
        "content": [
            "¿Te gustaría hacer una solicitud para mejorar tu entorno?",
            "Selecciona una de las opciones.",
            ["btnOpt31", "Hacer solicitud"],
            ["btnOpt32", "No, gracias."],
            ["btnOpt33", "Otra Consulta"]
        ]
    },
    "1112": { 
        "type": "text", 
        "content": ["Gracias por tu interés en los '100 Jueves de Acción por el Bien Común'. ¡Hasta pronto!"] 
    },
    "112": { 
        "type": "text", 
        "content": ["Por favor, ingresa tu Cédula de Identidad (C.I.) para continuar."] 
    },
    "11211": {
        "type": "button",
        "content": [
            "¡Gracias, [Nombre]! Ahora, elige una de las siguientes acciones para llevar a cabo",
            "Selecciona una de las opciones.",
            ["btnOpt41", "Deshierbe"],
            ["btnOpt42", "Limpieza de Aceras"],
            ["btnOpt43", "Limpieza de Cunetas"]
        ]
    },
    "112111": { 
        "type": "text", 
        "content": ["¡Genial, deshierbar es una excelente manera de embellecer nuestra comunidad!"] 
    },
    "112112": { 
        "type": "text", 
        "content": ["¡Perfecto, mantener las aceras limpias es crucial para una ciudad segura y acogedora!"] 
    },
    "112113": { 
        "type": "text", 
        "content": ["¡Excelente, limpiar las cunetas ayuda a prevenir inundaciones y a mantener nuestras calles en buen estado!"] 
    },
    "1121111": { 
        "type": "text", 
        "content": ["📍¿Dónde te gustaría que realizáramos esta acción?\n Describe la dirección del lugar con la mayor precisión posible (Ej: Zona, calle/avenida, al lado de, frente a)."] 
    },
    "11211111": {
        "type": "button",
        "content": [
            "Para ayudarnos a identificar el lugar exacto, ¿podrías compartirnos la ubicación georreferenciada del sitio?",
            "Selecciona una de las opciones.",
            ["btnOpt51", "Enviar Ubicacion"],
            ["btnOpt52", "No tengo ubicacion"]
        ]
    },
    "112111111": { 
        "type": "location_request_message", 
        "content": ["Por favor, envíenos la ubicacion georeferenciada presionando el siguiente boton."] 
    },
    "1121111111": {
        "type": "button",
        "content": [
            "Si tienes alguna fotografía o video del lugar, sería genial que los compartas con nosotros para que podamos entender mejor la situación.",
            "Selecciona una de las opciones.",
            ["btnOpt61", "Enviar fotografia"],
            ["btnOpt62", "No tengo fotografias"]
        ]
    },
    "11211111111": { 
        "type": "text", 
        "content": ["Por favor, envíenos la foto o video."] 
    },
    "112111111111": { 
        "type": "text", 
        "content": ["¡Perfecto! [Nombre] aquí tienes un resumen de tu solicitud:\n\n ✅ Acción solicitada: [Accion]\n ✅ C.I.: [Numero]\n ✅ Nombre: [Nombre]\n ✅ Direccion: [Ubicacion]\n ✅ Foto: [Imagen]\n ✅ Fecha solicitud: [FechaSol]\n Tu solicitud ha sido registrada y será sometida a una inspección previa para asegurar que podamos realizar la acción de la mejor manera posible. ¡Gracias por tu contribución!"] 
    },
    "1121111111111": { 
        "type": "text", 
        "content": ["Puedes escribir la palabra clave 'Inicio' en cualquier momento para detener la acción actual y regresar al menú principal."] 
    },
    "11212": {
        "type": "button",
        "content": [
            "No encontramos tu C.I. en nuestros registros. ¿Te gustaría registrarte?",
            "Selecciona una de las opciones.",
            ["btnOpt71", "Sí, registrar"],
            ["btnOpt72", "No, gracias"]
        ]
    },
    "112121": { 
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
    "1121211": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Apellido Paterno"] 
    },
    "11212111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Apellido Materno"] 
    },
    "112121111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Nombres"] 
    },
    "1121211111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Correo Electronico"] 
    },
    "11212111111": { 
        "type": "text", 
        "content": ["Por favor, ingresa los siguientes datos para registrarte.\n\n Contraseaña a utilizar"] 
    },
    "112121111111": { 
        "type": "text", 
        "content": ["¡Listo! Ahora continuemos con tu solicitud."] 
    },
    "1122": { 
        "type": "text", 
        "content": ["Por favor ingresa un Cédula de Identidad (C.I.) valido y sin extension."] 
    },
    "113": { 
        "type": "text", 
        "content": ["Para consultas generales, por favor, comunícate con nuestra línea gratuita al 155. ¡Estamos para ayudarte!"] 
    },
    "12": {
        "type": "text",
        "content": [
            "🙋🏻Modo seguimiento:\n ▪ Si deseas cambiar a hacer una solicitud escribe: NuevaSolicitud",
        ]
    }
}
# ======= ======= ======= ======= =======
# ======= ======= REDUCED MESSAGES EQUIVALENCE ======= =======
reducedMessageCodes = {
    "1111": "112",
    "1122": "112",
    "112122": "1112",
    "112111112":"1121111111",
    "11211111112":"112111111111",
    "112121111111": "11211",
    "112121111112": "1112",
    "1113": "113"
}
# ======= ======= ======= ======= =======
# ======= ======= MESSAGES WHIT SPECIAL ANSWERS ======= =======
specialMessageCodes = [
    "11",
    "111",
    "11211",
    "112111",
    "112112",
    "112113",
    "112121111111",
    "112111111111"
]
# ======= ======= ======= ======= =======
# ======= ======= IGNORE MESSAGE STATE/CODES ======= =======
ignoreMessages = [
    "invalid",
    "invalidPat",
    "invalidMat",
    "invalidNom",
    "invalidemail",
    "cancel",
    "freeChat"
]
# ======= ======= ======= ======= =======
# ======= ======= MESSAGES WHIT SPECIAL ANSWERS ======= =======
endConversationMessages = [
    "113",
    "1112",
    "112111111111"
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
