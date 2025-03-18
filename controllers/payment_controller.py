from flask import Blueprint, jsonify, request
from models.transaction_models.payment_method import PaymentMethod

paymentBp = Blueprint('paymentBp',__name__)

@paymentBp.route('/paymentmethod', methods=['GET', 'OPTIONS'])
def get_payment_method():
    if request.method == 'OPTIONS':
        return jsonify({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }), 200

    payment_methods = PaymentMethod.query.all()
    serialized_payment_methods = [
        {
            "id": payment_method.id,
            "name": payment_method.payment_name,
            "number": payment_method.payment_number
        }
        for payment_method in payment_methods
    ]

    response = jsonify({
        "success": True,
        "message": "Payment method retrieved successfully",
        "data": serialized_payment_methods
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response