class MarkovChain:
    def __init__(self):
        self.transition_matrix = [
            [0.9, 0.1, 0.0, 0.0],
            [0.8, 0.2, 0.0, 0.0],
            [0.6, 0.3, 0.1, 0.0],
            [0.5, 0.3, 0.2, 0.0],
        ]
        self.current_state = 0

    def update_matrix(self, result):
        if result == "win":
            self.transition_matrix[self.current_state] = [0.1, 0.2, 0.4, 0.3]
        elif result == "jackpot":
            self.transition_matrix[self.current_state] = [0.05, 0.1, 0.35, 0.5]
        else:
            self.transition_matrix[self.current_state] = [0.4, 0.3, 0.2, 0.1]

    def get_next_state(self):
        import random
        probabilities = self.transition_matrix[self.current_state]
        self.current_state = random.choices(range(len(probabilities)), weights=probabilities)[0]
        return self.current_state
