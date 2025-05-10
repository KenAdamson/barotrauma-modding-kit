"""
Test suite for YAML validation and conversion
"""
import sys
import os
import unittest
from pathlib import Path

# Add the tools directory to the path
sys.path.append(str(Path(__file__).parent.parent / "tools"))
from converters.yaml_to_xml import YamlSchemaValidator
from validators.yaml_validator import validate_yaml_file

class TestYamlValidation(unittest.TestCase):
    """
    Test case for YAML validation
    """
    def setUp(self):
        """Set up test environment"""
        self.project_root = Path(__file__).parent.parent
        self.example_file = self.project_root / "docs" / "examples" / "medical_item" / "healing_spray.yml"
        self.schema_file = self.project_root / "schemas" / "yaml" / "barotrauma_items.ysd"
        
    def test_example_file_exists(self):
        """Test that the example file exists"""
        self.assertTrue(self.example_file.exists(), f"Example file {self.example_file} does not exist")
    
    def test_schema_file_exists(self):
        """Test that the schema file exists"""
        self.assertTrue(self.schema_file.exists(), f"Schema file {self.schema_file} does not exist")
    
    def test_file_validation(self):
        """Test validation of the example file"""
        if self.example_file.exists() and self.schema_file.exists():
            result = validate_yaml_file(str(self.example_file), str(self.schema_file))
            self.assertTrue(result, "Example file validation failed")

if __name__ == "__main__":
    unittest.main()
