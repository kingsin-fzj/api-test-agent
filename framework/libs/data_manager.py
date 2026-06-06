"""Test data management"""

import yaml
import json
from pathlib import Path
from framework.utils.logger import TestLogger
from typing import Dict, Any, Optional

logger = TestLogger.get_logger(__name__)

class DataManager:
    def __init__(self, data_file: str):
        self.data_file = Path(data_file)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        if not self.data_file.exists():
            logger.warning(f"Data file not found: {self.data_file}")
            return {}
        try:
            if self.data_file.suffix in ['.yaml', '.yml']:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            elif self.data_file.suffix == '.json':
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                raise ValueError(f"Unsupported format: {self.data_file.suffix}")
        except Exception as e:
            logger.error(f"Failed to load: {e}")
            return {}
    
    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.replace('[', '.').replace(']', '').split('.')
        value = self.data
        try:
            for key in keys:
                if not key:
                    continue
                if isinstance(value, list):
                    value = value[int(key)]
                elif isinstance(value, dict):
                    value = value[key]
                else:
                    return default
            return value
        except (KeyError, IndexError, ValueError, TypeError):
            return default
    
    def get_all(self) -> Dict[str, Any]:
        return self.data
