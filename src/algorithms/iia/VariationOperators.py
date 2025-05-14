import random
from typing import List, Tuple, Dict, Any


def crossover_population(population: List[List[int]], crossover_probability: float = 0.8, always_crossover_for_testing: bool = False) -> List[List[int]]:
    """
    Apply single-point crossover to chromosomes in the population.
    
    Args:
        population (List[List[int]]): List of chromosomes (binary vectors)
        crossover_probability (float): Probability of applying crossover (default: 0.8)
        always_crossover_for_testing (bool): If True, ignores probability and always performs crossover (for testing)
        
    Returns:
        List[List[int]]: New population after crossover
    """
    if len(population) < 2:
        return population
    
    # Create a copy of the input population
    new_population = population.copy()
    n = len(population)
    
    # Create pairs for crossover
    for i in range(0, n - 1, 2):
        # Apply crossover with probability or always if testing flag is set
        if always_crossover_for_testing or random.random() < crossover_probability:
            parent1 = population[i].copy()
            parent2 = population[i + 1].copy()
            
            # Ensure parents have the same length
            if len(parent1) != len(parent2):
                print(f"⚠️ Skipping crossover due to different chromosome lengths: {len(parent1)} vs {len(parent2)}")
                continue
            
            # Determine number of concepts based on chromosome length 
            # (each concept is represented by 30 bits)
            if len(parent1) % 30 != 0:
                print(f"⚠️ Skipping crossover - chromosome length {len(parent1)} is not a multiple of 30")
                continue
                
            num_concepts = len(parent1) // 30
            
            # Choose a random concept as the crossover point
            # This ensures we don't break the 30-bit structure
            crossover_concept = random.randint(0, num_concepts - 1)
            crossover_point = crossover_concept * 30
            
            # Create offspring by swapping genetic material
            offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
            offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
            
            # Add offspring to the new population
            new_population.append(offspring1)
            new_population.append(offspring2)
            
            print(f"🧬 Applied crossover at concept {crossover_concept + 1} (bit {crossover_point})")
            print(f"   Parent 1: {parent1[:min(10, len(parent1))]}... (length: {len(parent1)})")
            print(f"   Parent 2: {parent2[:min(10, len(parent2))]}... (length: {len(parent2)})")
            print(f"   Offspring 1: {offspring1[:min(10, len(offspring1))]}... (length: {len(offspring1)})")
            print(f"   Offspring 2: {offspring2[:min(10, len(offspring2))]}... (length: {len(offspring2)})")
    
    return new_population


def mutate_population(population: List[List[int]], mutation_rate: float = 0.05) -> List[List[int]]:
    """
    Apply mutation to chromosomes in the population.
    Each concept (30-bits) should maintain exactly one '1' bit.
    
    Args:
        population (List[List[int]]): List of chromosomes (binary vectors)
        mutation_rate (float): Probability of mutation per concept (default: 0.05)
        
    Returns:
        List[List[int]]: New population after mutation
    """
    # Create a deep copy of the population to avoid modifying the original
    mutated_population = [chromosome.copy() for chromosome in population]
    
    mutations_applied = 0
    
    # For each chromosome in the population
    for i in range(len(mutated_population)):
        chromosome = mutated_population[i]
        
        # Skip if chromosome length is not a multiple of 30
        if len(chromosome) % 30 != 0:
            print(f"⚠️ Skipping mutation - chromosome length {len(chromosome)} is not a multiple of 30")
            continue
            
        num_concepts = len(chromosome) // 30
        
        # For each concept in the chromosome
        for concept_idx in range(num_concepts):
            # Apply mutation with probability mutation_rate
            if random.random() < mutation_rate:
                # Get the 30-bit segment for this concept
                start_bit = concept_idx * 30
                end_bit = start_bit + 30
                concept_bits = chromosome[start_bit:end_bit]
                
                # Find the current '1' bit position
                try:
                    current_one_idx = concept_bits.index(1)
                except ValueError:
                    # If no '1' bit found, set a random bit to 1
                    current_one_idx = -1
                
                # Choose a new random position that's different from the current one
                new_one_idx = current_one_idx
                while new_one_idx == current_one_idx:
                    new_one_idx = random.randint(0, 29)
                
                # Create a new concept segment with the '1' bit in the new position
                new_concept_bits = [0] * 30
                new_concept_bits[new_one_idx] = 1
                
                # Replace the old segment with the new one
                chromosome[start_bit:end_bit] = new_concept_bits
                
                mutations_applied += 1
                print(f"🧬 Mutated concept {concept_idx + 1}: moved '1' from bit {current_one_idx} to bit {new_one_idx}")
    
    if mutations_applied > 0:
        print(f"🧬 Applied {mutations_applied} mutations across the population")
    
    return mutated_population


def apply_genetic_operators(chromosomes: List[List[int]], 
                           top_n: int = 10, 
                           crossover_probability: float = 0.8,
                           mutation_rate: float = 0.05,
                           test_mode: bool = False) -> List[List[int]]:
    """
    Apply genetic operators (selection, crossover, mutation) to the population.
    
    Args:
        chromosomes (List[List[int]]): List of chromosomes
        top_n (int): Number of top chromosomes to select
        crossover_probability (float): Probability of applying crossover
        mutation_rate (float): Probability of mutation per concept
        test_mode (bool): If True, forces crossover to always happen (for testing)
        
    Returns:
        List[List[int]]: Evolved population
    """
    # Ensure we don't try to select more chromosomes than we have
    top_n = min(top_n, len(chromosomes))
    
    # Select top N chromosomes
    selected_chromosomes = chromosomes[:top_n]
    
    print(f"\n🧪 Applying genetic operators to evolve population:")
    print(f"   • Selected top {top_n} chromosomes")
    
    # Apply crossover
    print(f"   • Applying crossover with probability {crossover_probability}")
    crossover_result = crossover_population(selected_chromosomes, crossover_probability, always_crossover_for_testing=test_mode)
    
    # Apply mutation
    print(f"   • Applying mutation with rate {mutation_rate}")
    mutated_result = mutate_population(crossover_result, mutation_rate)
    
    print(f"   • Population evolved from {len(selected_chromosomes)} to {len(mutated_result)} chromosomes")
    
    return mutated_result


def reconstruct_learning_path(chromosome: List[int], 
                              all_los: List[Dict[str, Any]], 
                              concept_bit_length: int = 30) -> List[Dict[str, Any]]:
    """
    Reconstruct a learning path from a chromosome by mapping bits to learning objects.
    
    Args:
        chromosome (List[int]): The chromosome representing a learning path
        all_los (List[Dict[str, Any]]): All available learning objects
        concept_bit_length (int): Number of bits per concept (default: 30)
        
    Returns:
        List[Dict[str, Any]]: Learning objects corresponding to the chromosome
    """
    if not chromosome:
        return []
    
    # Determine the number of concepts based on chromosome length
    num_concepts = len(chromosome) // concept_bit_length
    
    # Collect the learning objects that match the chromosome
    selected_los = []
    
    for concept_idx in range(num_concepts):
        start_bit = concept_idx * concept_bit_length
        end_bit = start_bit + concept_bit_length
        concept_bits = chromosome[start_bit:end_bit]
        
        # Find the index of the '1' bit (if any)
        if 1 in concept_bits:
            lo_idx = concept_bits.index(1)
            # If we have LOs for this concept and index
            if concept_idx < len(all_los) and lo_idx < len(all_los[concept_idx]):
                selected_los.append(all_los[concept_idx][lo_idx])
    
    return selected_los 