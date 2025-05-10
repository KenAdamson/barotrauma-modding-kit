"""
YAML Validator for Barotrauma modding files
"""
import yaml
import os
import sys
import argparse
from pathlib import Path

# We need to access the schema validator from the converter
sys.path.append(str(Path(__file__).parent.parent / "converters"))
from yaml_to_xml import YamlSchemaValidator

def validate_yaml_file(yaml_file, schema_file):
    """
    Validate a YAML file against a schema
    
    Args:
        yaml_file: Path to the YAML file to validate
        schema_file: Path to the schema file
    
    Returns:
        bool: True if validation succeeds, False otherwise
    """
    try:
        # Load YAML file
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
        
        # Initialize validator
        validator = YamlSchemaValidator(schema_file)
        
        # Validate data
        validator.validate(yaml_data)
        
        print(f"✓ Validation successful: {yaml_file}")
        return True
    
    except Exception as e:
        print(f"✗ Validation failed: {yaml_file}")
        print(f"  Error: {str(e)}")
        return False

def main():
    """
    Main entry point for the validator
    """
    parser = argparse.ArgumentParser(description='Validate Barotrauma YAML files against schemas')
    parser.add_argument('file', help='YAML file to validate')
    parser.add_argument('--schema', '-s', help='Schema file to validate against (auto-detected if not specified)')
    args = parser.parse_args()
    
    yaml_file = args.file
    schema_file = args.schema
    
    # Auto-detect schema if not specified
    if not schema_file:
        # Get the root directory of the toolkit
        toolkit_root = Path(__file__).parent.parent.parent
        schemas_dir = toolkit_root / "schemas" / "yaml"
        
        # Determine schema based on file content
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            
        # Check top-level keys to guess schema
        if 'items' in yaml_data:
            schema_file = str(schemas_dir / "barotrauma_items.ysd")
        elif 'afflictions' in yaml_data:
            schema_file = str(schemas_dir / "barotrauma_afflictions.ysd")
        else:
            print("Could not auto-detect schema. Please specify schema file with --schema")
            sys.exit(1)
        
        print(f"Auto-detected schema: {schema_file}")
    
    # Validate the file
    success = validate_yaml_file(yaml_file, schema_file)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
