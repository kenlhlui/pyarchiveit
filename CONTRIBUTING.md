
# CONTRIBUTING.md

## Development Guide

### 🛠️ Setting Up Development Environment
To install the development dependencies (local_dev), use uv to run:
```bash
uv sync --group local_dev
```

### 📄 Building Documentation
To install the dependencies for building the documentation (docs), use uv to run:
```bash
uv sync --group docs
```
Then run the following command to build the documentation locally:
```bash
mkdocs serve
```

### 🚀 Releasing a New Version
Use the following commands to release a new version:
```bash
bash scripts/release.sh
```