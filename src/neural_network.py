import numpy as np

class NeuralNetwork:
    def __init__(self, input_size=16, hidden1_size=48, hidden2_size=32, output_size=4):
        """
        Initialize the neural network with a deeper architecture.
        We use 16 inputs to support richer environmental sensing.
        """
        self.input_size = input_size
        self.hidden1_size = hidden1_size
        self.hidden2_size = hidden2_size
        self.output_size = output_size
        
        # He initialization for better training with ReLU
        self.w1 = np.random.randn(input_size, hidden1_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden1_size))
        
        self.w2 = np.random.randn(hidden1_size, hidden2_size) * np.sqrt(2.0 / hidden1_size)
        self.b2 = np.zeros((1, hidden2_size))
        
        self.w3 = np.random.randn(hidden2_size, output_size) * np.sqrt(2.0 / hidden2_size)
        self.b3 = np.zeros((1, output_size))

    def forward(self, inputs):
        """
        Forward pass through the network.
        Returns raw output logits for action selection.
        """
        # Convert inputs to numpy array
        x = np.array(inputs, dtype=np.float32).reshape(1, -1)
        
        # Hidden Layer 1
        z1 = np.dot(x, self.w1) + self.b1
        a1 = np.maximum(z1, 0)  # ReLU activation
        
        # Hidden Layer 2
        z2 = np.dot(a1, self.w2) + self.b2
        a2 = np.maximum(z2, 0)  # ReLU activation
        
        # Output Layer (linear - no activation)
        z3 = np.dot(a2, self.w3) + self.b3
        return z3.flatten()

    def get_weights(self):
        """
        Flatten all weights and biases into a single array for the Genetic Algorithm.
        """
        weights = []
        weights.extend(self.w1.flatten())
        weights.extend(self.b1.flatten())
        weights.extend(self.w2.flatten())
        weights.extend(self.b2.flatten())
        weights.extend(self.w3.flatten())
        weights.extend(self.b3.flatten())
        return np.array(weights, dtype=np.float32)

    def set_weights(self, flat_weights):
        """
        Restore weights from a flat array produced by the Genetic Algorithm.
        Dynamically calculates sizes to support architecture changes.
        """
        idx = 0
        
        # Layer 1
        w1_size = self.input_size * self.hidden1_size
        self.w1 = flat_weights[idx:idx + w1_size].reshape(self.input_size, self.hidden1_size)
        idx += w1_size
        
        b1_size = self.hidden1_size
        self.b1 = flat_weights[idx:idx + b1_size].reshape(1, self.hidden1_size)
        idx += b1_size
        
        # Layer 2
        w2_size = self.hidden1_size * self.hidden2_size
        self.w2 = flat_weights[idx:idx + w2_size].reshape(self.hidden1_size, self.hidden2_size)
        idx += w2_size
        
        b2_size = self.hidden2_size
        self.b2 = flat_weights[idx:idx + b2_size].reshape(1, self.hidden2_size)
        idx += b2_size
        
        # Output Layer
        w3_size = self.hidden2_size * self.output_size
        self.w3 = flat_weights[idx:idx + w3_size].reshape(self.hidden2_size, self.output_size)
        idx += w3_size
        
        b3_size = self.output_size
        self.b3 = flat_weights[idx:idx + b3_size].reshape(1, self.output_size)

    def copy(self):
        """
        Create a deep copy of the network (useful for elitism).
        """
        new_nn = NeuralNetwork(self.input_size, self.hidden1_size, self.hidden2_size, self.output_size)
        new_nn.set_weights(self.get_weights().copy())
        return new_nn