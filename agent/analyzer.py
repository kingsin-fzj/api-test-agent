"""API Analyzer - Understand API business logic"""

import json
import re
from typing import Dict, List, Any, Optional
from framework.utils.logger import TestLogger

logger = TestLogger.get_logger(__name__)

class APIAnalyzer:
    """Analyze API specifications and business logic"""
    
    def __init__(self):
        self.api_info = {}
        self.operations = []
        self.dependencies = []
    
    def analyze_description(self, description: str) -> Dict[str, Any]:
        """Analyze API from text description"""
        logger.info(f"Analyzing description: {description}")
        
        api_info = {}
        
        # Extract API name
        name_match = re.search(r'^([^:\uff1a]+)', description)
        if name_match:
            api_info['name'] = name_match.group(1).strip()
        
        # Extract HTTP method and endpoint
        method_match = re.search(r'(GET|POST|PUT|DELETE|DEL|PATCH|HEAD|OPTIONS)\s+(/[^,\uff0c]*)', description)
        if method_match:
            method = method_match.group(1)
            api_info['method'] = 'DELETE' if method == 'DEL' else method
            api_info['endpoint'] = method_match.group(2).strip()
        
        # Extract parameters
        params_match = re.search(r'\u53c2\u6570[\uff1a:]*([^,\uff0c]+)', description)
        if params_match:
            params_str = params_match.group(1).strip()
            api_info['params'] = [p.strip() for p in re.split(r'[,\uff0c]', params_str)]
        
        # Extract returns
        returns_match = re.search(r'\u8fd4\u56de[\uff1a:]*([^,\uff0c\u5f02]*)', description)
        if returns_match:
            returns_str = returns_match.group(1).strip()
            api_info['returns'] = [r.strip() for r in re.split(r'[,\uff0c]', returns_str)]
        
        # Extract expected status code
        code_match = re.search(r'(\u72b6\u6001\u7801|code)[\uff1a:]*([0-9]+)', description)
        if code_match:
            api_info['expected_code'] = int(code_match.group(2))
        
        # Extract exceptions
        exception_match = re.search(r'\u5f02\u5e38[\uff1a:]*([^,\uff0c]*)', description)
        if exception_match:
            api_info['exceptions'] = [e.strip() for e in exception_match.group(1).split('\u3001')]
        
        logger.info(f"Extracted API info: {json.dumps(api_info, ensure_ascii=False)}")
        self.api_info = api_info
        return api_info
    
    def identify_dependencies(self, api_info: Dict) -> List[Dict[str, str]]:
        """Identify API dependencies and related operations"""
        logger.info("Identifying API dependencies")
        
        dependencies = []
        method = api_info.get('method', '').upper()
        endpoint = api_info.get('endpoint', '')
        
        # DELETE -> GET (verify deletion)
        if method == 'DELETE':
            get_endpoint = endpoint.replace('/api/auth', '/api/user')
            dependencies.append({
                'type': 'verify_deletion',
                'method': 'GET',
                'endpoint': get_endpoint,
                'description': 'Verify the resource was deleted'
            })
        
        # POST -> GET (verify creation)
        elif method == 'POST' and 'create' in api_info.get('name', '').lower():
            dependencies.append({
                'type': 'verify_creation',
                'method': 'GET',
                'endpoint': endpoint,
                'description': 'Verify the resource was created'
            })
        
        self.dependencies = dependencies
        return dependencies
    
    def get_api_info(self) -> Dict[str, Any]:
        """Get analyzed API information"""
        return {
            'api_info': self.api_info,
            'dependencies': self.dependencies
        }
