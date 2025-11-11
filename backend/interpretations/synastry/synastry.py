import json
from pathlib import Path
from typing import Optional

class SynastryInterpreter:
    def __init__(self, score_file: Optional[str] = None):
        if score_file is None:
            score_file = Path(__file__).parent / "data" / "synastry_scores.json"
        self.scores = self._load_scores(score_file)

    def _load_scores(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def get_compatibility(self, sign1: str, sign2: str) -> Optional[float]:
        key = f"{sign1.capitalize()} + {sign2.capitalize()}"
        return self.scores.get(key)

# Example plugin interface
def register_interpreter(interpreter_class):
    # In a real system, this would add to a registry
    pass
