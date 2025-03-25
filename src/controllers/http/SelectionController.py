from flask import Blueprint, request, jsonify
from src.algorithms.iia.AffinityCalculation import AffinityCalculation
from src.algorithms.iia.Selection import Selection

selection_controller = Blueprint('selection_controller', __name__)

@selection_controller.route('/selection/best-path', methods=['POST'])
def get_best_learning_path():
    try:
        data = request.get_json()

        learner_email = data.get('learner_email')
        learning_goals = data.get('learning_goals')
        knowledge_base = data.get('knowledge_base')

        if not learner_email or not learning_goals or not knowledge_base:
            return jsonify({"error": "Missing required fields"}), 400

        threshold = 0.5
        alpha = 0.5

        affinity_calc = AffinityCalculation(learner_email, learning_goals, knowledge_base, threshold)
        ranked_population = affinity_calc.rank_learning_paths()
        affinity_data = affinity_calc.get_affinity_and_concentration()

        selection = Selection(ranked_population, affinity_data, alpha)
        selected_path, selected_index = selection.roulette_wheel_selection()
        filtered_result = selection.get_filtered_best_path_from_result(selected_path, selected_index)

        return jsonify(filtered_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
