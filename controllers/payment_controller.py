from flask import Blueprint, jsonify
from models.transaction_models.payment_method import PaymentMethod

paymentBp = Blueprint('paymentBp',__name__)

@paymentBp.route('/paymentmethod', methods=['GET'])
def get_payment_method():
    payment_methods = PaymentMethod.query.all()
    serialized_payment_methods = []
    for payment_method in payment_methods:
        serialized_payment_method = {
            "id": payment_method.id,
            "name": payment_method.payment_name,
            "number": payment_method.payment_number
        }
        serialized_payment_methods.append(serialized_payment_method)
    return jsonify({
        "success": True,
        "message": "Payment method retrieved successfully",
        "data": serialized_payment_methods
    }), 200