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
    "invalidCi": { 
        "type": "text", 
        "content": [
            "❌ Por favor, ingresa un C.I. válido. Solo se admiten números y debe tener un mínimo de 5 dígitos."
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
            "¡Hola [whatsappName]! Bienvenido/a al proyecto 100 jueves de Acción por el Bien Común. Estoy aquí para ayudarte a contribuir a nuestra comunidad. 😊",
            "Selecciona una de las opciones.",
            ["btnOpt21", "Saber del programa"],
            ["btnOpt22", "Hacer solicitud"],
            ["btnOpt23", "Hacer seguimiento"]
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
            ["btnOpt31", "Hacer solicitud"],
            ["btnOpt32", "No, gracias."],
            ["btnOpt33", "Otra Consulta"]
        ]
    },
    "112": { 
        "type": "text", 
        "content": ["😊 Gracias por tu interés en los '100 Jueves de Acción por el Bien Común'.\n ¡Hasta pronto! "] 
    },
    "113": { 
        "type": "text", 
        "content": ["✅ Para consultas generales, por favor, comunícate con nuestra línea gratuita al 155."] 
    },
    "12": { 
        "type": "text", 
        "content": ["Por favor, ingresa tu Cédula de Identidad (C.I.) para continuar."] 
    },
    "1211": {
        "type": "button",
        "content": [
            "👋¡Hola, [Nombre]!\n Elige una de las siguientes acciones para llevar a cabo:",
            "Selecciona una de las opciones.",
            ["btnOpt41", "Deshierbe"],
            ["btnOpt42", "Limpieza de Aceras"],
            ["btnOpt43", "Limpieza de Cunetas"]
        ]
    },
    "12111": { 
        "type": "text", 
        "content": ["👍🏻¡Genial, deshierbar es una excelente manera de embellecer nuestra comunidad!"] 
    },
    "12112": { 
        "type": "text", 
        "content": ["👍🏻¡Perfecto, mantener las aceras limpias es crucial para una ciudad segura y acogedora!"] 
    },
    "12113": { 
        "type": "text", 
        "content": ["👍🏻¡Excelente, limpiar las cunetas ayuda a prevenir inundaciones y a mantener nuestras calles en buen estado!"] 
    },
    "121111": { 
        "type": "text", 
        "content": ["📍¿Dónde te gustaría que realizáramos esta acción?\n Describe la dirección del lugar con la mayor precisión posible (Ej: Zona, calle/avenida, al lado de, frente a)."] 
    },
    "1211111": {
        "type": "button",
        "content": [
            "📍Para ayudarnos a identificar el lugar exacto, ¿Podrías compartirnos la ubicación del lugar?",
            "Selecciona una de las opciones.",
            ["btnOpt51", "Enviar Ubicacion"],
            ["btnOpt52", "No tengo ubicacion"]
        ]
    },
    "12111111": { 
        "type": "location_request_message", 
        "content": ["Por favor, envíenos la ubicacion georeferenciada presionando el siguiente boton."] 
    },
    "121111111": {
        "type": "button",
        "content": [
            "📷 Si tienes alguna fotografía, sería genial que nos compartas para entender mejor la situación.",
            "Selecciona una de las opciones.",
            ["btnOpt61", "Enviar fotografia"],
            ["btnOpt62", "No tengo fotografias"]
        ]
    },
    "1211111111": { 
        "type": "text", 
        "content": ["Por favor, envíenos la foto o video."] 
    },
    "12111111111": { 
        "type": "text", 
        "content": ["¡Perfecto! [Nombre] aquí tienes un resumen de tu solicitud:\n\n ✅ Acción solicitada: [Accion]\n ✅ C.I.: [Numero]\n ✅ Nombre: [Nombre]\n ✅ Direccion: [Ubicacion]\n ✅ Foto: [Imagen]\n ✅ Fecha solicitud: [FechaSol]\n Tu solicitud ha sido registrada y será sometida a una inspección previa para asegurar que podamos realizar la acción de la mejor manera posible. ¡Gracias por tu contribución!"] 
    },
    "121111111111": { 
        "type": "text", 
        "content": ["Puedes escribir la palabra clave 'Inicio' en cualquier momento para detener la acción actual y regresar al menú principal."] 
    },
    "1212": {
        "type": "button",
        "content": [
            "No encontramos tu C.I. en nuestros registros. ¿Te gustaría registrarte?",
            "Selecciona una de las opciones.",
            ["btnOpt71", "Sí, registrar"],
            ["btnOpt72", "No, gracias"]
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
        "content": ["¡Listo! Ahora continuemos con tu solicitud."] 
    },
    "122": { 
        "type": "text", 
        "content": ["Por favor ingresa un Cédula de Identidad (C.I.) valido y sin extension."] 
    },
    "13": {
        "type": "text",
        "content": [
            "🙋🏻Modo seguimiento:\n ▪ Si deseas cambiar a hacer una solicitud escribe: NuevaSolicitud",
        ]
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
    "1212111111": "1211",
    "1212111112": "112"
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
    "1212111111",
    "12111111111"
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
    "freeChat",
    "ignore"
]
# ======= ======= ======= ======= =======
# ======= ======= MESSAGES WHIT SPECIAL ANSWERS ======= =======
endConversationMessages = [
    "113",
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
