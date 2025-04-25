from flask import Blueprint, request, jsonify
from src.algorithms.iia.AffinityCalculation import AffinityCalculation
from src.algorithms.iia.SelectionV2 import Selection
from src.algorithms.iia.VariationOperators import apply_genetic_operators, reconstruct_learning_path
from src.algorithms.iia.getLS import getLS

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

        threshold = 0.01
        alpha = 0.5

        # Initial affinity calculation and selection
        affinity_calc = AffinityCalculation(learner_email, learning_goals, knowledge_base, threshold)
        ranked_population = affinity_calc.rank_learning_paths()
        affinity_data = affinity_calc.get_affinity_and_concentration()

        # ✅ Correct instantiation
        # Original selection
        selection = Selection(ranked_population, affinity_data, alpha)
        selected_path, selected_index = selection.roulette_wheel_selection()
        filtered_result = selection.get_filtered_best_path_from_result(selected_path, selected_index)
        # ✅ Filtered version for app/controller
        print("\n🧪 Filtered Best Path Output (LO Name & ID Only):")
        print(filtered_result)

        original_affinity = selected_path[1]

        # Extract all chromosomes from the ranked population
        all_chromosomes = [path[3] for path in ranked_population]

        # Apply genetic operators (crossover and mutation) to evolve the population
        evolved_chromosomes = apply_genetic_operators(
            all_chromosomes,
            top_n=10,  # Take top 10 chromosomes
            crossover_probability=0.8,
            mutation_rate=0.05,
            test_mode=False
        )

        # Get all available learning objects from the population data
        ls_service = getLS()
        population_data = ls_service.LOsLS(learning_goals, knowledge_base)
        all_los = population_data.get("LOs", [])

        # Initialize final variables to original paths in case evolution is not successful
        final_path = selected_path
        final_index = selected_index

        # Re-evaluate the fitness of the evolved population
        if evolved_chromosomes:
            # Create new learning paths from evolved chromosomes
            evolved_population = []

            for evolved_chromosome in evolved_chromosomes:
                # First check if this is an unchanged chromosome from the original population
                matching_original_path = None
                for idx, path in enumerate(ranked_population):
                    if path[3] == evolved_chromosome:
                        matching_original_path = path
                        break

                if matching_original_path:
                    # If it's an original chromosome, use its existing data
                    evolved_population.append(matching_original_path)
                else:
                    # If it's a new chromosome from crossover/mutation, we need to reconstruct
                    if len(evolved_chromosome) % 30 != 0:
                        continue

                    # Reconstruct learning objects from the chromosome
                    try:
                        reconstructed_los = reconstruct_learning_path(evolved_chromosome, all_los)
                        if not reconstructed_los:
                            continue

                        # Extract learning styles from reconstructed LOs
                        reconstructed_ls = [
                            {
                                "learning_style_visual_verbal": float(lo.get("learning_style_visual_verbal", 0) or 0),
                                "learning_style_sequential_global": float(lo.get("learning_style_sequential_global", 0) or 0),
                                "learning_style_sensitive_intuitive": float(lo.get("learning_style_sensitive_intuitive", 0) or 0),
                                "learning_style_active_reflective": float(lo.get("learning_style_active_reflective", 0) or 0)
                            }
                            for lo in reconstructed_los
                        ]

                        # Calculate affinity for this reconstructed path
                        reconstructed_affinity = affinity_calc.compute_affinity(reconstructed_ls)

                        # Create a new path tuple with the reconstructed data
                        reconstructed_path = (reconstructed_ls, reconstructed_affinity, reconstructed_los, evolved_chromosome)
                        evolved_population.append(reconstructed_path)
                    except Exception as e:
                        print(f"Error reconstructing learning path: {str(e)}")
                        continue

            # Re-rank the evolved population if we have any valid evolved paths
            if evolved_population:
                # Calculate concentration for evolved chromosomes
                evolved_chromosomes_list = [path[3] for path in evolved_population]
                evolved_affinity_data = [
                    [path[1], affinity_calc.calculate_concentration(path[3], evolved_chromosomes_list)]
                    for path in evolved_population
                ]

                # Create a new Selection object with the evolved population
                evolved_selection = Selection(evolved_population, evolved_affinity_data, alpha)
                evolved_path, evolved_index = evolved_selection.roulette_wheel_selection()

                # Compare the evolved best path with the original best path
                evolved_affinity = evolved_path[1]

                # Choose the best path between original and evolved
                if evolved_affinity > original_affinity:
                    print(f"Evolution successful! Improved affinity from {original_affinity:.4f} to {evolved_affinity:.4f}")
                    final_path = evolved_path
                    final_index = evolved_index
                else:
                    print("Evolution did not improve the path. Keeping original.")

        # Return filtered result in the same format expected by the mobile app
        filtered_result = selection.get_filtered_best_path_from_result(final_path, final_index)
        return jsonify(filtered_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
