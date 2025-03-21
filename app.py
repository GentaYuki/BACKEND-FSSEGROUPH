from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    print('connecting to database...')
    # Configure app
    app.config.update(
        SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY="secret!",
        JWT_SECRET_KEY="secret!",
        UPLOAD_EXTENSIONS=['jpg', 'jpeg', 'png']
    )

    # Initialize extensions
    CORS(app, 
    resources={r"/*": {
        "origins": ["http://localhost:3000", 
                   "http://127.0.0.1:3000", 
                   "http://192.168.1.8:3000", 
                   "https://toko-edi-ya.vercel.app"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Methods"], # Add this line
        "supports_credentials": True
    }})
    # Add preflight handler
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response
    
    JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from controllers.user_controller import userBp
    from controllers.master_question_controller import masterBp
    from controllers.product_controller import productBp
    from controllers.discount_controller import discountBp
    from controllers.transaction_controller import transactionBp
    from controllers.category_controller import categoryBp
    from controllers.review_controller import reviewBp
    from controllers.payment_controller import paymentBp
    

    app.register_blueprint(userBp)
    app.register_blueprint(masterBp)
    app.register_blueprint(productBp)
    app.register_blueprint(discountBp)
    app.register_blueprint(transactionBp)
    app.register_blueprint(categoryBp)
    app.register_blueprint(reviewBp)
    app.register_blueprint(paymentBp)


    print('connected to database')
    # Register routes
    @app.route("/")
    @cross_origin()  # Allow CORS for this route
    def helloWorld():
        return jsonify({"message": "Hello, cross-origin-world!"})

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)