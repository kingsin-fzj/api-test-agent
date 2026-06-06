"""Authentication handler"""

from framework.utils.logger import TestLogger
from typing import Dict, Any

logger = TestLogger.get_logger(__name__)

class AuthHandler:
    def __init__(self, auth_config: Dict[str, Any]):
        self.auth_config = auth_config
        self.auth_type = auth_config.get('type', 'custom')
        self.token = None
    
    def get_auth_header(self) -> Dict[str, str]:
        if self.auth_type == 'custom':
            return self._get_custom_auth()
        elif self.auth_type == 'jwt':
            return self._get_jwt_auth()
        elif self.auth_type == 'oauth2':
            return self._get_oauth2_auth()
        else:
            raise ValueError(f"Unsupported auth type: {self.auth_type}")
    
    def _get_custom_auth(self) -> Dict[str, str]:
        logger.info("Using custom authentication")
        return {}
    
    def _get_jwt_auth(self) -> Dict[str, str]:
        logger.info("Using JWT authentication")
        return {"Authorization": f"Bearer {self.token}"}
    
    def _get_oauth2_auth(self) -> Dict[str, str]:
        logger.info("Using OAuth2 authentication")
        return {"Authorization": f"Bearer {self.token}"}
