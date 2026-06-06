"""Test Case Generator - Generate RobotFramework test scripts"""

import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from framework.utils.logger import TestLogger
from jinja2 import Template

logger = TestLogger.get_logger(__name__)

ROBOT_TEST_TEMPLATE = '''*** Settings ***
Documentation    {{ api_name }} - Test Suite
Library    RequestsLibrary
Library    Collections
Library    String

Variables    config/variables.robot

*** Variables ***
${BASE_URL}    {{ base_url }}
${TIMEOUT}     {{ timeout }}

{% for scenario in scenarios %}
*** Test Cases ***
{{ scenario.name | replace(' ', '_') }}
    [Documentation]    {{ scenario.description }}
    [Tags]    {% for tag in scenario.tags %}{{ tag }}    {% endfor %}
    
    # Execute
    Log    Executing {{ scenario.name }}

{% endfor %}
*** Keywords ***
API Call
    [Arguments]    ${method}    ${endpoint}    @{args}
    [Documentation]    Make an API call
    Log    API Call: ${method} ${endpoint}
'''

class TestGenerator:
    """Generate RobotFramework test scripts from scenarios"""
    
    def __init__(self, output_dir: str = "tests/generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_robot_test(self, scenarios: List[Dict[str, Any]], 
                          api_info: Dict[str, Any],
                          config: Dict[str, Any]) -> str:
        """Generate Robot Framework test script from scenarios"""
        logger.info(f"Generating Robot Framework test script")
        
        # Create review batch directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_dir = self.output_dir / f"review_{timestamp}"
        batch_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate test file name
        api_name = api_info.get('name', 'test').lower().replace(' ', '_')
        test_file = batch_dir / f"test_{api_name}.robot"
        
        # Render template
        template = Template(ROBOT_TEST_TEMPLATE)
        content = template.render(
            api_name=api_info.get('name', 'API Test'),
            base_url=config.get('api', {}).get('base_url', 'http://localhost:8000'),
            timeout=config.get('api', {}).get('timeout', 30),
            scenarios=scenarios
        )
        
        # Write test file
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Generated test file: {test_file}")
        
        # Generate metadata file
        self._generate_metadata(batch_dir, api_info, scenarios)
        
        return str(test_file)
    
    def _generate_metadata(self, batch_dir: Path, api_info: Dict, scenarios: List[Dict]):
        """Generate metadata file for review"""
        import json
        
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'api_info': api_info,
            'scenarios': [
                {
                    'name': s.get('name'),
                    'type': s.get('type'),
                    'description': s.get('description'),
                    'tags': s.get('tags', [])
                }
                for s in scenarios
            ],
            'total_scenarios': len(scenarios),
            'status': 'pending_review'
        }
        
        metadata_file = batch_dir / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated metadata file: {metadata_file}")
    
    def generate_test_data_file(self, required_data: List[str], 
                               api_info: Dict) -> str:
        """Generate test data YAML file"""
        import yaml
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_file = self.output_dir / f"data_{api_info.get('name', 'test')}_{timestamp}.yaml"
        
        test_data = {
            'api': api_info.get('name', 'test'),
            'endpoint': api_info.get('endpoint', ''),
            'method': api_info.get('method', 'GET'),
            'test_cases': [
                {
                    'name': 'normal_case',
                    'data': {field: f"test_{field}" for field in required_data}
                },
                {
                    'name': 'exception_case',
                    'data': {field: "invalid_" + field for field in required_data}
                }
            ]
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            yaml.dump(test_data, f, default_flow_style=False, allow_unicode=True)
        
        logger.info(f"Generated test data file: {data_file}")
        return str(data_file)
