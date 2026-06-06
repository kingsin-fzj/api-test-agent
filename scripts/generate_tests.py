#!/usr/bin/env python
"""Generate automated test scripts using AI Agent"""

import argparse
import sys
import yaml
from pathlib import Path
from agent.analyzer import APIAnalyzer
from agent.scenario_designer import ScenarioDesigner
from agent.generator import TestGenerator
from agent.data_identifier import DataIdentifier
from framework.utils.logger import TestLogger

# Configure logging
TestLogger.configure(log_level="INFO", log_file="logs/agent.log")
logger = TestLogger.get_logger(__name__)

def load_config(env: str = 'dev') -> dict:
    """Load configuration for environment"""
    config_file = Path(f"config/{env}.yaml")
    if not config_file.exists():
        logger.error(f"Config file not found: {config_file}")
        sys.exit(1)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_from_description(description: str, env: str = 'dev'):
    """Generate test script from API description"""
    logger.info("="*60)
    logger.info("API Test Agent - Test Generation")
    logger.info("="*60)
    
    config = load_config(env)
    
    # Step 1: Analyze API
    logger.info("\n[Step 1] Analyzing API...")
    analyzer = APIAnalyzer()
    api_info = analyzer.analyze_description(description)
    logger.info(f"API analyzed: {api_info['name']}")
    
    # Step 2: Identify dependencies
    logger.info("\n[Step 2] Identifying dependencies...")
    dependencies = analyzer.identify_dependencies(api_info)
    for dep in dependencies:
        logger.info(f"  - {dep['type']}: {dep['method']} {dep['endpoint']}")
    
    # Step 3: Design scenarios
    logger.info("\n[Step 3] Designing test scenarios...")
    designer = ScenarioDesigner()
    scenarios = designer.design_scenarios(api_info, dependencies)
    for i, scenario in enumerate(scenarios, 1):
        logger.info(f"  {i}. [{scenario['type']}] {scenario['name']}")
    
    # Step 4: Identify test data
    logger.info("\n[Step 4] Identifying test data requirements...")
    data_identifier = DataIdentifier()
    data_requirements = data_identifier.identify_data_requirements(api_info, scenarios)
    logger.info(f"  - Required fields: {data_requirements['required_fields']}")
    logger.info(f"  - Preparation steps: {len(data_requirements['preparation_steps'])}")
    
    # Step 5: Generate test script
    logger.info("\n[Step 5] Generating test script...")
    generator = TestGenerator()
    test_file = generator.generate_robot_test(scenarios, api_info, config)
    logger.info(f"Test file generated: {test_file}")
    
    # Step 6: Generate test data
    logger.info("\n[Step 6] Generating test data...")
    data_file = generator.generate_test_data_file(
        data_requirements['required_fields'],
        api_info
    )
    logger.info(f"Data file generated: {data_file}")
    
    logger.info("\n" + "="*60)
    logger.info("Test generation completed!")
    logger.info("="*60)
    logger.info(f"\nNext steps:")
    logger.info(f"1. Review the generated test: {test_file}")
    logger.info(f"2. Modify as needed")
    logger.info(f"3. Run: python scripts/review_tests.py --approve <review_dir>")
    logger.info("")

def main():
    parser = argparse.ArgumentParser(
        description="AI Agent for generating automated test scripts"
    )
    parser.add_argument(
        '--type',
        choices=['description', 'openapi', 'interactive'],
        default='description',
        help='Input type'
    )
    parser.add_argument(
        '--input',
        help='Input data (description, file path, or URL)'
    )
    parser.add_argument(
        '--env',
        choices=['dev', 'test', 'prod'],
        default='dev',
        help='Environment configuration'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode'
    )
    
    args = parser.parse_args()
    
    if args.interactive or (not args.input and not args.type == 'interactive'):
        # Interactive mode
        print("\n" + "="*60)
        print("API Test Agent - Interactive Mode")
        print("="*60)
        print("\nEnter API description (e.g.):")
        print('  "DELETE /api/auth, params: sign, username, returns: user_id"')
        print()
        description = input("API Description: ").strip()
        
        if not description:
            logger.error("API description cannot be empty")
            sys.exit(1)
        
        generate_from_description(description, args.env)
    else:
        generate_from_description(args.input, args.env)

if __name__ == '__main__':
    main()
