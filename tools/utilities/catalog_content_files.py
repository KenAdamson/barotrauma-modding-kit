"""
Catalog Content Files

This script recursively finds all XML files in the Barotrauma Content directory,
calculates checksums, and stores the information in a structured format for
later reference during schema reverse engineering.
"""

import os
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def calculate_file_checksum(file_path: str, algorithm: str = 'sha256') -> str:
    """
    Calculate the checksum of a file using the specified algorithm.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (default: sha256)
        
    Returns:
        Hexadecimal checksum string
    """
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Algorithm {algorithm} not available. Choose from: {', '.join(hashlib.algorithms_available)}")
    
    hash_obj = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        # Read and update hash in chunks to avoid loading large files into memory
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_obj.update(byte_block)
    
    return hash_obj.hexdigest()


def find_xml_files(directory: str) -> List[str]:
    """
    Recursively find all XML files in the specified directory.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of paths to XML files
    """
    xml_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    
    return sorted(xml_files)


def catalog_files(content_dir: str, output_file: str, hash_algorithm: str = 'sha256') -> None:
    """
    Catalog all XML files in the Content directory.
    
    Args:
        content_dir: Path to the Content directory
        output_file: Path to save the catalog
        hash_algorithm: Hash algorithm to use for checksums
    """
    if not os.path.isdir(content_dir):
        raise ValueError(f"Content directory not found: {content_dir}")
    
    print(f"Scanning for XML files in {content_dir}...")
    xml_files = find_xml_files(content_dir)
    print(f"Found {len(xml_files)} XML files.")
    
    catalog = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "content_directory": content_dir,
            "hash_algorithm": hash_algorithm,
            "total_files": len(xml_files)
        },
        "files": {}
    }
    
    for i, file_path in enumerate(xml_files):
        if i % 100 == 0 and i > 0:
            print(f"Processed {i}/{len(xml_files)} files...")
        
        try:
            rel_path = os.path.relpath(file_path, content_dir)
            checksum = calculate_file_checksum(file_path, hash_algorithm)
            
            catalog["files"][rel_path] = {
                "checksum": checksum,
                "algorithm": hash_algorithm,
                "size_bytes": os.path.getsize(file_path),
                "last_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                "reverse_engineered": False,
                "metadata": {}  # For storing reverse engineering notes and schema info
            }
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"Writing catalog to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"Catalog saved with {len(catalog['files'])} files.")


def main():
    parser = argparse.ArgumentParser(description='Catalog Barotrauma Content XML files for schema reverse engineering')
    parser.add_argument('--content-dir', '-d', default='x:/steam_library/steamapps/common/Barotrauma/Content',
                       help='Path to the Barotrauma Content directory')
    parser.add_argument('--output', '-o', default='barotrauma_content_catalog.json',
                       help='Output file to save the catalog')
    parser.add_argument('--algorithm', '-a', default='sha256',
                       help='Hash algorithm to use for checksums')
    args = parser.parse_args()
    
    catalog_files(args.content_dir, args.output, args.algorithm)


if __name__ == "__main__":
    main()
