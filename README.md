# Barotrauma Modding Kit

This repository contains tools and resources for modding the game Barotrauma. It provides schemas, templates, conversion tools, and documentation to simplify the mod creation process.

## Directory Structure

```text
barotrauma-modding-kit/
├── docs/                        # Comprehensive documentation
│   ├── getting-started.md       # Quick start guide
│   ├── formats/                 # Documentation for each supported format
│   ├── modding-guide.md         # Detailed modding guide
│   └── examples/                # Example mods in different formats
├── schemas/                     # Schema definitions
│   ├── xml/                     # XML schemas (.xsd)
│   ├── yaml/                    # YAML schemas (.ysd)
│   └── mappings/                # Format mapping configurations
├── tools/                       # Utilities and converters
│   ├── converters/              # Format conversion tools
│   ├── validators/              # Validation utilities
│   └── utilities/               # Helper scripts and tools
├── templates/                   # Template files for common mod structures
│   ├── items/                   # Item templates
│   ├── afflictions/             # Affliction templates
│   └── content-packages/        # Content package templates
└── tests/                       # Test cases
```

## Quick Start

1. **Choose a template** from the `templates/` directory based on what you're creating
2. **Customize the template** according to your needs
3. **Validate your file** using the validation tools
4. **Convert to XML** if working with YAML or another format
5. **Place in your LocalMods folder** to test in-game

See the `docs/getting-started.md` file for detailed instructions.

## References

- [LuaCsForBarotrauma Documentation](https://evilfactory.github.io/LuaCsForBarotrauma/lua-docs/)
- [Barotrauma Mod Documentation](https://regalis11.github.io/BaroModDoc/)
- [Steam Community Update](https://store.steampowered.com/news/app/602960/view/3178990340944884206)
- [Barotrauma Modding Documentation](https://github.com/Barotrauma-Modding/Documentation)
- [Official Barotrauma Wiki Guidelines](https://barotraumagame.com/wiki/Official_Barotrauma_Wiki:Guidelines)
- [LuaCsForBarotrauma GitHub](https://github.com/evilfactory/LuaCsForBarotrauma/blob/master/README.md)

## Format Support

The toolkit currently supports working with:

- **XML** - Barotrauma's native format
- **YAML** - A more readable alternative

We plan to expand support to other formats in the future.
