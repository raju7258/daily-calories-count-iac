import json
import os
from typing import Dict, Any

class ConfigLoader:
    @staticmethod
    def load_config(env_name: str) -> Dict[str, Any]:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "config", 
            f"{env_name}.json"
        )
        
        with open(config_path, 'r') as f:
            return json.load(f)