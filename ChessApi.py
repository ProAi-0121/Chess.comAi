from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/update_moves', methods=['POST'])
def update_moves():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Invalid data"}), 400
    try:
        with open("game_data.json", "r") as file:
            previous_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        previous_data = {}

    if data != previous_data:
        try:
            with open("game_data.json", "w") as file:
                json.dump(data, file, indent=4)
            return jsonify({"success": True, "message": "Game data updated successfully"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        return jsonify({"success": True, "message": "No changes detected"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
