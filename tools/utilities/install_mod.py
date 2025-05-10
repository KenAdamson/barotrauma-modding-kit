"""
Utility to convert a YAML mod to XML and install it to the Barotrauma LocalMods folder
"""
import sys
import os
import argparse
import shutil
from pathlib import Path

# Add the converter directory to the path
sys.path.append(str(Path(__file__).parent.parent / "converters"))
from yaml_to_xml import YamlToXmlConverter

def get_barotrauma_localmod_path():
    """
    Attempt to locate the Barotrauma LocalMods folder
    
    Returns:
        Path object to the LocalMods folder or None if not found
    """
    # Common locations for Steam installations
    if sys.platform == "win32":
        # Windows
        common_paths = [
            Path(os.path.expandvars("%PROGRAMFILES(X86)%/Steam/steamapps/common/Barotrauma/LocalMods")),
            Path(os.path.expandvars("%PROGRAMFILES%/Steam/steamapps/common/Barotrauma/LocalMods")),
            # Add more potential paths here
        ]
    elif sys.platform == "darwin":
        # macOS
        common_paths = [
            Path("~/Library/Application Support/Steam/steamapps/common/Barotrauma/LocalMods").expanduser(),
        ]
    else:
        # Linux
        common_paths = [
            Path("~/.steam/steam/steamapps/common/Barotrauma/LocalMods").expanduser(),
        ]
    
    # Check for existence of paths
    for path in common_paths:
        if path.exists():
            return path
    
    return None

def install_mod(yaml_file, output_dir=None, no_install=False):
    """
    Convert YAML mod to XML and install to LocalMods folder
    
    Args:
        yaml_file: Path to the YAML file
        output_dir: Optional custom output directory
        no_install: If True, only convert and don't install
    
    Returns:
        Path to the output XML file
    """
    # Load YAML file
    import yaml
    with open(yaml_file, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    
    # Determine the mod name from the filename if not in the YAML
    mod_name = Path(yaml_file).stem
    
    # Get project root
    toolkit_root = Path(__file__).parent.parent.parent
    
    # Initialize converter with the mapping file
    mapping_file = toolkit_root / "schemas" / "mappings" / "barotrauma_mapping.yml"
    converter = YamlToXmlConverter(str(mapping_file))
    
    # Convert YAML to XML
    xml_tree = converter.convert(yaml_data)
    
    # Determine output directory
    if output_dir:
        out_dir = Path(output_dir)
    elif no_install:
        out_dir = Path(yaml_file).parent
    else:
        # Use the LocalMods directory
        local_mods = get_barotrauma_localmod_path()
        if not local_mods:
            print("Could not find Barotrauma LocalMods directory. Please specify with --output-dir")
            sys.exit(1)
        out_dir = local_mods / mod_name
    
    # Create output directory if it doesn't exist
    os.makedirs(out_dir, exist_ok=True)
    
    # Save XML to file
    output_file = out_dir / f"{Path(yaml_file).stem}.xml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converter.to_string(xml_tree))
    
    print(f"✓ Converted {yaml_file} to {output_file}")
    
    if not no_install and output_dir is None:
        print(f"✓ Installed to Barotrauma LocalMods: {out_dir}")
    
    return output_file

def main():
    """
    Main entry point for the installer
    """
    parser = argparse.ArgumentParser(description='Convert and install Barotrauma YAML mods to XML')
    parser.add_argument('file', help='YAML file to convert and install')
    parser.add_argument('--output-dir', '-o', help='Custom output directory (instead of Barotrauma LocalMods)')
    parser.add_argument('--no-install', '-n', action='store_true', help="Don't install, just convert and save in the same directory")
    args = parser.parse_args()
    
    install_mod(args.file, args.output_dir, args.no_install)

if __name__ == "__main__":
    main()
