# Super Mario GA AI - Neuroevolution Project

A Neuro-evolutionary AI that learns to play Super Mario-style platformer using Genetic Algorithm + Neural Network. The AI evolves from random movement to a Completionist (collects coins + reaches goal efficiently).

![Training Progress](Figure_2.png)

## ✨ Features

- Deep Neural Network (16 inputs, 2 hidden layers)
- Genetic Algorithm with adaptive mutation & elitism
- Completionist Behavior — heavily rewards coin collection
- Multi-Level Curriculum (Level 1 → 2 → 3)
- God View — Watch 100 agents evolve simultaneously
- Scientific Logging — Detailed CSV logs for analysis
- Early Stopping & Model Snapshotting

## 🚀 Results

- Best Fitness: ~513,000+
- Successfully trained on Level 3
- AI learns to collect coins while avoiding enemies and reaching the goal

## 🛠 Tech Stack

- Python
- Pygame (Game Engine)
- NumPy (Neural Network)
- Matplotlib (Visualization)
- Genetic Algorithm (Custom)

## 📁 Project Structure

Super Mario GA/
├── main.py
├── trainer.py
├── game.py
├── neural_network.py
├── ga.py
├── player.py
├── saved_models/     # Best genomes
├── training_log.csv
└── agent_state_log.csv


## How to Run

```bash
pip install -r requirements.txt
python main.py

Press 2 → AI Training
Press 1 → Play as Human
