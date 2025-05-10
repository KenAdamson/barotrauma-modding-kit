"""
Reverse Engineering Manager

This utility helps manage the reverse engineering process of Barotrauma XML schemas.
It allows:
- Viewing the catalog of files
- Updating the status of files (reverse engineered or not)
- Adding metadata and notes to files
- Tracking progress
- Exporting schema definitions
"""

import os
import json
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import xml.etree.ElementTree as ET


class ReverseEngineeringManager:
    """
    Manages the reverse engineering process for Barotrauma XML files
    """
    
    def __init__(self, catalog_file: str, barotrauma_dir: str = None):
        """
        Initialize the manager with the catalog file and optional Barotrauma directory
        
        Args:
            catalog_file: Path to the catalog JSON file
            barotrauma_dir: Path to the Barotrauma Content directory (optional)
        """
        self.catalog_file = catalog_file
        self.barotrauma_dir = barotrauma_dir
        self.catalog = self._load_catalog()
        
    def _load_catalog(self) -> Dict[str, Any]:
        """
        Load the catalog from the JSON file
        
        Returns:
            Catalog dictionary
        """
        try:
            with open(self.catalog_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading catalog: {e}")
            # Return a basic structure if the file doesn't exist or is invalid
            return {
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "content_directory": self.barotrauma_dir or "",
                    "hash_algorithm": "sha256",
                    "total_files": 0
                },
                "files": {}
            }
            
    def _save_catalog(self) -> None:
        """
        Save the catalog to the JSON file
        """
        with open(self.catalog_file, 'w', encoding='utf-8') as f:
            json.dump(self.catalog, f, indent=2)
        print(f"Catalog saved to {self.catalog_file}")
            
    def list_files(self, status: Optional[bool] = None, pattern: Optional[str] = None) -> List[str]:
        """
        List files in the catalog, optionally filtered by status or pattern
        
        Args:
            status: Filter by reverse_engineered status (True, False, or None for all)
            pattern: Filter by file path pattern
            
        Returns:
            List of file paths
        """
        file_paths = []
        
        for file_path, info in self.catalog["files"].items():
            if status is not None and info["reverse_engineered"] != status:
                continue
                
            if pattern and pattern not in file_path:
                continue
                
            file_paths.append(file_path)
            
        return sorted(file_paths)
        
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific file
        
        Args:
            file_path: Path to the file (relative to Content directory)
            
        Returns:
            File information dictionary or None if not found
        """
        # Try the exact path
        if file_path in self.catalog["files"]:
            return self.catalog["files"][file_path]
            
        # Try with path normalization
        normalized_path = os.path.normpath(file_path).replace("\\", "/")
        for path in self.catalog["files"]:
            if os.path.normpath(path).replace("\\", "/") == normalized_path:
                return self.catalog["files"][path]
                
        return None
        
    def mark_reverse_engineered(self, file_path: str, status: bool = True, 
                               notes: Optional[str] = None, 
                               schema_path: Optional[str] = None) -> bool:
        """
        Mark a file as reverse engineered or not
        
        Args:
            file_path: Path to the file (relative to Content directory)
            status: Whether the file is reverse engineered
            notes: Optional notes about the reverse engineering
            schema_path: Optional path to the schema file created
            
        Returns:
            True if successful, False otherwise
        """
        file_info = self.get_file_info(file_path)
        if not file_info:
            print(f"File not found in catalog: {file_path}")
            return False
            
        file_info["reverse_engineered"] = status
        
        if notes:
            if "notes" not in file_info["metadata"]:
                file_info["metadata"]["notes"] = []
            file_info["metadata"]["notes"].append({
                "timestamp": datetime.now().isoformat(),
                "content": notes
            })
            
        if schema_path:
            file_info["metadata"]["schema_path"] = schema_path
            
        self._save_catalog()
        return True
        
    def add_metadata(self, file_path: str, key: str, value: Any) -> bool:
        """
        Add or update metadata for a file
        
        Args:
            file_path: Path to the file (relative to Content directory)
            key: Metadata key
            value: Metadata value
            
        Returns:
            True if successful, False otherwise
        """
        file_info = self.get_file_info(file_path)
        if not file_info:
            print(f"File not found in catalog: {file_path}")
            return False
            
        file_info["metadata"][key] = value
        self._save_catalog()
        return True
        
    def verify_checksum(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Verify the checksum of a file against the catalog
        
        Args:
            file_path: Path to the file (relative to Content directory)
            
        Returns:
            Tuple of (is_valid, current_checksum)
        """
        if not self.barotrauma_dir:
            print("Barotrauma directory not specified, can't verify checksum")
            return False, None
            
        file_info = self.get_file_info(file_path)
        if not file_info:
            print(f"File not found in catalog: {file_path}")
            return False, None
            
        full_path = os.path.join(self.barotrauma_dir, file_path)
        if not os.path.exists(full_path):
            print(f"File not found on disk: {full_path}")
            return False, None
            
        algorithm = file_info["algorithm"]
        expected_checksum = file_info["checksum"]
        
        hash_obj = hashlib.new(algorithm)
        with open(full_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                hash_obj.update(byte_block)
        
        current_checksum = hash_obj.hexdigest()
        is_valid = current_checksum == expected_checksum
        
        if not is_valid:
            print(f"Checksum mismatch for {file_path}")
            print(f"  Expected: {expected_checksum}")
            print(f"  Current:  {current_checksum}")
            
        return is_valid, current_checksum
        
    def analyze_xml_structure(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze the structure of an XML file to help with schema creation
        
        Args:
            file_path: Path to the file (relative to Content directory)
            
        Returns:
            Dictionary with analysis results
        """
        if not self.barotrauma_dir:
            print("Barotrauma directory not specified, can't analyze XML")
            return {}
            
        full_path = os.path.join(self.barotrauma_dir, file_path)
        if not os.path.exists(full_path):
            print(f"File not found on disk: {full_path}")
            return {}
            
        try:
            tree = ET.parse(full_path)
            root = tree.getroot()
            
            analysis = {
                "root_element": root.tag,
                "attributes": {},
                "child_elements": {},
                "element_counts": {}
            }
            
            # Process root attributes
            analysis["attributes"][root.tag] = list(root.attrib.keys())
            
            # Process all elements and their attributes recursively
            self._analyze_element(root, analysis["child_elements"], analysis["attributes"], analysis["element_counts"])
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing XML file {file_path}: {e}")
            return {}
            
    def _analyze_element(self, element: ET.Element, child_elements: Dict, all_attributes: Dict, element_counts: Dict) -> None:
        """
        Recursively analyze an XML element and its children
        
        Args:
            element: The XML element to analyze
            child_elements: Dictionary to store child element relationships
            all_attributes: Dictionary to store attributes for each element type
            element_counts: Dictionary to store counts of each element type
        """
        # Count this element
        if element.tag in element_counts:
            element_counts[element.tag] += 1
        else:
            element_counts[element.tag] = 1
        
        # Process children
        child_tags = []
        for child in element:
            if child.tag not in child_tags:
                child_tags.append(child.tag)
                
            # Process child's attributes
            if child.tag not in all_attributes:
                all_attributes[child.tag] = []
                
            for attr in child.attrib.keys():
                if attr not in all_attributes[child.tag]:
                    all_attributes[child.tag].append(attr)
                    
            # Recursively process this child
            self._analyze_element(child, child_elements, all_attributes, element_counts)
            
        # Store the child elements for this type
        if element.tag not in child_elements:
            child_elements[element.tag] = []
            
        for tag in child_tags:
            if tag not in child_elements[element.tag]:
                child_elements[element.tag].append(tag)
                
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the reverse engineering progress
        
        Returns:
            Dictionary with statistics
        """
        total_files = len(self.catalog["files"])
        reverse_engineered = 0
        file_types = {}
        
        for file_path, info in self.catalog["files"].items():
            if info["reverse_engineered"]:
                reverse_engineered += 1
                
            # Categorize by top-level directory
            parts = file_path.split('/', 1)
            category = parts[0] if len(parts) > 0 else "Other"
            
            if category not in file_types:
                file_types[category] = {
                    "total": 0,
                    "reverse_engineered": 0
                }
                
            file_types[category]["total"] += 1
            if info["reverse_engineered"]:
                file_types[category]["reverse_engineered"] += 1
                
        return {
            "total_files": total_files,
            "reverse_engineered": reverse_engineered,
            "completion_percentage": (reverse_engineered / total_files * 100) if total_files > 0 else 0,
            "categories": file_types
        }
        
    def export_xml_schema(self, file_path: str, output_path: str) -> bool:
        """
        Generate an XML schema definition (XSD) based on file analysis
        
        Args:
            file_path: Path to the XML file (relative to Content directory)
            output_path: Path to save the generated XSD file
            
        Returns:
            True if successful, False otherwise
        """
        analysis = self.analyze_xml_structure(file_path)
        if not analysis:
            return False
            
        # This would typically involve much more complex logic to generate a proper XSD
        # This is a simplified placeholder that would need to be expanded
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n\n')
                
                # Root element
                root_element = analysis["root_element"]
                f.write(f'  <xs:element name="{root_element}">\n')
                f.write('    <xs:complexType>\n')
                
                # Root attributes
                if root_element in analysis["attributes"] and analysis["attributes"][root_element]:
                    f.write('      <xs:attribute>\n')
                    for attr in analysis["attributes"][root_element]:
                        f.write(f'        <xs:attribute name="{attr}" type="xs:string"/>\n')
                    f.write('      </xs:attribute>\n')
                    
                # Child elements (simplified)
                if root_element in analysis["child_elements"] and analysis["child_elements"][root_element]:
                    f.write('      <xs:sequence>\n')
                    for child in analysis["child_elements"][root_element]:
                        f.write(f'        <xs:element name="{child}" type="xs:anyType" minOccurs="0" maxOccurs="unbounded"/>\n')
                    f.write('      </xs:sequence>\n')
                    
                f.write('    </xs:complexType>\n')
                f.write('  </xs:element>\n')
                f.write('</xs:schema>\n')
                
            # Update the catalog
            self.add_metadata(file_path, "schema_path", output_path)
            return True
            
        except Exception as e:
            print(f"Error exporting XML schema: {e}")
            return False
        

def main():
    parser = argparse.ArgumentParser(description='Manage the reverse engineering of Barotrauma XML schemas')
    parser.add_argument('--catalog', '-c', default='docs/content_catalog.json',
                       help='Path to the catalog JSON file')
    parser.add_argument('--barotrauma-dir', '-b', default='x:/steam_library/steamapps/common/Barotrauma/Content',
                       help='Path to the Barotrauma Content directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # List files command
    list_parser = subparsers.add_parser('list', help='List files in the catalog')
    list_parser.add_argument('--status', choices=['done', 'pending', 'all'], default='all',
                            help='Filter by reverse engineering status')
    list_parser.add_argument('--pattern', '-p', help='Filter by file path pattern')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get information about a file')
    info_parser.add_argument('file_path', help='Path to the file (relative to Content directory)')
    
    # Mark command
    mark_parser = subparsers.add_parser('mark', help='Mark a file as reverse engineered')
    mark_parser.add_argument('file_path', help='Path to the file (relative to Content directory)')
    mark_parser.add_argument('--status', choices=['done', 'pending'], default='done',
                           help='Reverse engineering status')
    mark_parser.add_argument('--notes', '-n', help='Notes about the reverse engineering')
    mark_parser.add_argument('--schema', '-s', help='Path to the schema file created')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze XML structure')
    analyze_parser.add_argument('file_path', help='Path to the file (relative to Content directory)')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Get statistics about reverse engineering progress')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export XML schema definition')
    export_parser.add_argument('file_path', help='Path to the file (relative to Content directory)')
    export_parser.add_argument('output_path', help='Path to save the generated XSD file')
    
    args = parser.parse_args()
    
    # Initialize the manager
    manager = ReverseEngineeringManager(args.catalog, args.barotrauma_dir)
    
    # Execute the command
    if args.command == 'list':
        status_map = {'done': True, 'pending': False, 'all': None}
        files = manager.list_files(status_map[args.status], args.pattern)
        print(f"Found {len(files)} {'files' if len(files) != 1 else 'file'}:")
        for file in files:
            info = manager.get_file_info(file)
            status = "✓" if info["reverse_engineered"] else "✗"
            print(f"  {status} {file}")
            
    elif args.command == 'info':
        info = manager.get_file_info(args.file_path)
        if info:
            print(f"File: {args.file_path}")
            print(f"  Status: {'Reverse Engineered' if info['reverse_engineered'] else 'Pending'}")
            print(f"  Checksum: {info['checksum']} ({info['algorithm']})")
            print(f"  Size: {info['size_bytes']} bytes")
            print(f"  Last Modified: {info['last_modified']}")
            
            if info["metadata"]:
                print("  Metadata:")
                for key, value in info["metadata"].items():
                    if key == "notes":
                        print("    Notes:")
                        for note in value:
                            print(f"      [{note['timestamp']}] {note['content']}")
                    else:
                        print(f"    {key}: {value}")
                        
            # Verify checksum
            valid, current = manager.verify_checksum(args.file_path)
            if valid:
                print("  Checksum Verification: Valid")
            elif current:
                print("  Checksum Verification: INVALID - File has changed!")
                
        else:
            print(f"File not found in catalog: {args.file_path}")
            
    elif args.command == 'mark':
        status = args.status == 'done'
        success = manager.mark_reverse_engineered(args.file_path, status, args.notes, args.schema)
        if success:
            print(f"File {args.file_path} marked as {'reverse engineered' if status else 'pending'}")
            
    elif args.command == 'analyze':
        analysis = manager.analyze_xml_structure(args.file_path)
        if analysis:
            print(f"Analysis of {args.file_path}:")
            print(f"  Root Element: {analysis['root_element']}")
            
            print("  Element Hierarchy:")
            for parent, children in analysis["child_elements"].items():
                print(f"    {parent} → {', '.join(children)}")
                
            print("  Attributes by Element:")
            for element, attrs in analysis["attributes"].items():
                print(f"    {element}: {', '.join(attrs)}")
                
            print("  Element Counts:")
            for element, count in analysis["element_counts"].items():
                print(f"    {element}: {count}")
                
    elif args.command == 'stats':
        stats = manager.get_statistics()
        print("Reverse Engineering Progress:")
        print(f"  Total Files: {stats['total_files']}")
        print(f"  Reverse Engineered: {stats['reverse_engineered']} ({stats['completion_percentage']:.1f}%)")
        
        print("  By Category:")
        for category, data in stats["categories"].items():
            percentage = (data["reverse_engineered"] / data["total"] * 100) if data["total"] > 0 else 0
            print(f"    {category}: {data['reverse_engineered']}/{data['total']} ({percentage:.1f}%)")
            
    elif args.command == 'export':
        success = manager.export_xml_schema(args.file_path, args.output_path)
        if success:
            print(f"XML schema exported to {args.output_path}")
            
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
