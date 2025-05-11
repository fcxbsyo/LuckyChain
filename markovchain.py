class MarkovChain:
    def __init__(self):
        # Transition matrix where each state has a probability distribution for the next state
        self.transition_matrix = [
            [0.2, 0.6, 0.2, 0.0],  # From state 0: slightly escalates
            [0.1, 0.4, 0.4, 0.1],  # From state 1: climbs fast
            [0.05, 0.2, 0.4, 0.35],  # From state 2: hard to return
            [0.0, 0.1, 0.3, 0.6]  # From state 3: almost stuck here
        ]
        self.current_state = 0

    def update_matrix(self, result):
        """
        Updates the transition matrix based on the result of the current spin.
        If the result is 'win', introduce a subtle loss by reducing the chance of winning.
        """
        if result == "win":
            # Slightly reduce the win chance (e.g., 80% win -> 75%, 20% loss -> 25%)
            self.transition_matrix[self.current_state] = [0.1, 0.3, 0.3, 0.3]  # increased loss probability
        elif result == "jackpot":
            self.transition_matrix[self.current_state] = [0.0, 0.1, 0.3, 0.6]  # straight to hardest
        else:
            self.transition_matrix[self.current_state] = [0.5, 0.3, 0.15, 0.05]  # only slightly easier

    def get_next_state(self):
        """
        Get the next state using weighted probabilities based on the current state
        with a slight bias towards losing.
        """
        import random
        probabilities = self.transition_matrix[self.current_state]
        self.current_state = random.choices(range(len(probabilities)), weights=probabilities)[0]
        return self.current_state

