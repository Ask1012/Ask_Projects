from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__, static_folder='public', static_url_path='')

# Initialize orders list
orders = []

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/order', methods=['POST'])
def handle_order():
    try:
        order = request.json
        orders.insert(0, order)  # Add the order to the beginning of the list
        return jsonify({'message': 'Order received'}), 200
    except Exception as e:
        print(f'Error handling order: {e}')
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/order', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

@app.route('/kitchen')
def kitchen():
    return send_from_directory(app.static_folder, 'kitchen.html')

@app.route('/admin')
def admin():
    return send_from_directory(app.static_folder, 'admin.html')

@app.route('/menu-items', methods=['GET'])
def get_menu_items():
    try:
        with open(os.path.join(app.static_folder, 'useritem.json'), 'r') as f:
            items = json.load(f)
        return jsonify(items), 200
    except Exception as e:
        print(f'Error reading menu items: {e}')
        return jsonify({'success': False}), 500

@app.route('/add-item', methods=['POST'])
def add_item():
    try:
        new_item = request.json

        with open(os.path.join(app.static_folder, 'useritem.json'), 'r') as f:
            items = json.load(f)

        items.append(new_item)

        with open(os.path.join(app.static_folder, 'useritem.json'), 'w') as f:
            json.dump(items, f, indent=2)

        return jsonify({'success': True}), 200
    except Exception as e:
        print(f'Error handling item addition: {e}')
        return jsonify({'success': False}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
