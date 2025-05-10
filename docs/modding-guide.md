# Comprehensive Barotrauma Modding Guide

This guide provides in-depth information about modding Barotrauma, covering important concepts, best practices, and technical details.

## Understanding Barotrauma's Mod System

Barotrauma mods are defined using XML files which describe game elements including items, characters, locations, and game mechanics. Mods are stored in the `LocalMods` directory and loaded when the game starts.

## Key Concepts

### Content Packages

Content packages define the metadata for your mod, including its name, description, and dependencies. Every mod requires a ContentPackage.xml file.

### Items

Items are physical objects that can be placed in the game world or inventory. They can range from simple tools to complex machines with multiple components.

### Afflictions

Afflictions are status effects that can be applied to characters, affecting their behavior, health, or abilities.

### Game Mechanics

Beyond adding content, mods can also modify game mechanics like physics properties, AI behavior, or environmental factors.

## XML Structure

Barotrauma's XML follows a specific structure for each element type. The schemas in the `schemas/xml/` directory provide formal definitions for these structures.

### Common Patterns

- Elements and attributes are typically camelCase
- IDs and identifiers should be unique across all mods
- References between elements use identifiers
- Nested elements define component relationships

## Using Alternative Formats

This toolkit allows you to write mods in alternative formats, like YAML, which are then converted to the required XML format.

### YAML Benefits

- More readable and concise syntax
- Reduced chance of syntax errors
- Better support for comments and documentation
- Easier maintenance for complex mods

See `docs/formats/yaml-format.md` for detailed information on using YAML.

## Testing and Debugging

1. Enable the developer console in Barotrauma
2. Use the console to check for errors when loading your mod
3. The game logs can provide additional information about mod loading issues
4. Test thoroughly in different game scenarios

## Distribution

Mods can be shared via:

- Steam Workshop
- Mod sharing websites
- Direct file sharing

Be sure to include a clear README with installation instructions and dependency information.

## Resources

- [Official Barotrauma Wiki](https://barotraumagame.com/wiki/Main_Page)
- [Barotrauma Modding Documentation](https://github.com/Barotrauma-Modding/Documentation)
- [Barotrauma Lua API Documentation](https://evilfactory.github.io/LuaCsForBarotrauma/lua-docs/)
