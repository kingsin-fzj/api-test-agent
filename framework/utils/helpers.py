"""Helper utilities"""

import json
import time
from datetime import datetime

class TimeHelper:
    @staticmethod
    def get_timestamp():
        return int(time.time())
    
    @staticmethod
    def get_timestamp_ms():
        return int(time.time() * 1000)
    
    @staticmethod
    def get_datetime_string():
        return datetime.now().strftime("%Y%m%d_%H%M%S")

class JsonHelper:
    @staticmethod
    def pretty_print(data):
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def to_json(data):
        return json.dumps(data)
    
    @staticmethod
    def from_json(json_string):
        return json.loads(json_string)
