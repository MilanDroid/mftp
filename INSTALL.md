# Installation Guide

This guide explains how to install the mFTP client on any device.

## Quick Start

### For End Users

1. **Download the package** - Get either:
   - `mftp_client-1.0.0-py3-none-any.whl` (recommended)
   - `mftp_client-1.0.0.tar.gz`

2. **Install with pip**:
   ```bash
   pip install mftp_client-1.0.0-py3-none-any.whl
   ```

3. **Run the command**:
   ```bash
   mftp --help
   ```

That's it! The `mftp` command is now available system-wide.

## Installation Methods by Platform

### macOS

#### Using Homebrew Python (recommended)
```bash
brew install python3
pip3 install mftp_client-1.0.0-py3-none-any.whl
mftp --help
```

#### Using System Python
```bash
python3 -m pip install --user mftp_client-1.0.0-py3-none-any.whl
mftp --help
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install mftp_client-1.0.0-py3-none-any.whl
mftp --help
```

### Linux (RHEL/CentOS/Fedora)

```bash
sudo dnf install python3 python3-pip
pip3 install mftp_client-1.0.0-py3-none-any.whl
mftp --help
```

### Windows

#### Using Python from python.org
1. Download and install Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Open Command Prompt or PowerShell:
   ```cmd
   pip install mftp_client-1.0.0-py3-none-any.whl
   mftp --help
   ```

#### Using Windows Store Python
```powershell
# Install Python from Microsoft Store first
pip install mftp_client-1.0.0-py3-none-any.whl
mftp --help
```

## Advanced Installation

### Install in Virtual Environment (Recommended for Developers)

```bash
# Create virtual environment
python3 -m venv mftp-env

# Activate it
# On macOS/Linux:
source mftp-env/bin/activate
# On Windows:
mftp-env\Scripts\activate

# Install
pip install mftp_client-1.0.0-py3-none-any.whl

# Use
mftp --help
```

### Install from Source

```bash
git clone https://github.com/antony/mftp.git
cd mftp
pip install -e .
```

### Install System-Wide (Requires Admin)

#### macOS/Linux
```bash
sudo pip3 install mftp_client-1.0.0-py3-none-any.whl
```

#### Windows (as Administrator)
```cmd
pip install mftp_client-1.0.0-py3-none-any.whl
```

## Verifying Installation

After installation, verify it works:

```bash
# Check if command is available
mftp --version

# See help
mftp --help

# Test in interactive mode
mftp
```

## Troubleshooting

### Command not found after installation

**Problem**: `mftp: command not found`

**Solution**: Add Python's bin directory to your PATH:

- **macOS/Linux**: Add to `~/.bashrc` or `~/.zshrc`:
  ```bash
  export PATH="$HOME/.local/bin:$PATH"
  ```

- **Windows**: Add to PATH environment variable:
  ```
  %APPDATA%\Python\Python3x\Scripts
  ```

### Permission denied errors

**Problem**: `PermissionError` during installation

**Solution**: Install to user directory:
```bash
pip install --user mftp_client-1.0.0-py3-none-any.whl
```

### Missing dependencies

**Problem**: `ModuleNotFoundError: No module named 'colorama'`

**Solution**: Install dependencies manually:
```bash
pip install colorama
```

## Uninstalling

To remove mFTP:

```bash
pip uninstall mftp-client
```

## System Requirements

- Python 3.6 or higher
- pip (usually included with Python)
- 10 MB free disk space
- Internet connection (for initial pip install)

## Supported Platforms

- macOS 10.13+ (High Sierra and later)
- Linux (all major distributions)
- Windows 10/11
- Any platform with Python 3.6+