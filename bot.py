class Bot:
    def __init__(self, machine, strategy='infinite'):
        self.machine = machine
        self.strategy_type = strategy
        self.session_data = []

    def auto_spin(self):
        while not self.decide_to_stop():
            self.machine.toggle_spinning()
            # will add sleep or step time if needed

    def decide_to_stop(self):
        return False  # Infinite strategy
