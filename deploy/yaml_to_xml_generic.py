import yaml
import os
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom

class YamlSchemaValidator:
    """
    Generic YAML Schema Validator that can work with any YSD schema
    """
    def __init__(self, schema_file=None):
        self.schema = None
        if schema_file:
            self.load_schema(schema_file)

    def load_schema(self, schema_file):
        """Load schema from file"""
        with open(schema_file, 'r') as f:
            self.schema = yaml.safe_load(f)
        return self.schema

    def validate(self, data, schema_path=None, context_path=""):
        """
        Validate YAML data against a schema

        Args:
            data: The YAML data to validate
            schema_path: Path within the schema to validate against (for nested validation)
            context_path: String representing the current path in the data (for error messages)
        """
        if self.schema is None:
            raise ValueError("No schema loaded. Call load_schema() first.")

        # Get the schema section to validate against
        schema = self.schema
        if schema_path:
            for path_part in schema_path.split('.'):
                if path_part in schema:
                    schema = schema[path_part]
                else:
                    raise ValueError(f"Schema path '{schema_path}' not found")

        # Validate based on schema type
        if isinstance(schema, dict) and "type" in schema:
            self._validate_by_type(data, schema, context_path)
        else:
            raise ValueError(f"Invalid schema at {schema_path if schema_path else 'root'}")

        return True

    def _validate_by_type(self, data, schema, path):
        """Validate data against a type definition in the schema"""
        schema_type = schema["type"]

        # Check required fields
        if schema.get("required", False) and data is None:
            raise ValueError(f"Missing required field: '{path}'")

        # Skip validation for null/None values that aren't required
        if data is None:
            return True

        # Validate type
        self._validate_type(data, schema_type, path)

        # Type-specific validation
        if schema_type == "array" and "items" in schema:
            self._validate_array(data, schema, path)
        elif schema_type == "object" and "properties" in schema:
            self._validate_object(data, schema, path)

        return True

    def _validate_type(self, data, expected_type, path):
        """Validate that data matches the expected type"""
        if expected_type == "string" and not isinstance(data, str):
            raise ValueError(f"Field '{path}' must be a string, got {type(data).__name__}")
        elif expected_type == "number" and not isinstance(data, (int, float)):
            raise ValueError(f"Field '{path}' must be a number, got {type(data).__name__}")
        elif expected_type == "integer" and not isinstance(data, int):
            raise ValueError(f"Field '{path}' must be an integer, got {type(data).__name__}")
        elif expected_type == "boolean" and not isinstance(data, bool):
            raise ValueError(f"Field '{path}' must be a boolean, got {type(data).__name__}")
        elif expected_type == "array" and not isinstance(data, list):
            raise ValueError(f"Field '{path}' must be an array, got {type(data).__name__}")
        elif expected_type == "object" and not isinstance(data, dict):
            raise ValueError(f"Field '{path}' must be an object, got {type(data).__name__}")

    def _validate_array(self, data, schema, path):
        """Validate array items against the schema"""
        for i, item in enumerate(data):
            item_path = f"{path}[{i}]"
            self._validate_by_type(item, schema["items"], item_path)

    def _validate_object(self, data, schema, path):
        """Validate object properties against the schema"""
        # Check for required properties
        if "required" in schema and isinstance(schema["required"], list):
            for req_prop in schema["required"]:
                if req_prop not in data:
                    raise ValueError(f"Missing required property '{req_prop}' in {path}")

        # Validate each property against its schema
        if "properties" in schema:
            for prop, prop_schema in schema["properties"].items():
                if prop in data:
                    prop_path = f"{path}.{prop}" if path else prop
                    self._validate_by_type(data[prop], prop_schema, prop_path)

class YamlToXmlConverter:
    """
    Generic YAML to XML Converter
    """
    def __init__(self, mapping_file=None):
        self.mapping = None
        if mapping_file:
            self.load_mapping(mapping_file)

    def load_mapping(self, mapping_file):
        """Load custom mapping rules"""
        with open(mapping_file, 'r') as f:
            self.mapping = yaml.safe_load(f)
        return self.mapping

    def convert(self, yaml_data, root_element=None):
        """
        Convert YAML data to XML

        Args:
            yaml_data: The parsed YAML data
            root_element: Optional name for the root element

        Returns:
            ElementTree object
        """
        # Create root element if specified, otherwise use the first key
        if root_element:
            root = ET.Element(root_element)
        else:
            # Try to get the first key as the root element
            if isinstance(yaml_data, dict) and len(yaml_data) > 0:
                first_key = next(iter(yaml_data.keys()))
                root = ET.Element(first_key)
                yaml_data = yaml_data[first_key]
            else:
                # Fallback to a generic root
                root = ET.Element("root")

        # Process the data
        self._process_node(root, yaml_data)

        return ET.ElementTree(root)

    def _process_node(self, parent, data):
        """Process a node in the YAML data and add it to the XML"""
        if isinstance(data, dict):
            self._process_dict(parent, data)
        elif isinstance(data, list):
            self._process_list(parent, data)
        else:
            # Text content for the element
            parent.text = str(data)

    def _process_dict(self, parent, data):
        """Process a dictionary node"""
        for key, value in data.items():
            # Handle attributes (keys starting with @)
            if key.startswith('@'):
                parent.set(key[1:], str(value))
            # Handle special text node
            elif key == '#text':
                parent.text = str(value)
            # Handle normal child elements
            else:
                # Apply mapping if available
                mapped_key = self._apply_mapping(key, parent.tag)

                if isinstance(value, list):
                    # Handle list of child elements
                    self._process_list(parent, value, mapped_key)
                elif isinstance(value, dict):
                    # Create element and process its children
                    child = ET.SubElement(parent, mapped_key)
                    self._process_dict(child, value)
                else:
                    # Simple element with a value
                    child = ET.SubElement(parent, mapped_key)
                    child.text = str(value)

    def _process_list(self, parent, data, element_name=None):
        """Process a list node"""
        for item in data:
            if isinstance(item, dict):
                # For dictionaries, try to find an element name
                item_name = element_name

                # If no element name provided, try to get one from the item
                if not item_name and '@element' in item:
                    item_name = item.pop('@element')

                # Create element with the determined name
                if item_name:
                    child = ET.SubElement(parent, item_name)
                    self._process_dict(child, item)
                else:
                    # If we can't determine an element name, add the items directly to parent
                    self._process_dict(parent, item)
            else:
                # For simple values, create elements with the provided name
                if element_name:
                    child = ET.SubElement(parent, element_name)
                    child.text = str(item)
                else:
                    # If no element name, use a generic "item" tag
                    child = ET.SubElement(parent, "item")
                    child.text = str(item)

    def _apply_mapping(self, key, parent_tag):
        """Apply any custom mapping rules to element names"""
        if self.mapping:
            # Try to find a mapping for this key under the parent tag
            parent_mappings = self.mapping.get(parent_tag, {})
            if key in parent_mappings:
                return parent_mappings[key]

            # Try global mappings
            global_mappings = self.mapping.get('*', {})
            if key in global_mappings:
                return global_mappings[key]

        # Default: return the original key
        return key

def main():
    if len(sys.argv) < 2:
        print("Usage: python yaml_to_xml.py <yaml_file> [output_xml_file] [schema_file] [mapping_file]")
        sys.exit(1)

    yaml_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else yaml_file.replace('.yml', '.xml').replace('.yaml', '.xml')
    schema_file = sys.argv[3] if len(sys.argv) > 3 else None
    mapping_file = sys.argv[4] if len(sys.argv) > 4 else None

    try:
        # Load the YAML file
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)

        # Validate if schema provided
        if schema_file:
            validator = YamlSchemaValidator(schema_file)
            validator.validate(yaml_data)
            print(f"YAML validation successful against {schema_file}")

        # Convert to XML
        converter = YamlToXmlConverter(mapping_file)
        xml_tree = converter.convert(yaml_data)

        # Format the XML with proper indentation
        xml_string = ET.tostring(xml_tree.getroot(), encoding='utf-8')
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8").decode('utf-8')

        # Remove empty lines (common issue with minidom)
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

        print(f"Successfully converted {yaml_file} to {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
