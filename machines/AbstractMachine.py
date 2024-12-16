from abc import ABC, abstractmethod


class AbstractMachine(ABC):
    def __init__(self):
        self.input_data = None
        self.memory_structures = []
        self.current_state = None
        self.final_states = set()
        self.reject_states = set()

    @abstractmethod
    def load_input(self, input_data):
        pass

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def is_accepting(self):
        pass

    @abstractmethod
    def is_rejecting(self):
        pass

    @abstractmethod
    def run(self, max_steps=None):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_config(self):
        pass
