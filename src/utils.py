import pickle
import csv
import os
import numpy as np

def save_genome(genome, filename=None):
    """
    Saves the genome (weights) to disk.
    Creates directory if it doesn't exist and returns the full path.
    """
    os.makedirs("saved_models", exist_ok=True)
    if filename is None:
        filename = "saved_models/best_genome.pkl"
    elif not filename.startswith("saved_models/"):
        filename = f"saved_models/{filename}"
        
    with open(filename, 'wb') as f:
        pickle.dump(genome, f)
    return filename

def load_genome(filename="saved_models/best_genome.pkl"):
    """Loads a saved genome from disk."""
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"Warning: Genome file {filename} not found.")
        return None

def log_stats(generation, best_fitness, avg_fitness, level_num, model_path):
    """
    Logs generation-level statistics to CSV for long-term analysis.
    """
    file_path = 'training_log.csv'
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Generation', 'Best_Fitness', 'Avg_Fitness', 'Level', 'Model_Path'])
        writer.writerow([generation, f"{best_fitness:.2f}", f"{avg_fitness:.2f}", level_num, model_path])

def log_agent_state(generation, inputs, output, action):
    """
    Detailed logging of the best agent's sensory inputs, network outputs,
    and chosen action. Essential for scientific behavior analysis.
    """
    file_path = 'agent_state_log.csv'
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                'Generation', 'Inputs', 'Neural_Output', 
                'Action_Taken', 'Input_Summary'
            ])
        
        # Convert to readable strings
        inputs_str = str([round(float(x), 4) for x in inputs])
        output_str = str([round(float(x), 4) for x in output])
        
        writer.writerow([
            generation, 
            inputs_str, 
            output_str, 
            int(action),
            f"MaxInput: {max(inputs):.3f}"
        ])