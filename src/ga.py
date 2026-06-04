import numpy as np
import random

class GeneticAlgorithm:
    """
    The GeneticAlgorithm class manages the evolution of Neural Network weights.
    Enhanced with adaptive mechanisms to prevent genetic plateaus and promote
    Completionist strategies across multiple levels.
    """
    def __init__(self, population_size=150, initial_mutation_rate=0.22, crossover_rate=0.75, elite_size=12):
        """
        Optimized hyperparameters for neuroevolution in platformers:
        - population_size: 150 balances diversity and computation.
        - initial_mutation_rate: Starts higher for exploration, then decays.
        - elite_size: Protects top agents while maintaining diversity.
        """
        self.population_size = population_size
        self.mutation_rate = initial_mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.generation = 0

    def initialize_population(self, genome_size):
        """Generates the initial random population of genomes."""
        return [np.random.randn(genome_size).astype(np.float32) for _ in range(self.population_size)]

    def tournament_selection(self, population, fitnesses, tournament_size=6):
        """Selects a strong parent using tournament selection."""
        contestants = random.sample(range(len(population)), tournament_size)
        winner_idx = max(contestants, key=lambda idx: fitnesses[idx])
        return population[winner_idx]

    def crossover(self, parent1, parent2):
        """Blend crossover - better suited for neural network weights."""
        if random.random() < self.crossover_rate:
            alpha = random.uniform(0.3, 0.7)
            child = alpha * parent1 + (1 - alpha) * parent2
            return child.astype(np.float32)
        else:
            return parent1.copy()

    def mutate(self, genome):
        """Adaptive Gaussian mutation with decaying strength."""
        # Decay mutation strength over generations
        sigma = 0.75 * (0.965 ** self.generation)
        
        mutated = genome.copy()
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] += np.random.normal(0, sigma)
                
                # Occasional larger mutation for diversity
                if random.random() < 0.08:
                    mutated[i] += np.random.normal(0, sigma * 3.5)
        
        return mutated

    def evolve(self, population, fitnesses):
        """
        Creates the next generation using elitism, selection, crossover and mutation.
        """
        self.generation += 1
        
        # Sort population by fitness (descending)
        sorted_indices = np.argsort(fitnesses)[::-1]
        sorted_pop = [population[i] for i in sorted_indices]
        
        new_population = []
        
        # Elitism: Best agents advance unchanged
        for i in range(self.elite_size):
            new_population.append(sorted_pop[i].copy())
        
        # Generate remaining individuals
        while len(new_population) < self.population_size:
            parent1 = self.tournament_selection(population, fitnesses)
            parent2 = self.tournament_selection(population, fitnesses)
            
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            
            new_population.append(child)
        
        # Adaptive mutation rate decay
        if self.generation % 15 == 0:
            self.mutation_rate = max(0.08, self.mutation_rate * 0.92)
        
        return new_population