import json
import sys
import os
from machines.TuringMachine import TuringMachine

class Simulator:
    def __init__(self, input_json_path):
        self.input_json_path = input_json_path
        self.config = self._load_config()
        self.machine = self._create_machine(self.config)
    
    def _load_config(self):
        with open(self.input_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _parse_transition_function(self, tf_dict):
        parsed = {}
        for key, value in tf_dict.items():
            k = key.strip("()")
            state_read, symbol_read = k.split(',')
            state_read = state_read.strip()
            symbol_read = symbol_read.strip()
            
            new_state, write_symbol, direction = value
            parsed[(state_read, symbol_read)] = (new_state, write_symbol, direction)
        return parsed

    def _create_machine(self, config):
        machine_type = config.get('machine_type', '').lower()
        if machine_type == 'turing':
            transition_function = self._parse_transition_function(config.get('transition_function', {}))
            return TuringMachine(
                blank_symbol=config.get('blank_symbol', '_'),
                initial_state=config.get('initial_state', 'q0'),
                final_states=config.get('final_states', []),
                reject_states=config.get('reject_states', []),
                transition_function=transition_function
            )
        else:
            raise ValueError("Tipo de máquina não suportado: " + machine_type)
    
    def run(self):
        words = self.config.get('words', [])
        output_log = {
            "machine_type": self.config.get('machine_type'),
            "words_log": []
        }
        
        for word in words:
            self.machine.reset()
            self.machine.load_input(word)
            
            word_log = {
                "word": word,
                "steps": []
            }
            
            step_count = 0
            initial_config = self.machine.get_config()
            word_log["steps"].append({
                "step": step_count,
                "state": initial_config["current_state"],
                "tape": initial_config["tape"],
                "head_position": initial_config["head_position"]
            })
            
            while not self.machine.is_accepting() and not self.machine.is_rejecting():
                successful_step = self.machine.step()
                step_count += 1
                config = self.machine.get_config()
                word_log["steps"].append({
                    "step": step_count,
                    "state": config["current_state"],
                    "tape": config["tape"],
                    "head_position": config["head_position"]
                })
                if not successful_step:
                    break
            
            if self.machine.is_accepting():
                result = "accepted"
            elif self.machine.is_rejecting():
                result = "rejected"
            else:
                result = "halted_without_accept"
            
            word_log["result"] = result
            output_log["words_log"].append(word_log)

        os.makedirs("resources", exist_ok=True)
        with open("resources/output_log.json", "w", encoding="utf-8") as f:
            json.dump(output_log, f, indent=4, ensure_ascii=False)
        print("Log de execução salvo em resources/output_log.json")