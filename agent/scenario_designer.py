"""Test Scenario Designer - Design test scenarios"""

import json
from typing import Dict, List, Any
from framework.utils.logger import TestLogger

logger = TestLogger.get_logger(__name__)

class ScenarioDesigner:
    """Design test scenarios based on API analysis"""
    
    def __init__(self):
        self.scenarios = []
    
    def design_scenarios(self, api_info: Dict, dependencies: List[Dict]) -> List[Dict[str, Any]]:
        """Design test scenarios"""
        logger.info(f"Designing test scenarios for: {api_info.get('name')}")
        
        scenarios = []
        
        # Normal case
        normal_scenario = self._design_normal_scenario(api_info)
        scenarios.append(normal_scenario)
        
        # Exception cases
        if 'exceptions' in api_info:
            for exception in api_info['exceptions']:
                exception_scenario = self._design_exception_scenario(api_info, exception)
                scenarios.append(exception_scenario)
        
        # Related verification scenarios
        for dependency in dependencies:
            related_scenario = self._design_related_scenario(api_info, dependency)
            scenarios.append(related_scenario)
        
        logger.info(f"Designed {len(scenarios)} scenarios")
        self.scenarios = scenarios
        return scenarios
    
    def _design_normal_scenario(self, api_info: Dict) -> Dict[str, Any]:
        method = api_info.get('method', '').upper()
        endpoint = api_info.get('endpoint', '')
        params = api_info.get('params', [])
        expected_code = api_info.get('expected_code', 200)
        
        scenario = {
            'type': 'normal',
            'name': f"{api_info.get('name', '')} - Normal case",
            'description': f"{method} {endpoint} should return status code {expected_code}",
            'tags': ['normal', 'smoke'],
            'setup_steps': [],
            'execute_steps': [
                {
                    'action': 'api_call',
                    'method': method,
                    'endpoint': endpoint,
                    'params': {param: f"${{{param}}}" for param in params}
                }
            ],
            'verify_steps': [
                {
                    'assertion': 'status_code_equals',
                    'expected': expected_code
                }
            ],
            'required_data': params
        }
        return scenario
    
    def _design_exception_scenario(self, api_info: Dict, exception: str) -> Dict[str, Any]:
        method = api_info.get('method', '').upper()
        endpoint = api_info.get('endpoint', '')
        params = api_info.get('params', [])
        
        scenario = {
            'type': 'exception',
            'name': f"{api_info.get('name', '')} - Exception: {exception}",
            'description': f"When {exception}",
            'tags': ['exception', 'negative'],
            'setup_steps': [],
            'execute_steps': [
                {
                    'action': 'api_call',
                    'method': method,
                    'endpoint': endpoint,
                    'params': {param: f"${{{param}}}" for param in params}
                }
            ],
            'verify_steps': [
                {
                    'assertion': 'response_contains_message',
                    'keyword': exception
                }
            ],
            'required_data': params,
            'note': f"This scenario tests the exception: {exception}"
        }
        return scenario
    
    def _design_related_scenario(self, api_info: Dict, dependency: Dict) -> Dict[str, Any]:
        method = api_info.get('method', '').upper()
        endpoint = api_info.get('endpoint', '')
        params = api_info.get('params', [])
        expected_code = api_info.get('expected_code', 200)
        
        scenario = {
            'type': 'related_verification',
            'name': f"{api_info.get('name', '')} - {dependency['type']}",
            'description': dependency['description'],
            'tags': ['related', 'integration'],
            'setup_steps': [],
            'execute_steps': [
                {
                    'action': 'api_call',
                    'method': method,
                    'endpoint': endpoint,
                    'params': {param: f"${{{param}}}" for param in params}
                }
            ],
            'verify_steps': [
                {
                    'assertion': 'status_code_equals',
                    'expected': expected_code
                },
                {
                    'action': 'api_call',
                    'method': dependency['method'],
                    'endpoint': dependency['endpoint'],
                    'params': {param: f"${{{param}}}" for param in params}
                },
                {
                    'assertion': 'response_contains_keyword',
                    'keyword': '\u65e0\u6b64\u7528\u6237'
                }
            ],
            'required_data': params
        }
        return scenario
    
    def get_scenarios(self) -> List[Dict[str, Any]]:
        """Get all designed scenarios"""
        return self.scenarios
