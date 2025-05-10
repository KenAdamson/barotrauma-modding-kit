# Getting Started with Barotrauma Modding Kit

This guide will help you get started with creating mods for Barotrauma using this toolkit.

## Prerequisites

- [Barotrauma](https://store.steampowered.com/app/602960/Barotrauma/) installed
- Basic understanding of XML or YAML
- Python 3.6+ for running conversion tools

## Installation

1. Clone or download this repository
2. Make sure you have Python installed with the required dependencies:

   ```bash
   pip install pyyaml
   ```

## Basic Workflow

1. **Choose your format**: You can work with YAML (recommended for readability) or directly with XML
2. **Create your mod files**: Use the templates in the `templates/` directory as a starting point
3. **Validate your files**: Use the validation tools to ensure your files are correctly formatted
4. **Convert to XML**: If using YAML, convert to XML using the converter tools
5. **Install your mod**: Place the finished XML files in your Barotrauma LocalMods folder

## Directory Structure

- `schemas/`: XML and YAML schemas for validation
- `tools/`: Utilities for converting and validating mod files
- `templates/`: Example templates for common mod types
- `docs/`: Detailed documentation on mod creation

## Example

Creating a basic item mod:

1. Copy an appropriate template from `templates/items/`
2. Edit the YAML file with your item properties
3. Run the conversion tool:

   ```bash
   python tools/converters/yaml_to_xml.py your_item.yml
   ```

4. Place the resulting XML file in your Barotrauma LocalMods folder

See the `docs/examples/` directory for more comprehensive examples.
