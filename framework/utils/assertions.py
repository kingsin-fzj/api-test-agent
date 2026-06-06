"""Assertion utilities"""

from framework.utils.logger import TestLogger
logger = TestLogger.get_logger(__name__)

class AssertionHelper:
    """Assertion helper class"""
    
    @staticmethod
    def assert_status_code(response, expected_code, custom_code=None):
        actual_http_code = response.status_code
        assert actual_http_code == expected_code, f"Expected {expected_code}, got {actual_http_code}"
        logger.info(f"Status Code: {actual_http_code}")
        
        if custom_code is not None:
            try:
                response_data = response.json()
                actual_custom_code = response_data.get('status_code') or response_data.get('code')
                assert actual_custom_code == custom_code, f"Expected custom {custom_code}, got {actual_custom_code}"
                logger.info(f"Custom Code: {actual_custom_code}")
            except Exception as e:
                logger.error(f"Failed: {e}")
                raise
        return True
    
    @staticmethod
    def assert_response_contains(response, key_path, expected_value):
        try:
            response_data = response.json()
            actual_value = AssertionHelper._get_nested_value(response_data, key_path)
            assert actual_value == expected_value, f"Expected '{expected_value}', got '{actual_value}'"
            logger.info(f"{key_path} = {actual_value}")
            return True
        except Exception as e:
            logger.error(f"Assertion failed: {e}")
            raise
    
    @staticmethod
    def assert_response_contains_keyword(response, key_path, keyword):
        try:
            response_data = response.json()
            actual_value = AssertionHelper._get_nested_value(response_data, key_path)
            assert keyword in str(actual_value), f"Expected to contain '{keyword}', got '{actual_value}'"
            logger.info(f"{key_path} contains '{keyword}'")
            return True
        except Exception as e:
            logger.error(f"Assertion failed: {e}")
            raise
    
    @staticmethod
    def _get_nested_value(data, key_path):
        keys = key_path.replace('[', '.').replace(']', '').split('.')
        value = data
        for key in keys:
            if not key:
                continue
            if isinstance(value, list):
                value = value[int(key)]
            elif isinstance(value, dict):
                value = value[key]
            else:
                raise ValueError(f"Cannot access '{key}'")
        return value
