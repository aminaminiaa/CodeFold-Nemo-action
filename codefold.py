#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CodeFold - A professional tool for combining and extracting project files
Version: 1.0.0
"""

import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict

# Extended text file extensions with their MIME types
TEXT_EXTENSIONS_MIME = {
    '.txt': 'text/plain',
    '.py': 'text/x-python',
    '.js': 'text/javascript',
    '.jsx': 'text/javascript',
    '.ts': 'text/typescript',
    '.tsx': 'text/typescript',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.css': 'text/css',
    '.scss': 'text/x-scss',
    '.sass': 'text/x-sass',
    '.less': 'text/x-less',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.yaml': 'text/yaml',
    '.yml': 'text/yaml',
    '.md': 'text/markdown',
    '.markdown': 'text/markdown',
    '.rst': 'text/x-rst',
    '.csv': 'text/csv',
    '.c': 'text/x-c',
    '.cpp': 'text/x-c++',
    '.cc': 'text/x-c++',
    '.h': 'text/x-c',
    '.hpp': 'text/x-c++',
    '.java': 'text/x-java',
    '.php': 'text/x-php',
    '.rb': 'text/x-ruby',
    '.go': 'text/x-go',
    '.rs': 'text/x-rust',
    '.swift': 'text/x-swift',
    '.kt': 'text/x-kotlin',
    '.kts': 'text/x-kotlin',
    '.scala': 'text/x-scala',
    '.sh': 'text/x-sh',
    '.bash': 'text/x-sh',
    '.zsh': 'text/x-sh',
    '.fish': 'text/x-sh',
    '.ps1': 'text/x-powershell',
    '.bat': 'text/x-batch',
    '.cmd': 'text/x-batch',
    '.sql': 'application/sql',
    '.r': 'text/x-r',
    '.R': 'text/x-r',
    '.dart': 'text/x-dart',
    '.lua': 'text/x-lua',
    '.perl': 'text/x-perl',
    '.pl': 'text/x-perl',
    '.vim': 'text/x-vim',
    '.ini': 'text/plain',
    '.cfg': 'text/plain',
    '.conf': 'text/plain',
    '.toml': 'text/x-toml',
    '.lock': 'text/plain',
    '.env': 'text/plain',
    '.gitignore': 'text/plain',
    '.dockerignore': 'text/plain',
    '.editorconfig': 'text/plain',
    '.eslintrc': 'application/json',
    '.prettierrc': 'application/json',
    '.babelrc': 'application/json',
    '.vue': 'text/x-vue',
    '.svelte': 'text/x-svelte',
}

# Binary file extensions with their MIME types
BINARY_EXTENSIONS_MIME = {
    # Images
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp',
    '.ico': 'image/x-icon',
    '.svg': 'image/svg+xml',
    '.webp': 'image/webp',
    '.tiff': 'image/tiff',
    '.tif': 'image/tiff',
    # Audio
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.ogg': 'audio/ogg',
    '.flac': 'audio/flac',
    '.aac': 'audio/aac',
    '.m4a': 'audio/mp4',
    # Video
    '.mp4': 'video/mp4',
    '.avi': 'video/x-msvideo',
    '.mov': 'video/quicktime',
    '.wmv': 'video/x-ms-wmv',
    '.flv': 'video/x-flv',
    '.webm': 'video/webm',
    '.mkv': 'video/x-matroska',
    # Archives
    '.zip': 'application/zip',
    '.rar': 'application/x-rar-compressed',
    '.tar': 'application/x-tar',
    '.gz': 'application/gzip',
    '.7z': 'application/x-7z-compressed',
    '.bz2': 'application/x-bzip2',
    # Documents
    '.pdf': 'application/pdf',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xls': 'application/vnd.ms-excel',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.ppt': 'application/vnd.ms-powerpoint',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    # Executables and Libraries
    '.exe': 'application/x-msdownload',
    '.dll': 'application/x-msdownload',
    '.so': 'application/x-sharedlib',
    '.dylib': 'application/x-sharedlib',
    '.apk': 'application/vnd.android.package-archive',
    '.jar': 'application/java-archive',
    '.war': 'application/java-archive',
    # Fonts
    '.ttf': 'font/ttf',
    '.otf': 'font/otf',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.eot': 'application/vnd.ms-fontobject',
    # Other
    '.bin': 'application/octet-stream',
    '.dat': 'application/octet-stream',
    '.db': 'application/x-sqlite3',
    '.sqlite': 'application/x-sqlite3',
    '.pyc': 'application/x-bytecode.python',
}

def get_mime_type_by_extension(file_path):
    """Get MIME type based on file extension"""
    _, ext = os.path.splitext(file_path.lower())
    
    if ext in TEXT_EXTENSIONS_MIME:
        return TEXT_EXTENSIONS_MIME[ext]
    elif ext in BINARY_EXTENSIONS_MIME:
        return BINARY_EXTENSIONS_MIME[ext]
    else:
        return 'application/octet-stream'

def is_text_file(file_path):
    """Check if file is a text file based on extension"""
    _, ext = os.path.splitext(file_path.lower())
    return ext in TEXT_EXTENSIONS_MIME

def detect_tech_stack(root_dir):
    """Detect technologies based on file extensions present"""
    extension_tech_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.jsx': 'React',
        '.ts': 'TypeScript',
        '.tsx': 'React',
        '.vue': 'Vue',
        '.java': 'Java',
        '.c': 'C',
        '.cpp': 'C++',
        '.go': 'Go',
        '.rs': 'Rust',
        '.php': 'PHP',
        '.rb': 'Ruby',
        '.dart': 'Dart',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.r': 'R',
        '.R': 'R',
        '.cs': 'C#',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'Sass',
        '.sql': 'SQL',
        '.sh': 'Shell',
    }
    
    detected_techs = set()
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            _, ext = os.path.splitext(file.lower())
            if ext in extension_tech_map:
                detected_techs.add(extension_tech_map[ext])
    
    return ', '.join(sorted(detected_techs)) if detected_techs else 'Not detected'

def count_items(root_dir):
    """Count files and directories in project"""
    file_count = 0
    dir_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        dir_count += len(dirs)
        file_count += len(files)
    
    return file_count, dir_count

def combine_files(root_dir, output_file=None):
    """Combine all files in directory into a JSON-like structure"""
    root_path = Path(root_dir).resolve()
    project_name = root_path.name
    
    if output_file is None:
        output_file = f"{project_name}.txt"
    
    # Collect all items
    items = []
    
    for root, dirs, files in os.walk(root_dir):
        rel_root = os.path.relpath(root, root_dir)
        
        # Add empty directories
        for dir_name in sorted(dirs):
            dir_path = os.path.join(root, dir_name)
            rel_path = os.path.relpath(dir_path, root_dir)
            
            # Check if directory is empty
            if not os.listdir(dir_path):
                items.append({
                    'name': rel_path.replace('\\', '/'),
                    'type': 'directory',
                    'content': '<empty folder>'
                })
        
        # Add files
        for file_name in sorted(files):
            file_path = os.path.join(root, file_name)
            rel_path = os.path.relpath(file_path, root_dir)
            mime_type = get_mime_type_by_extension(file_path)
            
            item = {
                'name': rel_path.replace('\\', '/'),
                'type': mime_type
            }
            
            if is_text_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    item['content'] = content
                except Exception as e:
                    item['content'] = f'<error reading file: {str(e)}>'
            
            items.append(item)
    
    # Get project statistics
    file_count, dir_count = count_items(root_dir)
    tech_stack = detect_tech_stack(root_dir)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write(f"=== Project: {project_name} ===\n")
        f.write(f"Total files: {file_count}\n")
        f.write(f"Total directories: {dir_count}\n")
        f.write(f"Tech Stack: {tech_stack}\n")
        f.write("=" * 30 + "\n\n")
        
        # Write JSON-like structure
        f.write("[\n")
        for i, item in enumerate(items):
            f.write("  {\n")
            f.write(f'    "name": "{item["name"]}",\n')
            f.write(f'    "type": "{item["type"]}"')
            
            if 'content' in item:
                f.write(',\n')
                f.write('    "content": \n')
                f.write('"\n')
                f.write(item['content'])
                f.write('\n"\n')
            else:
                f.write('\n')
            
            if i < len(items) - 1:
                f.write("  },\n")
            else:
                f.write("  }\n")
        
        f.write("]\n")
    
    print(f"Successfully created: {output_file}")
    print(f"Project: {project_name}")
    print(f"Files: {file_count} | Directories: {dir_count}")
    print(f"Tech Stack: {tech_stack}")
    
    # ✨ اضافه کردن notification
    try:
        import subprocess
        subprocess.run([
            'notify-send',
            'CodeFold - Combine',
            f'✓ Combined {file_count} files\n{os.path.basename(output_file)}'
        ], check=False, stderr=subprocess.DEVNULL)
    except:
        pass
    
    return output_file

def extract_files(input_file, output_dir):
    """Extract files from combined format back to directory structure"""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip header (find the start of JSON structure)
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() == '[':
            start_idx = i
            break
    
    # Parse items
    items = []
    current_item = {}
    in_content = False
    content_lines = []
    
    i = start_idx + 1
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if stripped == '{':
            current_item = {}
            in_content = False
            content_lines = []
        
        elif stripped.startswith('"name":'):
            name = stripped.split(':', 1)[1].strip().strip(',').strip('"')
            current_item['name'] = name
        
        elif stripped.startswith('"type":'):
            type_val = stripped.split(':', 1)[1].strip().strip(',').strip('"')
            current_item['type'] = type_val
        
        elif stripped == '"content":':
            in_content = True
            i += 1  # Skip the opening quote line
        
        elif in_content and stripped == '"':
            # End of content
            current_item['content'] = ''.join(content_lines)
            in_content = False
            content_lines = []
        
        elif in_content:
            # Content line
            content_lines.append(lines[i])
        
        elif stripped in ['},', '}']:
            if current_item:
                items.append(current_item)
                current_item = {}
        
        i += 1
    
    # Create files and directories
    created_files = 0
    created_dirs = 0
    
    for item in items:
        if not item.get('name'):
            continue
        
        full_path = os.path.join(output_dir, item['name'])
        
        if item.get('type') == 'directory':
            os.makedirs(full_path, exist_ok=True)
            created_dirs += 1
            print(f"Created directory: {full_path}")
        else:
            # Create parent directories
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            if 'content' in item:
                # Text file with content
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(item['content'])
                print(f"Created text file: {full_path}")
            else:
                # Binary file (create empty placeholder)
                with open(full_path, 'wb') as f:
                    pass
                print(f"Created binary placeholder: {full_path}")
            
            created_files += 1
    
    print(f"\nExtraction completed!")
    print(f"Created {created_files} files and {created_dirs} directories in '{output_dir}'")
    
    # ✨ اضافه کردن notification
    try:
        import subprocess
        subprocess.run([
            'notify-send',
            'CodeFold - Extract',
            f'✓ Extracted {created_files} files\n{os.path.basename(output_dir)}'
        ], check=False, stderr=subprocess.DEVNULL)
    except:
        pass

def interactive_mode():
    """Interactive mode for user input"""
    print("=== CodeFold - Interactive Mode ===\n")
    print("Choose operation:")
    print("1. Combine files (directory -> text file)")
    print("2. Extract files (text file -> directory)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        path = input("Enter project directory path: ").strip().strip('"\'')
        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a valid directory.")
            sys.exit(1)
        combine_files(path)
    elif choice == '2':
        input_file = input("Enter input text file path: ").strip().strip('"\'')
        output_dir = input("Enter output directory path: ").strip().strip('"\'')
        extract_files(input_file, output_dir)
    else:
        print("Invalid choice.")
        sys.exit(1)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='CodeFold - Combine and extract project files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Combine files:
    python codefold.py -c /path/to/project output.txt
    python codefold.py -c /path/to/project
  
  Extract files:
    python codefold.py -e output.txt /path/to/extracted
    
  Interactive mode:
    python codefold.py
        """
    )
    
    parser.add_argument('-c', '--combine', nargs='+', metavar=('DIR', 'OUTPUT'),
                        help='Combine files from directory')
    parser.add_argument('-e', '--extract', nargs=2, metavar=('INPUT', 'OUTPUT'),
                        help='Extract files from text to directory')
    
    args = parser.parse_args()
    
    if args.combine:
        if len(args.combine) == 1:
            combine_files(args.combine[0])
        else:
            combine_files(args.combine[0], args.combine[1])
    elif args.extract:
        extract_files(args.extract[0], args.extract[1])
    else:
        # No arguments - run interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()
