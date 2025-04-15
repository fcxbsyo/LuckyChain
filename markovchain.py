class MarkovChain:
    def __init__(self):
        self.transition_matrix = [[0.25, 0.25, 0.25, 0.25] for _ in range(4)]
        self.current_state = 0

    def update_matrix(self, result):
        # do later: add logic to adjust probabilities based on result
        pass

    def get_next_state(self):
        import random
        probabilities = self.transition_matrix[self.current_state]
        self.current_state = random.choices(range(len(probabilities)), weights=probabilities)[0]
        return self.current_state
