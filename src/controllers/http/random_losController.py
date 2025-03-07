from flask import Blueprint, request, jsonify
from src.algorithms.iia.Pop_index_LO_match import GetLOMatching



from src.core.services.ChooseRandomLOService import ConceptOrderService

concept_controller = Blueprint('concept_controller', __name__)



@concept_controller.route('/get_selected_los', methods=['POST'])
def get_selected_los():
    data = request.get_json()
    learning_goals = data.get('learning_goals', [])  # Learning goals (e.g., ["Trees"])
    knowledge_base = data.get('knowledge_base', [])  # Knowledge base (e.g., ["Introduction to Programming"])

    # Ensure that learning_goals and knowledge_base are provided
    if not learning_goals or not knowledge_base:
        return jsonify({"error": "learning_goals and knowledge_base are required"}), 400

    # Instantiate GetLOMatching and get the matching LOs based on learning goals and knowledge base
    get_lo_matching = GetLOMatching()
    selected_los = get_lo_matching.getLOMatch(learning_goals, knowledge_base)

    # Return the selected LOs
    return jsonify({"selected_los": selected_los}), 200
