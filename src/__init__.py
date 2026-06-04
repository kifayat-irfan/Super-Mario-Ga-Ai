"""
Super Mario GA AI - Neuro-evolutionary Project

A modular neuroevolution framework using Genetic Algorithms
to evolve neural networks that play a Mario-style platformer.

Key Features:
- Deep Feed-Forward Neural Network
- Adaptive Genetic Algorithm
- Completionist fitness function (coins + progress + efficiency)
- Multi-level curriculum learning
- Scientific logging and visualization
"""

# Version and metadata
__version__ = "2.0.0"
__author__ = "Lead Architect Collaboration"

# Optional: Make key classes directly importable
from .neural_network import NeuralNetwork
from .ga import GeneticAlgorithm
from .trainer import Trainer
from .game import Game
from .player import Player

__all__ = [
    'NeuralNetwork',
    'GeneticAlgorithm',
    'Trainer',
    'Game',
    'Player'
]