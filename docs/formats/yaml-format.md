# YAML Format for Barotrauma Modding

YAML provides a more readable and maintainable alternative to XML for creating Barotrauma mods. This document explains how to structure your YAML files for conversion to Barotrauma's XML format.

## Basic Structure

YAML files should be structured according to the schemas in the `schemas/yaml/` directory. The general structure follows the hierarchy of Barotrauma's XML format but with more readable syntax.

```yaml
# Example item in YAML format
items:
  - identifier: ExampleItem
    name: Example Item
    category: Equipment
    tags: tool, electrical
    description: A helpful example item
    sprite:
      texture: Items/example_item.png
      depth: 0.55
      sourcerect: [0, 0, 128, 128]
    price:
      basePrice: 100
      stores:
        - store: outpost
          multiplier: 1.0
        - store: miningoutpost
          multiplier: 1.2
```

## Mapping to XML

The YAML-to-XML converter uses mapping rules defined in `schemas/mappings/barotrauma_mapping.yml` to determine how YAML keys should be translated to XML elements and attributes.

### Common Mappings

- Nested objects generally become child elements
- Arrays become multiple elements of the same type
- Properties with simple values usually become attributes
- Special cases are handled by explicit mapping rules

## Schema Validation

Your YAML files should conform to the YAML schemas (YSD files) provided in the `schemas/yaml/` directory. These schemas define the allowed structure, required fields, and data types.

## Best Practices

1. **Use descriptive identifiers** - Choose clear, unique identifiers for your mods
2. **Follow the schema** - Validate your YAML against the provided schemas
3. **Use comments** - YAML allows comments (prefixed with `#`) to document your intentions
4. **Group related properties** - Keep related properties together for readability
5. **Be consistent with indentation** - YAML relies on consistent indentation (2 spaces recommended)

## Examples

For complete examples of YAML-formatted mods, see the templates in the `templates/` directory and examples in the `docs/examples/` directory.
