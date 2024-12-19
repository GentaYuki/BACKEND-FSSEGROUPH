from flask import Blueprint, jsonify
from models.transaction_models.payment_method import PaymentMethod

paymentBp = Blueprint('paymentBp',__name__)

@paymentBp.route('/paymentmethod', methods=['GET'])
def get_payment_method():
    try:
        payment_methods = PaymentMethod.query.all()
        serialized_payment_methods = [
            {
                "id": payment_method.id,
                "name": payment_method.payment_name,
                "number": payment_method.payment_number
            }
            for payment_method in payment_methods
        ]
        return jsonify({
            "success": True,
            "message": "Payment method retrieved successfully",
            "data": serialized_payment_methods
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error retrieving payment method: {str(e)}",
            "data": None
        }), 500