# GraphController.py

from flask import Blueprint, request, jsonify
from src.core.services.GetLOsService import GetLOService

LO_controller = Blueprint('graph_controller', __name__)


@LO_controller.route('/get_los_for_concept', methods=['POST'])
def get_los_for_concept():
    data = request.get_json()

    concept_name = data.get('concept_name', '')

    if not concept_name:
        return jsonify({"error": "concept_name is required"}), 400

    graph_service = GetLOService()
    los = graph_service.get_los_related_to_concept(concept_name)

    if not los:
        return jsonify({"message": "No learning objects found for the given concept"}), 404

    # إرجاع النتيجة في تنسيق JSON
    return jsonify({"learning_objects": los}), 200
