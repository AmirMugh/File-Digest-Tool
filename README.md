# File Digest Tool 📂🔍

A Python-based utility for generating structured digests of project directories, designed to help AI language models analyze codebases efficiently.

## Overview

This tool creates comprehensive summaries of software projects by:
- Generating directory trees with size annotations
- Aggregating code/text file contents
- Applying smart filters to exclude non-code files
- Using multi-threading for faster processing

**GitHub**: [https://github.com/AmirMugh/File-Digest-Tool](https://github.com/AmirMugh/File-Digest-Tool)

## Features ✨

- **Directory Visualization**: Creates nested tree structures with file sizes
- **Smart Filtering** (Edit INCLUDE_EXTENSIONS and/or EXCLUDE_EXTENSIONS. Defaulted at most common file extenstions):
  - Includes: `.py`, `.cpp`, `.c`, `.h`, `.java`, `.cs`, `.js`, `.html`, `.css`, `.txt`
  - Excludes: binary/assets (`.exe`, `.dll`, `.jpg`, etc.)
- **Performance Optimizations**:
  - Multi-threaded file processing
  - Configurable file size limits
- **Custom Exclusions**: Skip specified directories
- **Progress Tracking**: Visual processing bar with tqdm

## For AI Models 🤖
This tool helps LLMs:

- Understand project structure through directory trees

- Access relevant code/text files in context

- Avoid processing binary/non-textual data

- Maintain file path context for code analysis


## Installation ⚙️
Clone the repo:
```bash
git clone https://github.com/AmirMugh/File-Digest-Tool.git
cd File-Digest-Tool
```

Ensure tqdm is installed, if not, install it with:
```bash
pip install tqdm
```
    
## Usage 🚀
**Basic command**:

```bash
python fileDigest.py /path/to/project
```

**Advanced options**:

```bash
python fileDigest.py /path/to/project \
  -o ./output/ \           # Custom output directory
  --exclude node_modules \ # Exclude specific directories
  --max-size 500           # Skip files >500KB
```
**Output Example** 📄
project_summary.txt structure:

```
project_root/
├── src/
│   ├── main.py (12.4 KB)
│   └── utils/
│       └── helpers.py (8.2 KB)
└── README.md (2.1 KB)

================================================
File: /project_root/src/main.py
================================================
[File content...]

================================================
File: /project_root/src/utils/helpers.py
================================================
[File content...]
```


## Contributing 🤝
Contributions are welcome! Please:

- Fork the repository

- Create a feature branch

- Submit a pull request


## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)



## Authors

- [@AmirMugh](https://www.github.com/AmirMugh)

