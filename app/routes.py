from flask import Blueprint, request, jsonify, send_file, current_app
import pandas as pd
from io import BytesIO
from .helpers import verificar_token
from .services.receivedMessagesHandler import onReceivedMessage

# ======= ======= BLUE PRINT DEF ======= =======
routes_bp = Blueprint('routes_bp', __name__)
# ======= ======= =======
# ======= WEBHOOK PATH =======
@routes_bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if(request.method == 'GET'):
        challenge = verificar_token(request)
        return challenge
    elif(request.method == 'POST'):
        response = onReceivedMessage(request)
        return response
# ======= ======= =======
# ======= EXCEL DOWNLOAD =======
@routes_bp.route('/download-excel', methods=['GET'])
def download_excel():
    collection = current_app.config['MONGO_DB']['data']
    
    data = list(collection.find({}, {'_id': 0}))
    
    if not data:
        return jsonify({"error": "No data available"}), 404
    
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                     as_attachment=True, download_name='data.xlsx')
# ======= ======= =======