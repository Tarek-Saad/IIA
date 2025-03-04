from flask import Blueprint, request, jsonify
from src.core.services.ChooseRandomLOService import ConceptOrderService
from src.algorithms.iia.Encoding import Encoding

concept_controller = Blueprint('concept_controller', __name__)

@concept_controller.route('/random_los_encoding', methods=['POST'])
def random_los_encoding():
    data = request.get_json()
    concept_names = data.get('traversal_result', [])  # Expecting a list of concept names

    # Check if concept_names is not empty
    if not concept_names:
        return jsonify({"error": "concept_names are required"}), 400

    # Instantiate ConceptOrderService to get random LOs for each concept
    concept_service = ConceptOrderService()
    concept_lo_mapping = concept_service.get_random_lo_for_each_concept(concept_names)

    # If no random LOs were selected, return an error
    if not concept_lo_mapping:
        return jsonify({"message": "No Learning Objects found for the given concepts"}), 404

    # Instantiate Encoding to generate chromosome
    encoding_service = Encoding()

    # Get the total number of LOs (this can be dynamically calculated or defined based on your dataset)
    total_los_count = 40  # Adjust based on the number of LOs per concept

    # Encode the selected LOs into a chromosome
    chromosome = encoding_service.encode_los_to_chromosome(concept_lo_mapping, total_los_count)

    return jsonify({"encoded_chromosome": chromosome}), 200