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
            "❌. Parece que la información ingresada no es válida. Por favor, asegúrate de proporcionar datos correctos.",
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
            "Para ayudarnos a identificar el lugar exacto, ¿podrías compartirnos la ubicación georreferenciada del sitio?",
            "Selecciona una de las opciones.",
            ["btnOpt1", "1️⃣. Enviar Ubicacion"],
            ["btnOpt2", "2️⃣. No enviar"]
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
            ["btnOpt1", "1️⃣. Enviar Foto/Video"],
            ["btnOpt2", "2️⃣. No enviar"]
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
            ["btnOpt1", "1️⃣. Sí, registrar"],
            ["btnOpt2", "2️⃣. No, gracias"]
        ]
    },
    "12121": { 
        "type": "list", 
        "content": [
            "Por favor, ingresa los siguientes datos para registrarte.\n\n Expedido",
            "Selecciona una de las opciones.",
            "Ver extenciones.",
            ["LPZ1", "1️⃣. LPZ", "Expedido en La Paz"],
            ["CBB1", "2️⃣. CBB", "Expedido en Cochabamba"],
            ["SCZ1", "3️⃣. SCZ", "Expedido en Santa Cruz"],
            ["CHQ1", "4️⃣. CHQ", "Expedido en Chuquisaca"],
            ["TJA1", "5️⃣. TJA", "Expedido en Tarija"],
            ["PTS1", "6️⃣. PTS", "Expedido en Potosí"],
            ["ORU1", "7️⃣. ORU", "Expedido en Oruro"],
            ["BNI1", "8️⃣. BNI", "Expedido en Beni"],
            ["PND1", "9️⃣. PND", "Expedido en Pando"]
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
    "113": "13",
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
