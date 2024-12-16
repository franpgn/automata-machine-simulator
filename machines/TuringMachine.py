from machines.AbstractMachine import AbstractMachine


class TuringMachine(AbstractMachine):
    def __init__(self, blank_symbol='_', initial_state='q0', final_states=None, reject_states=None,
                 transition_function=None):
        super().__init__()
        self.blank_symbol = blank_symbol
        self.head_position = 0
        self.current_state = initial_state

        if final_states is not None:
            self.final_states = set(final_states)
        else:
            self.final_states = set()

        if reject_states is not None:
            self.reject_states = set(reject_states)
        else:
            self.reject_states = set()

        if transition_function is not None:
            self.transition_function = transition_function
        else:
            self.transition_function = {}

    def load_input(self, input_data):
        self.input_data = input_data
        self.memory_structures = [list(input_data if input_data else self.blank_symbol)]
        self.head_position = 0
        self.current_state = list(self.final_states)[0] if not self.current_state else self.current_state

    def step(self):
        tape = self.memory_structures[0]

        if self.head_position < 0:
            tape.insert(0, self.blank_symbol)
            self.head_position = 0
        elif self.head_position >= len(tape):
            tape.append(self.blank_symbol)

        current_symbol = tape[self.head_position]
        key = (self.current_state, current_symbol)

        if key in self.transition_function:
            new_state, write_symbol, direction = self.transition_function[key]
            tape[self.head_position] = write_symbol
            self.current_state = new_state
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1
            return True
        else:
            return False

    def is_accepting(self):
        return self.current_state in self.final_states

    def is_rejecting(self):
        return self.current_state in self.reject_states

    def run(self, max_steps=None):
        steps = 0
        while (max_steps is None or steps < max_steps) and not self.is_accepting() and not self.is_rejecting():
            if not self.step():
                break
            steps += 1
        return self.is_accepting()

    def reset(self):
        self.load_input(self.input_data)

    def get_config(self):
        return {
            'current_state': self.current_state,
            'head_position': self.head_position,
            'tape': ''.join(self.memory_structures[0])
        }
