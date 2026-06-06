"""API Client"""

import requests
from typing import Dict, Any, Optional
from framework.utils.logger import TestLogger
import json

logger = TestLogger.get_logger(__name__)

class APIClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.last_response = None
    
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        logger.info(f"GET {url}")
        if params:
            logger.debug(f"Params: {params}")
        response = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
        self._log_response(response)
        self.last_response = response
        return response
    
    def post(self, endpoint: str, json_data: Optional[Dict] = None, data: Optional[Any] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        logger.info(f"POST {url}")
        if json_data:
            logger.debug(f"JSON: {json.dumps(json_data, ensure_ascii=False)}")
        response = self.session.post(url, json=json_data, data=data, timeout=self.timeout, **kwargs)
        self._log_response(response)
        self.last_response = response
        return response
    
    def put(self, endpoint: str, json_data: Optional[Dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        logger.info(f"PUT {url}")
        if json_data:
            logger.debug(f"JSON: {json.dumps(json_data, ensure_ascii=False)}")
        response = self.session.put(url, json=json_data, timeout=self.timeout, **kwargs)
        self._log_response(response)
        self.last_response = response
        return response
    
    def delete(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        url = self._build_url(endpoint)
        logger.info(f"DELETE {url}")
        if params:
            logger.debug(f"Params: {params}")
        response = self.session.delete(url, params=params, timeout=self.timeout, **kwargs)
        self._log_response(response)
        self.last_response = response
        return response
    
    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith('http'):
            return endpoint
        base = self.base_url.rstrip('/')
        endpoint = endpoint.lstrip('/')
        return f"{base}/{endpoint}"
    
    def _log_response(self, response: requests.Response):
        logger.info(f"Status: {response.status_code}")
        try:
            response_data = response.json()
            logger.debug(f"Response: {json.dumps(response_data, ensure_ascii=False)}")
        except:
            logger.debug(f"Response: {response.text[:500]}")
    
    def set_headers(self, headers: Dict):
        self.session.headers.update(headers)
    
    def set_auth_header(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    def close(self):
        self.session.close()
