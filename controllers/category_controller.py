from flask import Blueprint, jsonify
from models.product_models.list_category import ListCategory

categoryBp = Blueprint('categoryBp',__name__)

@categoryBp.route('/category', methods=['GET'])
def get_category():
    try:
        categories = ListCategory.query.all()
        serialized_categories = [
            {
                'id': category.id,
                'category': category.category
                
            }
            for category in categories
        ]
        
        return jsonify({
            'success': True,
            'message': 'Categories retrieved successfully',
            'data': serialized_categories
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500