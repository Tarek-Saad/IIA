from flask import Blueprint, request, jsonify
from src.core.services.GraphService import GraphService

graph_controller = Blueprint('graph_controller', __name__)

@graph_controller.route('/relevant_concepts', methods=['POST'])
def get_relevant_concepts():
    data = request.get_json()
    learning_goals = data.get('learning_goals', [])
    knowledge_base = data.get('knowledge_base', [])

    graph_service = GraphService()
    relevant_concepts = graph_service.get_relevant_concepts(learning_goals, knowledge_base)

    return jsonify({"relevant_concepts": list(relevant_concepts)}), 200

@graph_controller.route('/traversal', methods=['POST'])
def traversal():
    data = request.get_json()
    learning_goals = data.get('learning_goals', [])
    knowledge_base = data.get('knowledge_base', [])

    # Instantiate GraphService
    graph_service = GraphService()

    # Call the proposed traversal algorithm
    traversal_result = graph_service.proposed_traversal_algorithm(learning_goals, knowledge_base)

    return jsonify({"traversal_result": traversal_result}), 200
