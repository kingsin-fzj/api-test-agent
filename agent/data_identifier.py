"""Test Data Identifier - Identify and prepare test data"""

import re
from typing import Dict, List, Any
from framework.utils.logger import TestLogger

logger = TestLogger.get_logger(__name__)

class DataIdentifier:
    """Identify required test data and preparation steps"""
    
    def __init__(self):
        self.required_data = []
        self.preparation_steps = []
    
    def identify_data_requirements(self, api_info: Dict, 
                                  scenarios: List[Dict]) -> Dict[str, Any]:
        """Identify test data requirements from API info and scenarios"""
        logger.info("Identifying test data requirements")
        
        requirements = {
            'required_fields': [],
            'preparation_steps': [],
            'cleanup_steps': []
        }
        
        # Extract required fields from API parameters
        if 'params' in api_info:
            requirements['required_fields'] = api_info['params']
        
        # Identify preparation steps from scenarios
        for scenario in scenarios:
            if scenario.get('type') == 'exception':
                prep_step = self._identify_prep_step_for_exception(
                    api_info, 
                    scenario.get('name', '')
                )
                if prep_step:
                    requirements['preparation_steps'].append(prep_step)
        
        # Add verification setup for DELETE operations
        if api_info.get('method') == 'DELETE':
            requirements['preparation_steps'].insert(0, {
                'action': 'create_resource',
                'description': 'Create a resource to delete',
                'api_endpoint': '/api/create',
                'returns': ['resource_id']
            })
            requirements['cleanup_steps'].append({
                'action': 'verify_deletion',
                'description': 'Verify the resource was deleted',
                'api_endpoint': '/api/get',
                'expect_result': 'not_found'
            })
        
        logger.info(f"Identified requirements: {len(requirements['required_fields'])} fields, {len(requirements['preparation_steps'])} prep steps")
        
        self.required_data = requirements
        return requirements
    
    def _identify_prep_step_for_exception(self, api_info: Dict, 
                                         scenario_name: str) -> Dict[str, Any]:
        """Identify preparation steps needed for exception scenarios"""
        if 'not found' in scenario_name.lower() or 'nonexistent' in scenario_name.lower():
            return {
                'action': 'skip_creation',
                'description': 'Do not create the resource for not found scenario'
            }
        return {}
    
    def get_requirements(self) -> Dict[str, Any]:
        """Get identified data requirements"""
        return self.required_data
