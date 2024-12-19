from flask import Blueprint, jsonify, request
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_models.user import User, Role_division
from models.transaction_models.payment_method import PaymentMethod
from models.transaction_models.transaction_detail_customer import TrasactionDetailCustomer,StatusEnumCust
from models.transaction_models.transaction_detail_seller import TransactionDetailSeller, StatusEnumSell
from models.transaction_models.discount_code import DiscountCode
from models.transaction_models.order_product import OrderProduct
from models.product_models.product import Product

transactionBp = Blueprint('transactionBp',__name__)

# create transaction
@transactionBp.route('/transaction', methods=['POST'])
@jwt_required()
def create_order_transaction():
    current_user = get_jwt_identity()
    data = request.get_json()

    #cek if data is None
    if not data:
        return jsonify({"success": False, "message": "Missing JSON payload"}), 400

    #cek if required fields are present
    required_fields = ['payment_method_id', 'discount_code', 'products']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

    try:
        #cek if user exist and have role customer
        user = User.query.filter_by(id=current_user).first()
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
        if user.role not in [Role_division.customer]:
            return jsonify({
                "success": False,
                "message": "You are not authorized to create an order product"
            }), 403

        #cek if payment method exist
        payment_method = PaymentMethod.query.filter_by(id=data['payment_method_id']).first()
        if not payment_method:
            return jsonify({
                "success": False,
                "message": "Payment method not found"
            }), 404

        #cek if discount code exist
        discount = DiscountCode.query.filter_by(code=data['discount_code']).first()
        if not discount:
            return jsonify({
                "success": False,
                "message": "Discount code not found"
            }), 404
        
        # create order transaction
        order_products = []
        total_price = 0
        for product_data in data['products']:
            if 'product_id' not in product_data or 'quantity' not in product_data:
                return jsonify({
                    "success": False,
                    "message": "Missing required fields: product_id and quantity"
                }), 400

            product = Product.query.filter_by(id=product_data['product_id']).first()
            if not product:
                return jsonify({
                    "success": False,
                    "message": "Product not found"
                }), 404

            if product.stock_qty < product_data['quantity']:
                return jsonify({
                    "success": False,
                    "message": "Insufficient product quantity"
                }), 400
            
            sum_price = product.price * product_data['quantity']
            total_price += sum_price

            order_product = OrderProduct(
                customer_id=user.id,
                product_id=product.id,
                quantity=product_data['quantity'],
                sum_price=sum_price,
                seller_id=product.seller_id
            )

            order_products.append(order_product)

        #Apply discount
        discount_value = discount.discount_value
        total_price -= discount_value
        
        transaction_detail = TrasactionDetailCustomer(
            user_id=user.id,
            payment_id=payment_method.id,
            total_price=total_price,
            status=StatusEnumCust.pending
        )
        db.session.add(transaction_detail)
        db.session.commit()

        for order_product in order_products:
            order_product.order_id = transaction_detail.id
            db.session.add(order_product)
            db.session.commit()

        serialized_order_products = []
        for order_product in order_products:
            seller = User.query.filter_by(id=order_product.seller_id).first()
            if not seller:
                return jsonify({
                    "success": False,
                    "message": "Seller not found"
                }), 404

            serialized_order_product = {
                "transaction_id": order_product.order_id,
                "customer": user.userName,
                "title": Nproduct.title if (Nproduct := Product.query.get(order_product.product_id)) else None,
                "quantity": order_product.quantity,
                "sum_price": order_product.sum_price,
                "seller": seller.userName
            }
            serialized_order_products.append(serialized_order_product)

        serialized_transaction_detail = {
            "transaction_id": transaction_detail.id,
            "user_id": transaction_detail.user_id,
            "payment_method": payment_method.payment_method.value,
            "total_price": transaction_detail.total_price,
            "status": transaction_detail.status.value
        }
        
        #create transaction_detail_sellers from transaction_detail_customer
        transaction_detail_seller = []
        for order_product in order_products:
            transaction_detail_seller.append(
                TransactionDetailSeller(
                    order_id=transaction_detail.id,
                    seller_id=order_product.seller_id,
                    product_id=order_product.product_id,
                    total_price=order_product.sum_price,
                    status=StatusEnumSell.pending
                )
            )
        
        db.session.add_all(transaction_detail_seller)
        db.session.commit()    
        
        return jsonify(
            {
                "success": True,
                "message": "Transaction and order created successfully",
                "data_product": serialized_order_products,
                "data_transaction": serialized_transaction_detail
            }
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
        
    finally:
        db.session.close()
#cek histoy transaction for customer        
@transactionBp.route('/historytransaction', methods=['GET'])
@jwt_required()
def get_transaction():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404
    if user.role not in [Role_division.customer]:
        return jsonify({
            "success": False,
            "message": "You are not authorized to get transaction"
        }), 403
    transactions = TrasactionDetailCustomer.query.filter_by(user_id=user.id).all()
    serialized_transactions = []
    for transaction in transactions:
        order_products = OrderProduct.query.filter_by(order_id=transaction.id).all()
        serialized_order_products = []
        for order_product in order_products:
            seller = User.query.filter_by(id=order_product.seller_id).first()
            if not seller:
                return jsonify({
                    "success": False,
                    "message": "Seller not found"
                }), 404
            product = Product.query.filter_by(id=order_product.product_id).first()
            if not product:
                return jsonify({
                    "success": False,
                    "message": "Product not found"
                }), 404
            serialized_order_product = {
                "product_name": product.title,
                "quantity": order_product.quantity,
                "sum_price": order_product.sum_price,
                "seller": seller.userName
            }
            serialized_order_products.append(serialized_order_product)
        payment_method = PaymentMethod.query.filter_by(id=transaction.payment_id).first()
        if not payment_method:  
            return jsonify({
                "success": False,
                "message": "Payment method not found"
            }), 404
        
        serialized_transaction = {
            "Transaction_id": transaction.id,
            "customer": user.userName,
            "payment_method": payment_method.payment_method.value,
            "Bank" : payment_method.payment_name,
            "total_price": transaction.total_price,
            "status": transaction.status.value,
            "date": transaction.updated_at if transaction.updated_at else transaction.created_at,
            "order_products": serialized_order_products
        }
        serialized_transactions.append(serialized_transaction)
    return jsonify({
        "success": True,
        "message": "Transaction retrieved successfully",
        "data": serialized_transactions
    })
#create route to cek transaction detail for seller, so seller can cek each product in transacton detail seller
@transactionBp.route('/transaction/seller', methods=['GET'])
@jwt_required()
def get_transaction_detail():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404
    if user.role not in [Role_division.seller]:
        return jsonify({
            "success": False,
            "message": "You are not authorized to get transaction"
        }), 403
    transaction_detail_sellers = TransactionDetailSeller.query.filter_by(seller_id=user.id).all()
    serialized_transaction_detail_sellers = []
    for transaction_detail_seller in transaction_detail_sellers:
        serialized_transaction_detail_seller = {
            "transaction_id": transaction_detail_seller.order_id,
            "product": product.title if (product := Product.query.get(transaction_detail_seller.product_id)) else None,
            "total_price": transaction_detail_seller.total_price,
            "status": transaction_detail_seller.status.value
        }
        serialized_transaction_detail_sellers.append(serialized_transaction_detail_seller)
    return jsonify({
        "success": True,
        "message": "Transaction detail retrieved successfully",
        "data": serialized_transaction_detail_sellers
    })


@transactionBp.route('/transaction/seller', methods=['POST'])
@jwt_required()
def update_transaction():
    current_user = get_jwt_identity()
    data = request.get_json()
    user = User.query.filter_by(id=current_user).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    if user.role not in [Role_division.seller]:
        return jsonify({
            "success": False,
            "message": "You are not authorized to update transaction"
        }), 404
        
    if not data.get('transaction_id'):
        return jsonify({
            "success": False,
            "message": "Transaction ID is required"
        }), 400

    transaction_detail_sellers = TransactionDetailSeller.query.filter_by(order_id=data.get('transaction_id'), product_id=data.get('product_id')).first()
    if not transaction_detail_sellers:
        return jsonify({
            "success": False,
            "message": "Transaction detail not found"
        }), 404
    print(transaction_detail_sellers.status)

    if transaction_detail_sellers.seller_id != user.id:
        return jsonify({
            "success": False,
            "message": "You are not authorized to update this product"
        }), 403

    current_status = transaction_detail_sellers.status
    new_status = data.get('status')

    # Define the valid sequence for status updates
    status_order = [StatusEnumSell.pending, StatusEnumSell.on_process, StatusEnumSell.on_delivery]

    if new_status == StatusEnumSell.rejected:
        # If the new status is 'rejected', allow it from any state
        transaction_detail_sellers.status = new_status
        db.session.commit()
    else:
        # Check if the status change follows the allowed order
        if new_status not in status_order:
            return jsonify({
                "success": False,
                "message": "Invalid status transition."
            }), 400

        if current_status == StatusEnumSell.pending and new_status == StatusEnumSell.on_process:
            transaction_detail_sellers.status = new_status
        elif current_status == StatusEnumSell.on_process and new_status == StatusEnumSell.on_delivery:
            transaction_detail_sellers.status = new_status
        else:
            return jsonify({
                "success": False,
                "message": "Status update cannot be skipped."
            }), 400

        db.session.commit()

    # Check if all status in 1 transaction_id have all same status
    transaction_detail_sellers_all = TransactionDetailSeller.query.filter_by(order_id=data.get('transaction_id')).all()
    statuses = [seller.status for seller in transaction_detail_sellers_all]
    if len(set(statuses)) == 1:
        transaction_detail_customer = TrasactionDetailCustomer.query.filter_by(id=data.get('transaction_id')).first()
        if transaction_detail_customer:
            transaction_detail_customer.status = statuses[0]
            db.session.commit()
            
    return jsonify({
        "success": True,
        "message": "Transaction updated successfully"
    }),500