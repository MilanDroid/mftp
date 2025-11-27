# FTP Client

A feature-rich command-line FTP client written in Python with support for password authentication, multiple file operations, and recursive directory management.

## Features

- **Password Authentication**: Connect to FTP servers with username and password
- **Multiple File Deletion**: Remove multiple files at once
- **Recursive Operations**: Recursively remove directories and their contents
- **File Upload**: Upload single files to the server
- **Folder Upload**: Recursively upload entire folders
- **Rename Operations**: Rename both files and folders
- **Colorful Interface**: Easy-to-read colored output for better user experience

## Installation

### Option 1: Install from Source (Recommended for Development)

Clone the repository and install in editable mode:

```bash
git clone https://github.com/antony/mftp.git
cd mftp
pip install -e .
```

### Option 2: Install from Wheel File (Recommended for Distribution)

If you received a wheel file (.whl), install it directly:

```bash
pip install mftp_client-1.0.0-py3-none-any.whl
```

This works on any platform: macOS, Linux, Windows.

### Option 3: Install from Source Tarball

```bash
pip install mftp_client-1.0.0.tar.gz
```

### Option 4: Build and Install Locally

From the project directory:

```bash
pip install .
```

After installation using any method above, you can use the `mftp` command from anywhere on your system:

```bash
mftp -H ftp.example.com -u myuser
```

### Platform Support

This package works on:
- macOS (Intel and Apple Silicon)
- Linux (all distributions)
- Windows (10/11)
- Any platform with Python 3.6+

### Manual Installation (Without pip)

If you prefer to run the script directly without installation:

1. Make sure you have Python 3.6 or higher installed
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install colorama
```

3. Run the script:

```bash
python ftp_client.py
```

### Uninstall

To remove the installed command:

```bash
pip uninstall mftp-client
```

## Distribution

### For Developers: Building Distribution Packages

To create distribution packages that can be installed on any device:

1. Install build tools:
```bash
pip install build wheel twine
```

2. Build the distribution packages:
```bash
python -m build
```

This creates two files in the `dist/` directory:
- `mftp_client-1.0.0-py3-none-any.whl` - Wheel package (recommended)
- `mftp_client-1.0.0.tar.gz` - Source distribution

3. Share these files with others to install on any device:
```bash
pip install mftp_client-1.0.0-py3-none-any.whl
```

### Publishing to PyPI (Optional)

To make the package available via `pip install mftp-client` globally:

1. Create an account on [PyPI](https://pypi.org)
2. Upload the package:
```bash
twine upload dist/*
```

Then anyone can install it with:
```bash
pip install mftp-client
```

## Usage

After installation, you can use the `mftp` command directly:

### Interactive Mode

Run the FTP client without arguments for interactive mode:

```bash
mftp
```

Or if running directly without installation:
```bash
python ftp_client.py
```

Then connect inside the client:
```bash
ftp (disconnected)> connect ftp.example.com myuser mypassword
```

### Connect with Command-Line Arguments

**Recommended: Secure password prompt (password not visible in command line)**

```bash
mftp -H ftp.example.com -u myuser
```

This will prompt you to enter your password securely (it won't be displayed or saved in command history):
```
Password for myuser@ftp.example.com:
```

**With custom port:**

```bash
mftp -H ftp.example.com -u myuser -P 2121
```

**Not recommended: Password in command line (visible in history)**

```bash
mftp -H ftp.example.com -u myuser -p mypassword
```

Long form options:
```bash
mftp --host ftp.example.com --user myuser --port 21
```

### Running Without Installation

If you prefer to run the script directly:

```bash
chmod +x ftp_client.py
./ftp_client.py -H ftp.example.com -u myuser
```

### Command-Line Options

- `-H, --host` - FTP server hostname or IP address
- `-u, --user` - FTP username
- `-p, --password` - FTP password (optional, will prompt securely if omitted)
- `-P, --port` - FTP port (default: 21)
- `-h, --help` - Show help message

**Security Note:** It's recommended to omit the `-p` option and let the program prompt you for your password. This prevents your password from being visible in your shell history or process list.

## Available Commands

### Connection Commands

- `connect <host> <user> <password> [port]` - Connect to an FTP server
  - Example: `connect ftp.example.com myuser mypassword`
  - Example with port: `connect ftp.example.com myuser mypassword 2121`
- `disconnect` - Disconnect from the current server
- `quit` or `exit` - Exit the program

### Navigation Commands

- `ls [path]` - List directory contents
  - Example: `ls` (list current directory)
  - Example: `ls /public` (list specific directory)
- `cd <path>` - Change directory
  - Example: `cd /public/uploads`
- `pwd` - Print current working directory

### File Operations

- `rm <file1> [file2] ...` - Remove one or more files
  - Example: `rm file1.txt` (remove single file)
  - Example: `rm file1.txt file2.txt file3.txt` (remove multiple files)
- `rmdir <directory>` - Remove directory recursively (including all contents)
  - Example: `rmdir old_folder`
- `upload <local_path> [remote_path]` - Upload a file
  - Example: `upload /home/user/file.txt` (upload to current directory)
  - Example: `upload /home/user/file.txt /uploads/newfile.txt` (upload to specific path)
- `uploaddir <local_path> [remote_path]` - Upload a folder recursively
  - Example: `uploaddir /home/user/myfolder` (upload entire folder)
  - Example: `uploaddir /home/user/myfolder /remote/newfolder` (upload to specific path)
- `rename <old_name> <new_name>` - Rename file or folder
  - Example: `rename oldfile.txt newfile.txt`
  - Example: `rename old_folder new_folder`

### Other Commands

- `help` - Show available commands

## Example Session

```bash
$ python ftp_client.py

============================================================
FTP Client - Type 'help' for available commands
============================================================

ftp (disconnected)> connect ftp.example.com myuser mypassword
Connecting to ftp.example.com:21...
✓ Connected successfully!
220 Welcome to Example FTP Server

ftp> ls
drwxr-xr-x   2 user  group    4096 Jan 15 10:30 documents
-rw-r--r--   1 user  group    1024 Jan 15 10:31 file1.txt
-rw-r--r--   1 user  group    2048 Jan 15 10:32 file2.txt

ftp> cd documents
✓ Changed directory to: /documents

ftp> upload /home/user/myfile.txt
✓ Uploaded: /home/user/myfile.txt -> myfile.txt

ftp> uploaddir /home/user/myfolder
Created remote directory: myfolder
✓ Uploaded: /home/user/myfolder/file1.txt -> myfolder/file1.txt
✓ Uploaded: /home/user/myfolder/file2.txt -> myfolder/file2.txt
✓ Uploaded folder: /home/user/myfolder -> myfolder

ftp> rm file1.txt file2.txt
Removing 2 file(s)...
✓ Removed file: file1.txt
✓ Removed file: file2.txt
✓ Removed 2/2 files

ftp> rename oldfile.txt newfile.txt
✓ Renamed: oldfile.txt -> newfile.txt

ftp> rmdir old_folder
✓ Removed file: old_folder/file1.txt
✓ Removed file: old_folder/file2.txt
✓ Removed directory: old_folder

ftp> quit
✓ Disconnected successfully
Goodbye!
```

## Error Handling

The FTP client includes comprehensive error handling:
- Connection failures are reported with clear error messages
- File operation errors show which operations failed
- Invalid commands display usage information
- Network issues are caught and reported

## Security Note

This client transmits passwords in plain text as part of the FTP protocol. For secure file transfers, consider using SFTP or FTPS instead.

## Requirements

- Python 3.6+
- colorama 0.4.6+

## License

MIT License - See [LICENSE](LICENSE) file for details.

This is free and open source software.
