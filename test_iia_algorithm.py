"""
Test script for the Improved Immune Algorithm (IIA) with genetic operators.
This script runs the algorithm directly without using the API endpoint.
"""
from src.algorithms.iia.AffinityCalculation import AffinityCalculation
from src.algorithms.iia.SelectionV2 import Selection
from src.algorithms.iia.VariationOperators import apply_genetic_operators, reconstruct_learning_path
from src.algorithms.iia.getLS import getLS

def test_iia_with_genetic_operators(learner_email, learning_goals, knowledge_base, test_mode=True):
    """
    Test the IIA algorithm with genetic operators (crossover and mutation).
    
    Args:
        learner_email: The email of the learner
        learning_goals: List of learning goals
        knowledge_base: List of concepts the learner already knows
        test_mode: Whether to force crossover to always happen (for testing)
    """
    print("\n======================= 🔍 Starting IIA Algorithm Test =======================")
    print(f"Learner: {learner_email}")
    print(f"Learning goals: {learning_goals}")
    print(f"Knowledge base: {knowledge_base}")
    print(f"Test mode: {test_mode}")
    
    threshold = 0.5
    alpha = 0.5

    # Initial affinity calculation and selection
    print("\n🔹 Step 1: Initial affinity calculation")
    affinity_calc = AffinityCalculation(learner_email, learning_goals, knowledge_base, threshold)
    ranked_population = affinity_calc.rank_learning_paths()
    affinity_data = affinity_calc.get_affinity_and_concentration()

    # Roulette wheel selection
    print("\n🔹 Step 2: Roulette wheel selection")
    selection = Selection(ranked_population, affinity_data, alpha)
    selected_path, selected_index = selection.roulette_wheel_selection()
    
    print(f"\n📊 Original best path:")
    print(f"   • Index: {selected_index}")
    print(f"   • Affinity: {selected_path[1]:.4f}")
    print(f"   • Learning objects: {[lo.get('name') for lo in selected_path[2]]}")
    
    # Extract all chromosomes from the ranked population
    all_chromosomes = [path[3] for path in ranked_population]
    
    print("\n🔹 Step 3: Applying genetic operators")
    # Apply genetic operators (crossover and mutation) to evolve the population
    evolved_chromosomes = apply_genetic_operators(
        all_chromosomes, 
        top_n=10,  # Take top 10 chromosomes
        crossover_probability=0.8, 
        mutation_rate=0.05,
        test_mode=test_mode
    )
    
    # Get all available learning objects from the population data
    print("\n🔹 Step 4: Getting learning objects for reconstruction")
    ls_service = getLS()
    population_data = ls_service.LOsLS(learning_goals, knowledge_base)
    all_los = population_data.get("LOs", [])
    
    # Re-evaluate the fitness of the evolved population
    if evolved_chromosomes:
        print("\n🔹 Step 5: Re-evaluating evolved population")
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
                print(f"   ℹ️ Using original path (unchanged chromosome)")
            else:
                # If it's a new chromosome from crossover/mutation, we need to reconstruct
                if len(evolved_chromosome) % 30 != 0:
                    print(f"   ⚠️ Skipping chromosome with incompatible length: {len(evolved_chromosome)}")
                    continue
                
                # Reconstruct learning objects from the chromosome
                try:
                    reconstructed_los = reconstruct_learning_path(evolved_chromosome, all_los)
                    if not reconstructed_los:
                        print("   ⚠️ Skipping chromosome - no learning objects could be reconstructed")
                        continue
                        
                    # Extract learning styles from reconstructed LOs
                    reconstructed_ls = [
                        {
                            "learning_style_visual_verbal": lo.get("learning_style_visual_verbal", 0),
                            "learning_style_sequential_global": lo.get("learning_style_sequential_global", 0),
                            "learning_style_sensitive_intuitive": lo.get("learning_style_sensitive_intuitive", 0),
                            "learning_style_active_reflective": lo.get("learning_style_active_reflective", 0)
                        }
                        for lo in reconstructed_los
                    ]
                    
                    # Calculate affinity for this reconstructed path
                    reconstructed_affinity = affinity_calc.compute_affinity(reconstructed_ls)
                    
                    # Create a new path tuple with the reconstructed data
                    reconstructed_path = (reconstructed_ls, reconstructed_affinity, reconstructed_los, evolved_chromosome)
                    evolved_population.append(reconstructed_path)
                    
                    print(f"   ✅ Successfully reconstructed path with affinity: {reconstructed_affinity:.4f}")
                except Exception as e:
                    print(f"   ⚠️ Error reconstructing learning path: {str(e)}")
                    continue
        
        # Re-rank the evolved population if we have any valid evolved paths
        if evolved_population:
            print("\n🔹 Step 6: Ranking evolved population")
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
            original_affinity = selected_path[1]
            evolved_affinity = evolved_path[1]
            
            print(f"\n🔄 Comparing original vs evolved path:")
            print(f"   • Original path affinity: {original_affinity:.4f}")
            print(f"   • Evolved path affinity: {evolved_affinity:.4f}")
            
            print(f"\n📊 Evolved best path:")
            print(f"   • Index: {evolved_index}")
            print(f"   • Affinity: {evolved_path[1]:.4f}")
            print(f"   • Learning objects: {[lo.get('name') for lo in evolved_path[2]]}")
            
            # Choose the best path between original and evolved
            if evolved_affinity > original_affinity:
                improvement_percentage = ((evolved_affinity/original_affinity)-1)*100
                print(f"\n✅ Evolution successful! Improved by {improvement_percentage:.2f}%")
                final_path = evolved_path
                final_index = evolved_index
            else:
                print(f"\n⚠️ Evolution did not improve the path. Keeping original.")
                final_path = selected_path
                final_index = selected_index
        else:
            print("\n⚠️ No valid evolved paths were found. Keeping original path.")
            final_path = selected_path
            final_index = selected_index
    else:
        print("\n⚠️ No evolved chromosomes were created. Keeping original path.")
        final_path = selected_path
        final_index = selected_index
    
    # Return the filtered best path (only name and lo_id)
    filtered_los = [
        {"name": lo.get("name"), "lo_id": lo.get("lo_id")}
        for lo in final_path[2]
    ]
    final_result = {
        "path_index": final_index + 1,
        "learning_objects": filtered_los
    }
    
    print("\n📋 Final result:")
    print(final_result)
    print("\n======================= 🏁 IIA Algorithm Test Complete =======================")
    
    return final_result

if __name__ == "__main__":
    # Test parameters
    learner_email = "kareem@example.com"
    learning_goals = ["Searching"]
    knowledge_base = ["Introduction to Programming"]
    
    # Run the test
    test_iia_with_genetic_operators(learner_email, learning_goals, knowledge_base, test_mode=True) 