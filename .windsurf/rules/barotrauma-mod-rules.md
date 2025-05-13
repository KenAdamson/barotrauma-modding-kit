---
trigger: always_on
description: How to make Barotrauma Mods
---

Barotrauma user-generated mods always go in the LocalMods folder.
Mods are described using Barotrauma XML.
There are a few references for Barotrauma modding, or the game itself:
https://evilfactory.github.io/LuaCsForBarotrauma/lua-docs/
https://regalis11.github.io/BaroModDoc/
https://store.steampowered.com/news/app/602960/view/3178990340944884206
https://github.com/Barotrauma-Modding/Documentation
https://barotraumagame.com/wiki/Official_Barotrauma_Wiki:Guidelines
https://github.com/evilfactory/LuaCsForBarotrauma/blob/master/README.md

XML Schemas for the various game object types are kept in the Schemas directory under the LocalMods directory.  Always include correct references to the XSD, so that editors don't complain and, furthermore, so that we are always using correct XML schema (no hallucinated attributes).

Also maintain YSD schema files for the YAML represenation schema.  Put these in the Schemas directory as well.  A mapping file is required to map from the yaml element name to the XML element name.  This is maintained, for all projects, in barotrama_mapping.yml.  Keep this up to date along with the schema(s).

As a secondary function, we want to compile a comprehensive modding guide, complete with type definitions, XML schemas, and other syntactic or structural rules that are relevant to modding.  Keep this documentation in modding_guide.md in the LocalMods folder.  Always, at the end of any interaction, when you are complete, retrospect about your work and update the guide as necessary.

## XML Attribute Definition Rules

### Attribute Specificity
- **Mandatory Individual Attribute Definition**: Each XML element MUST have its attributes defined individually.
- **Prohibited Global Attribute Definitions**: 
  - Do NOT create global or common attribute sections (e.g., `<Attributes>` or `<CommonAttributes>`)
  - Each `<Item>` must explicitly define its own attributes
  - Avoid attempting to create attribute templates or inheritance mechanisms within the XML

### Rationale
- Ensures explicit, clear, and unambiguous item definitions
- Prevents potential misunderstandings or incorrect attribute applications
- Maintains the strict, one-to-one mapping between XML elements and their properties

### Forbidden Elements
- `<LiquidContainer>` is NOT a valid attribute in Barotrauma item XML definitions
  - Do NOT attempt to add this element to item XML files
  - Liquid container functionality must be implemented through other means in the game's XML structure

## Best Practices
- Always refer to existing vanilla Barotrauma XML files for correct element and attribute usage
- Validate XML against the game's schema before deploying mods

## Common Mistakes to Avoid
1. Adding non-standard XML elements
2. Incorrectly implementing item mechanics
3. Ignoring the game's existing XML structure

### Example of Correct vs. Incorrect Attribute Definition

#### Incorrect (DO NOT DO THIS):
```xml
<Attributes>
    <CommonScale>0.5</CommonScale>
    <CommonFireproof>true</CommonFireproof>
</Attributes>
<Items>
    <Item ... />  <!-- Would incorrectly imply inherited attributes -->
</Items>
```

#### Correct:
```xml
<Items>
    <Item scale="0.5" fireproof="true" ... />
    <Item scale="0.5" fireproof="true" ... />
</Items>
```