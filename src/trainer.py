import matplotlib.pyplot as plt
import numpy as np
import pygame
from src.game import Game
from src.ga import GeneticAlgorithm
from src.neural_network import NeuralNetwork
from src.utils import save_genome, log_stats, log_agent_state

class Trainer:
    """
    Final Optimized Version - Fast + High Quality + Proper Graph
    """
    def __init__(self):
        self.ga = GeneticAlgorithm(population_size=100, initial_mutation_rate=0.20)
        self.nn_template = NeuralNetwork()
        self.genome_size = len(self.nn_template.get_weights())
        self.population = self.ga.initialize_population(self.genome_size)
        
        self.generation = 1
        self.best_fitness_history = []
        self.avg_fitness_history = []
        
        self.best_fitness_ever = -float('inf')
        self.patience = 0
        self.max_patience = 70

    def calculate_fitness(self, player, status, frames):
        progress = player.rect.x / 2400.0
        coins = player.coins_collected
        win_bonus = 28000 if player.reached_goal else 0
        death_penalty = player.death_count * 7000
        stuck_penalty = player.stuck_counter * 380
        height_bonus = max(0, (250 - player.max_height_reached)) * 1100
        jump_bonus = min(player.jumps_made * 250, 7000)
        
        fitness = (
            coins * 1550 +
            progress * 5200 +
            win_bonus +
            height_bonus +
            jump_bonus -
            (frames * 0.075) -
            death_penalty -
            stuck_penalty
        )
        return max(fitness, 0.0)

    def train(self, render_mode=False):
        game = Game(mode='ai')
        pop_size = len(self.population)
        game.reset(population_size=pop_size)
        
        max_frames_per_gen = 1600
        render_interval = 40 if render_mode else 10000

        print("🚀 Training Started...")

        while self.generation <= 1000:
            brains = [NeuralNetwork() for _ in range(pop_size)]
            for i, genome in enumerate(self.population):
                brains[i].set_weights(genome)
            
            fitnesses = [0.0] * pop_size
            frame_counts = [0] * pop_size
            
            running = True
            frame = 0
            
            while running:
                pygame.event.pump()
                statuses = game.run_parallel_frame(brains)
                frame += 1
                
                if frame % 150 == 0:
                    best_idx = 0
                    inputs = game.get_ai_inputs(game.players[best_idx])
                    output = brains[best_idx].forward(inputs)
                    action = np.argmax(output)
                    log_agent_state(self.generation, inputs, output, action)
                
                all_done = True
                for i in range(pop_size):
                    if game.players[i].is_alive:
                        frame_counts[i] += 1
                        if statuses[i] != "ALIVE":
                            fitnesses[i] = self.calculate_fitness(game.players[i], statuses[i], frame_counts[i])
                        else:
                            all_done = False
                
                if frame % render_interval == 0 and render_mode:
                    game.draw()
                
                if all_done or frame > max_frames_per_gen:
                    for i in range(pop_size):
                        if game.players[i].is_alive:
                            fitnesses[i] = self.calculate_fitness(game.players[i], "ALIVE", frame_counts[i])
                    running = False
            
            # === EVOLUTION ===
            self.population = self.ga.evolve(self.population, fitnesses)
            best_fit = max(fitnesses)
            avg_fit = sum(fitnesses) / pop_size
            
            # === HISTORY FOR GRAPH ===
            self.best_fitness_history.append(best_fit)
            self.avg_fitness_history.append(avg_fit)
            
            if best_fit > self.best_fitness_ever:
                self.best_fitness_ever = best_fit
                self.patience = 0
                save_genome(self.population[0], f"gen_{self.generation}_best.pkl")
                save_genome(self.population[0], "best_genome.pkl")
            else:
                self.patience += 1
            
            log_stats(self.generation, best_fit, avg_fit, game.current_level_num, "saved")
            
            print(f"Gen {self.generation:3d} | Lvl {game.current_level_num} | Best: {best_fit:8.1f} | Avg: {avg_fit:6.1f} | Pat: {self.patience}/{self.max_patience} | Frames: {frame}")
            
            if self.patience >= self.max_patience and self.generation > 40:
                print("Early Stopping Activated.")
                break
            
            if best_fit > 13500 and game.current_level_num < 3:
                game.current_level_num += 1
                print(f"🎯 Level Up → {game.current_level_num}")
                game.reset(population_size=pop_size)
            
            self.generation += 1
            game.reset(population_size=pop_size)

        save_genome(self.population[0], "final_best_genome.pkl")
        print("✅ Training Completed Successfully!")
        self.plot_results()

    def plot_results(self):
        """Fixed & Improved Graph"""
        plt.figure(figsize=(12, 7))
        plt.plot(self.best_fitness_history, label="Best Fitness", color="lime", linewidth=2.5)
        plt.plot(self.avg_fitness_history, label="Average Fitness", color="cyan", linewidth=1.5, alpha=0.8)
        
        plt.title("Super Mario GA - Training Progress", fontsize=16)
        plt.xlabel("Generation", fontsize=12)
        plt.ylabel("Fitness Score", fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()