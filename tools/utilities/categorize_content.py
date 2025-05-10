"""
Categorize Barotrauma Content Files

This script analyzes the catalog of XML files and categorizes them based on
their root elements, structure, and file paths to provide a more organized
approach to the reverse engineering process.
"""

import os
import json
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Set, Tuple


def load_catalog(catalog_file: str) -> Dict[str, Any]:
    """
    Load the catalog from the JSON file
    
    Args:
        catalog_file: Path to the catalog JSON file
        
    Returns:
        Catalog dictionary
    """
    try:
        with open(catalog_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading catalog: {e}")
        return {"metadata": {}, "files": {}}


def get_xml_root_element(xml_file: str, content_dir: str) -> Tuple[str, Dict[str, str]]:
    """
    Get the root element of an XML file
    
    Args:
        xml_file: Path to the XML file (relative to Content directory)
        content_dir: Path to the Barotrauma Content directory
        
    Returns:
        Tuple of (root_element_name, root_attributes)
    """
    try:
        full_path = os.path.join(content_dir, xml_file)
        if not os.path.exists(full_path):
            return ("unknown", {})
            
        tree = ET.parse(full_path)
        root = tree.getroot()
        return (root.tag, root.attrib)
    except Exception as e:
        print(f"Error parsing XML file {xml_file}: {e}")
        return ("error", {})


def categorize_by_root_element(catalog: Dict[str, Any], content_dir: str) -> Dict[str, List[str]]:
    """
    Categorize XML files by their root element
    
    Args:
        catalog: The catalog dictionary
        content_dir: Path to the Barotrauma Content directory
        
    Returns:
        Dictionary mapping root elements to lists of file paths
    """
    root_element_map = defaultdict(list)
    print("Categorizing files by root element...")
    
    total_files = len(catalog["files"])
    for i, (file_path, info) in enumerate(catalog["files"].items()):
        if i % 50 == 0 and i > 0:
            print(f"  Processed {i}/{total_files} files...")
            
        root_element, _ = get_xml_root_element(file_path, content_dir)
        root_element_map[root_element].append(file_path)
    
    return dict(root_element_map)


def categorize_by_directory(catalog: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Categorize XML files by their directory structure
    
    Args:
        catalog: The catalog dictionary
        
    Returns:
        Dictionary mapping directories to lists of file paths
    """
    directory_map = defaultdict(list)
    
    for file_path in catalog["files"]:
        directory = os.path.dirname(file_path)
        if not directory:
            directory = "root"  # Files in the root directory
        directory_map[directory].append(file_path)
    
    return dict(directory_map)


def categorize_by_filename_pattern(catalog: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Categorize XML files by common filename patterns
    
    Args:
        catalog: The catalog dictionary
        
    Returns:
        Dictionary mapping patterns to lists of file paths
    """
    pattern_map = defaultdict(list)
    
    # Define some common patterns to look for
    patterns = {
        "items": ["item", "items", "weapon", "tool"],
        "characters": ["character", "human", "monster", "npc"],
        "locations": ["location", "outpost", "level", "map", "submarine"],
        "events": ["event", "mission", "campaign"],
        "afflictions": ["affliction", "status", "effect"],
        "tutorials": ["tutorial"],
        "skills": ["skill", "talent", "ability"],
        "ui": ["ui", "interface", "hud", "gui"]
    }
    
    for file_path in catalog["files"]:
        filename = os.path.basename(file_path).lower()
        
        # Check if the filename matches any pattern
        matched = False
        for category, keywords in patterns.items():
            for keyword in keywords:
                if keyword in filename:
                    pattern_map[category].append(file_path)
                    matched = True
                    break
            if matched:
                break
                
        # If no pattern matches, put in "other" category
        if not matched:
            pattern_map["other"].append(file_path)
    
    return dict(pattern_map)


def suggest_schema_priorities(categorized_files: Dict[str, Dict[str, List[str]]]) -> List[str]:
    """
    Suggest a priority order for reverse engineering schemas
    based on the categorization
    
    Args:
        categorized_files: Dictionary with different categorizations
        
    Returns:
        List of file paths in suggested priority order
    """
    # Define priority categories (these are likely to be core schema definitions)
    priority_roots = ["Items", "Character", "Affliction", "Location", "Event", "Submarine", "Job"]
    priority_dirs = ["root", "Items", "Characters", "Submarines", "Missions"]
    priority_patterns = ["items", "characters", "locations", "afflictions"]
    
    # Files that match multiple priority criteria will be ranked higher
    file_scores = defaultdict(int)
    
    # Score files based on root element
    for root, files in categorized_files["by_root"].items():
        score = 5 if root in priority_roots else 1
        for file in files:
            file_scores[file] += score
    
    # Score files based on directory
    for directory, files in categorized_files["by_directory"].items():
        for priority_dir in priority_dirs:
            if priority_dir in directory:
                for file in files:
                    file_scores[file] += 3
                break
    
    # Score files based on filename pattern
    for pattern, files in categorized_files["by_pattern"].items():
        score = 3 if pattern in priority_patterns else 1
        for file in files:
            file_scores[file] += score
    
    # Files in the root directory with simple names are often core definitions
    for file, score in list(file_scores.items()):
        filename = os.path.basename(file)
        if os.path.dirname(file) == "" and len(filename.split(".")[0]) < 15:
            file_scores[file] += 5
    
    # Sort files by score in descending order
    sorted_files = sorted(file_scores.items(), key=lambda x: x[1], reverse=True)
    
    return [file for file, _ in sorted_files]


def create_category_report(categorized_files: Dict[str, Dict[str, List[str]]], 
                          priority_files: List[str], output_file: str) -> None:
    """
    Create a detailed report of the categorization and priority suggestions
    
    Args:
        categorized_files: Dictionary with different categorizations
        priority_files: List of files in priority order
        output_file: Path to save the report
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Barotrauma Content File Categorization Report\n\n")
        
        # Write summary
        total_files = len(priority_files)
        f.write(f"## Summary\n\n")
        f.write(f"Total XML files: {total_files}\n\n")
        
        # Write root element categorization
        f.write(f"## Categorization by Root Element\n\n")
        for root, files in sorted(categorized_files["by_root"].items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"### {root} ({len(files)} files)\n\n")
            for file in sorted(files)[:10]:  # List first 10 files
                f.write(f"- `{file}`\n")
            if len(files) > 10:
                f.write(f"- ... and {len(files) - 10} more files\n")
            f.write("\n")
        
        # Write directory categorization (just top-level directories)
        f.write(f"## Categorization by Directory\n\n")
        top_dirs = {}
        for directory, files in categorized_files["by_directory"].items():
            top_dir = directory.split('/', 1)[0] if '/' in directory else directory
            if top_dir not in top_dirs:
                top_dirs[top_dir] = []
            top_dirs[top_dir].extend(files)
        
        for directory, files in sorted(top_dirs.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"### {directory} ({len(files)} files)\n\n")
            # Only list a few examples
            for file in sorted(files)[:5]:
                f.write(f"- `{file}`\n")
            if len(files) > 5:
                f.write(f"- ... and {len(files) - 5} more files\n")
            f.write("\n")
        
        # Write pattern categorization
        f.write(f"## Categorization by Filename Pattern\n\n")
        for pattern, files in sorted(categorized_files["by_pattern"].items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"### {pattern} ({len(files)} files)\n\n")
            for file in sorted(files)[:10]:
                f.write(f"- `{file}`\n")
            if len(files) > 10:
                f.write(f"- ... and {len(files) - 10} more files\n")
            f.write("\n")
        
        # Write priority list
        f.write(f"## Suggested Schema Reverse Engineering Priority\n\n")
        f.write("The following files are suggested as priorities for reverse engineering, based on their likely importance as core schema definitions:\n\n")
        for i, file in enumerate(priority_files[:50]):  # List top 50 priority files
            f.write(f"{i+1}. `{file}`\n")
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description='Categorize Barotrauma XML files for schema reverse engineering')
    parser.add_argument('--catalog', '-c', default='docs/content_catalog.json',
                       help='Path to the catalog JSON file')
    parser.add_argument('--content-dir', '-d', default='x:/steam_library/steamapps/common/Barotrauma/Content',
                       help='Path to the Barotrauma Content directory')
    parser.add_argument('--output', '-o', default='docs/content_categorization.md',
                       help='Output file to save the categorization report')
    args = parser.parse_args()
    
    # Load the catalog
    catalog = load_catalog(args.catalog)
    if not catalog["files"]:
        print("Error: No files found in the catalog.")
        return
    
    # Categorize files
    by_root = categorize_by_root_element(catalog, args.content_dir)
    by_directory = categorize_by_directory(catalog)
    by_pattern = categorize_by_filename_pattern(catalog)
    
    categorized_files = {
        "by_root": by_root,
        "by_directory": by_directory,
        "by_pattern": by_pattern
    }
    
    # Suggest priorities
    priority_files = suggest_schema_priorities(categorized_files)
    
    # Create report
    create_category_report(categorized_files, priority_files, args.output)
    print(f"Categorization report saved to {args.output}")
    
    # Create a prioritized list file for easy reference
    priority_list_file = os.path.splitext(args.output)[0] + "_priority_list.txt"
    with open(priority_list_file, 'w', encoding='utf-8') as f:
        for file in priority_files:
            f.write(f"{file}\n")
    print(f"Priority list saved to {priority_list_file}")


if __name__ == "__main__":
    main()
