# CodeFold - Nemo Action

A powerful Nemo action for combining and extracting project files with automatic tech stack detection.

## ✨ Features

- 🔀 **Combine**: Merge all project files into a structured text file
- 📦 **Extract**: Restore files from combined text back to directory structure
- 🔍 **Tech Detection**: Automatically detects technology stack
- 📊 **Statistics**: Shows file/directory counts
- 🔔 **Notifications**: Desktop notifications on completion
- 📝 **MIME Support**: Handles 80+ file types

## 🚀 Quick Install
```bash
chmod +x install.sh
./install.sh
```

## 📖 Usage

### Right-Click Context Menu

**Combine a project:**
1. Right-click on any folder
2. Select **"CodeFold - Combine"**
3. Output: `foldername.txt` created in the same folder

**Extract files:**
1. Right-click on any `.txt` file
2. Select **"CodeFold - Extract"**
3. Output: `filename_extracted/` directory created

### Command Line

```bash
# Combine files
codefold.py -c /path/to/project

# Extract files
codefold.py -e combined.txt /output/directory

# Interactive mode
codefold.py
```

## 🗑️ Uninstall

```bash
chmod +x uninstall.sh
./uninstall.sh
```
## 🛠️ Requirements

- **Python 3.6+** (pre-installed on most Linux)
- **Nemo File Manager** (Cinnamon desktop)
- **libnotify-bin** (auto-installed by installer)

## 📄 Supported File Types

### Text Files (80+ types)
Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, PHP, Ruby, HTML, CSS, JSON, YAML, Markdown, SQL, Shell scripts, and more...

### Binary Files
Images (PNG, JPG, SVG...), Audio (MP3, WAV...), Video (MP4, AVI...), Archives (ZIP, TAR...), Documents (PDF, DOCX...), and more...


**Made with ❤️ for Cinnamon Desktop**