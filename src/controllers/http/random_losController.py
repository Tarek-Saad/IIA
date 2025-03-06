from flask import Blueprint, request, jsonify
from src.algorithms.iia.Pop_index_LO_match import GetLOMatching


from src.algorithms.iia.Population import Population
from src.core.services.ChooseRandomLOService import ConceptOrderService
from src.algorithms.iia.Encoding import Encoding
from src.core.services.ConceptMappingService import ConceptMappingService

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

    # Set the concept_lo_mapping to the ConceptMappingService for global use
    mapping_service = ConceptMappingService()
    mapping_service.set_concept_lo_mapping(concept_lo_mapping)

    # If no random LOs were selected, return an error
    if not concept_lo_mapping:
        return jsonify({"message": "No Learning Objects found for the given concepts"}), 404

    # Instantiate Encoding to generate chromosome
    encoding_service = Encoding()
    chromosome = encoding_service.encode_los_to_chromosome(concept_lo_mapping)

    return jsonify({"encoded_chromosome": chromosome}), 200

@concept_controller.route('/generate_initial_population', methods=['POST'])
def generate_initial_population():
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

    # Instantiate Population to generate the initial population of antibodies (chromosomes)
    population_service = Population()

    # Generate the initial population (100 antibodies)
    population = population_service.generate_initial_population(concept_lo_mapping, population_size=100, total_los_count=40)

    return jsonify({"initial_population": population}), 200


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
