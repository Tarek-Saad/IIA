from flask import Blueprint, request, jsonify
from flask_cors import CORS
from src.core.services.generate_learning_analysis import generate_learning_analysis

learning_analysis_controller = Blueprint('learning_analysis_controller', __name__)
CORS(learning_analysis_controller, resources={
    r"/*": {
        "origins": ["http://192.168.1.195:3000", "http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    }
})

@learning_analysis_controller.route('/analyze', methods=['POST'])
def analyze_learning():
    data = request.get_json()

    user_knowledge = data.get("user_knowledge", "")
    user_goal = data.get("user_goal", "")

    if not user_knowledge or not user_goal:
        return jsonify({"error": "Both user_knowledge and user_goal are required"}), 400

    result = generate_learning_analysis(user_knowledge, user_goal)
    return jsonify(result), 200