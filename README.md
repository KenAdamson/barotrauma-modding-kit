# Barotrauma Modding Kit

This repository contains tools and resources for modding the game Barotrauma.

## Contents

- **Schemas/**: XML and YAML schemas for Barotrauma game objects
- **deploy/**: Deployment scripts and utilities
- **.windsurf/**: Configuration rules for modding

## References

- [LuaCsForBarotrauma Documentation](https://evilfactory.github.io/LuaCsForBarotrauma/lua-docs/)
- [Barotrauma Mod Documentation](https://regalis11.github.io/BaroModDoc/)
- [Steam Community Update](https://store.steampowered.com/news/app/602960/view/3178990340944884206)
- [Barotrauma Modding Documentation](https://github.com/Barotrauma-Modding/Documentation)
- [Official Barotrauma Wiki Guidelines](https://barotraumagame.com/wiki/Official_Barotrauma_Wiki:Guidelines)
- [LuaCsForBarotrauma GitHub](https://github.com/evilfactory/LuaCsForBarotrauma/blob/master/README.md)

## Setup

Barotrauma mods should be placed in the `LocalMods` folder of your Barotrauma installation.

## XML and YAML Schemas

XML schemas for various game object types are included in the `Schemas` directory. Always include correct references to the XSD files in your XML documents to ensure proper validation.

YAML schema files (YSD) are also maintained for YAML representation. The mapping between YAML element names and XML element names is maintained in `barotrama_mapping.yml`.
