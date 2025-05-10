# Barotrauma Schema Reverse Engineering

This document describes the approach and tools used for reverse engineering the Barotrauma XML schemas from the game's Content directory.

## Overview

Barotrauma uses XML files to define game content such as items, characters, afflictions, and more. By analyzing these files, we can create schemas that allow for validation and conversion of modding files across different formats.

The process is designed to be systematic and traceable, with careful tracking of file checksums to detect changes between game versions.

## Tools

### 1. Content Cataloging (`catalog_content_files.py`)

This utility scans the Barotrauma Content directory and creates a comprehensive catalog of all XML files, including:

- File path relative to the Content directory
- SHA-256 checksum for detecting changes
- File size and last modified timestamp
- Status tracking for reverse engineering progress

```bash
python tools/utilities/catalog_content_files.py --content-dir "x:/path/to/Barotrauma/Content" --output "docs/content_catalog.json"
```

### 2. Reverse Engineering Manager (`reverse_engineering_manager.py`)

This tool helps manage the reverse engineering process with functions to:

- List files and filter by status or pattern
- Get detailed information about files
- Mark files as reverse engineered
- Add metadata notes
- Verify checksums
- Analyze XML structure
- Generate statistics about progress

```bash
# List all files
python tools/utilities/reverse_engineering_manager.py list

# Get information about a specific file
python tools/utilities/reverse_engineering_manager.py info "Afflictions.xml"

# Mark a file as reverse engineered
python tools/utilities/reverse_engineering_manager.py mark "Afflictions.xml" --notes "Completed schema for afflictions" --schema "schemas/xml/Afflictions.xsd"

# Analyze XML structure
python tools/utilities/reverse_engineering_manager.py analyze "Afflictions.xml"

# Get progress statistics
python tools/utilities/reverse_engineering_manager.py stats
```

### 3. Content Categorization (`categorize_content.py`)

This utility analyzes the catalog and categorizes files based on:

- Root XML elements
- Directory structure
- Filename patterns

It then generates a comprehensive report and suggests a priority order for reverse engineering based on likely importance as core schema definitions.

```bash
python tools/utilities/categorize_content.py
```

## Methodology

1. **Catalog**: Start by cataloging all XML files and their checksums
2. **Categorize**: Group related files and identify core schema definitions
3. **Analyze**: Examine file structures to understand their schema
4. **Document**: Record findings, relationships, and special rules
5. **Implement**: Create XSD schemas based on the analysis
6. **Test**: Validate the schemas against existing content files
7. **Track**: Mark files as completed and keep notes on implementation details

## Legal Considerations

We don't copy or distribute the game's XML files; we only analyze their structure and document the schemas. This approach ensures our work is:

1. **Legal**: We're reverse engineering for interoperability purposes
2. **Ethical**: We're not redistributing copyrighted content
3. **Robust**: Our schemas will work with future game updates (with version checking)

## Tracking Progress

The content catalog maintains a record of reverse engineering progress:

- Files marked as "reverse engineered" (with timestamps)
- Metadata notes about special handling or complex behaviors
- Checksums to detect when game updates change file contents

The categorization report prioritizes files for reverse engineering based on their importance as core schema definitions, helping us focus efforts efficiently.
