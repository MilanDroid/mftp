#!/usr/bin/env python3
import os
import sys
import argparse
import getpass
from ftplib import FTP, error_perm
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)


class FTPClient:
    def __init__(self):
        self.ftp = None
        self.connected = False

    def connect(self, host, user, password, port=21):
        """Connect to FTP server with password authentication"""
        try:
            print(f"{Fore.CYAN}Connecting to {host}:{port} with username {user}...{Style.RESET_ALL}")
            self.ftp = FTP()
            self.ftp.connect(host, port)
            self.ftp.login(user, password)
            self.connected = True
            welcome_msg = self.ftp.getwelcome()
            print(f"{Fore.GREEN}✓ Connected successfully!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{welcome_msg}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Connection failed: {e}{Style.RESET_ALL}")
            return False

    def disconnect(self):
        """Disconnect from FTP server"""
        if self.ftp and self.connected:
            try:
                self.ftp.quit()
                print(f"{Fore.GREEN}✓ Disconnected successfully{Style.RESET_ALL}")
            except:
                self.ftp.close()
            self.connected = False

    def list_directory(self, path='.'):
        """List directory contents"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return []

        try:
            items = []
            self.ftp.cwd(path)
            self.ftp.dir(lambda x: items.append(x))
            return items
        except error_perm as e:
            print(f"{Fore.RED}✗ Error listing directory: {e}{Style.RESET_ALL}")
            return []

    def is_directory(self, path):
        """Check if path is a directory"""
        try:
            current = self.ftp.pwd()
            self.ftp.cwd(path)
            self.ftp.cwd(current)
            return True
        except error_perm:
            return False

    def file_exists(self, filepath):
        """Check if a file exists on the server"""
        try:
            # Try to get the size of the file
            self.ftp.size(filepath)
            return True
        except error_perm:
            return False

    def remove_file(self, filepath):
        """Remove a single file"""
        try:
            self.ftp.delete(filepath)
            print(f"{Fore.GREEN}✓ Removed file: {filepath}{Style.RESET_ALL}")
            return True
        except error_perm as e:
            print(f"{Fore.RED}✗ Failed to remove file {filepath}: {e}{Style.RESET_ALL}")
            return False

    def remove_files(self, filepaths):
        """Remove multiple files or directories"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return

        print(f"{Fore.CYAN}Removing {len(filepaths)} item(s)...{Style.RESET_ALL}")
        success_count = 0
        for filepath in filepaths:
            if self.is_directory(filepath):
                print(f"{Fore.YELLOW}'{filepath}' is a directory, removing recursively...{Style.RESET_ALL}")
                if self.remove_directory_recursive(filepath):
                    success_count += 1
            else:
                if self.remove_file(filepath):
                    success_count += 1

        print(f"{Fore.GREEN}✓ Removed {success_count}/{len(filepaths)} item(s){Style.RESET_ALL}")

    def remove_directory_recursive(self, path):
        """Recursively remove directory and all its contents"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return False

        try:
            try:
                self.ftp.cwd(path)
            except error_perm:
                return self.remove_file(path)

            current_path = self.ftp.pwd()
            items = []
            self.ftp.dir(items.append)

            for item in items:
                parts = item.split()
                if len(parts) < 9:
                    continue

                name = ' '.join(parts[8:])
                if name in ['.', '..']:
                    continue

                item_path = f"{current_path}/{name}".replace('//', '/')

                if item.startswith('d'):
                    self.remove_directory_recursive(item_path)
                else:
                    self.remove_file(item_path)

            parent_dir = '/'.join(current_path.rstrip('/').split('/')[:-1])
            if not parent_dir:
                parent_dir = '/'

            self.ftp.cwd(parent_dir)
            self.ftp.rmd(current_path)
            print(f"{Fore.GREEN}✓ Removed directory: {path}{Style.RESET_ALL}")
            return True

        except error_perm as e:
            print(f"{Fore.RED}✗ Failed to remove directory {path}: {e}{Style.RESET_ALL}")
            return False

    def remove_directories(self, dirpaths):
        """Remove multiple directories recursively"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return

        print(f"{Fore.CYAN}Removing {len(dirpaths)} directory(ies)...{Style.RESET_ALL}")
        success_count = 0
        for dirpath in dirpaths:
            if self.remove_directory_recursive(dirpath):
                success_count += 1

        print(f"{Fore.GREEN}✓ Removed {success_count}/{len(dirpaths)} directory(ies){Style.RESET_ALL}")

    def upload_file(self, local_path, remote_path=None):
        """Upload a file to the FTP server"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return False

        if not os.path.isfile(local_path):
            print(f"{Fore.RED}✗ Local file not found: {local_path}{Style.RESET_ALL}")
            return False

        if remote_path is None:
            remote_path = os.path.basename(local_path)

        try:
            with open(local_path, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}', f)
            print(f"{Fore.GREEN}✓ Uploaded: {local_path} -> {remote_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to upload {local_path}: {e}{Style.RESET_ALL}")
            return False

    def upload_folder(self, local_path, remote_path=None):
        """Upload a folder and all its contents recursively"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return False

        if not os.path.isdir(local_path):
            print(f"{Fore.RED}✗ Local folder not found: {local_path}{Style.RESET_ALL}")
            return False

        if remote_path is None:
            remote_path = os.path.basename(local_path)

        try:
            try:
                self.ftp.mkd(remote_path)
                print(f"{Fore.CYAN}Created remote directory: {remote_path}{Style.RESET_ALL}")
            except error_perm:
                pass

            for item in os.listdir(local_path):
                local_item_path = os.path.join(local_path, item)
                remote_item_path = f"{remote_path}/{item}"

                if os.path.isfile(local_item_path):
                    self.upload_file(local_item_path, remote_item_path)
                elif os.path.isdir(local_item_path):
                    self.upload_folder(local_item_path, remote_item_path)

            print(f"{Fore.GREEN}✓ Uploaded folder: {local_path} -> {remote_path}{Style.RESET_ALL}")
            return True

        except Exception as e:
            print(f"{Fore.RED}✗ Failed to upload folder {local_path}: {e}{Style.RESET_ALL}")
            return False

    def upload_files(self, local_paths):
        """Upload multiple files"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return

        print(f"{Fore.CYAN}Uploading {len(local_paths)} file(s)...{Style.RESET_ALL}")
        success_count = 0
        for local_path in local_paths:
            if self.upload_file(local_path):
                success_count += 1

        print(f"{Fore.GREEN}✓ Uploaded {success_count}/{len(local_paths)} file(s){Style.RESET_ALL}")

    def upload_folders(self, local_paths):
        """Upload multiple folders"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return

        print(f"{Fore.CYAN}Uploading {len(local_paths)} folder(s)...{Style.RESET_ALL}")
        success_count = 0
        for local_path in local_paths:
            if self.upload_folder(local_path):
                success_count += 1

        print(f"{Fore.GREEN}✓ Uploaded {success_count}/{len(local_paths)} folder(s){Style.RESET_ALL}")

    def sync_path(self, local_path, remote_path=None, skip_existing=False):
        """
        Sync a file or folder to the FTP server

        Args:
            local_path: Local file or folder path
            remote_path: Remote destination path (optional)
            skip_existing: If True, skip files that already exist on server
        """
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return False

        if not os.path.exists(local_path):
            print(f"{Fore.RED}✗ Local path not found: {local_path}{Style.RESET_ALL}")
            return False

        if os.path.isfile(local_path):
            return self._sync_file(local_path, remote_path, skip_existing)
        elif os.path.isdir(local_path):
            return self._sync_folder(local_path, remote_path, skip_existing)

        return False

    def _sync_file(self, local_path, remote_path=None, skip_existing=False):
        """Sync a single file to the server"""
        if remote_path is None:
            remote_path = os.path.basename(local_path)

        # Check if file exists on server
        if self.file_exists(remote_path):
            if skip_existing:
                print(f"{Fore.YELLOW}⊘ Skipped (exists): {local_path} -> {remote_path}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.CYAN}↻ Replacing: {local_path} -> {remote_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}↑ Uploading: {local_path} -> {remote_path}{Style.RESET_ALL}")

        # Upload or replace the file
        try:
            with open(local_path, 'rb') as f:
                self.ftp.storbinary(f'STOR {remote_path}', f)
            print(f"{Fore.GREEN}✓ Synced: {local_path} -> {remote_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to sync {local_path}: {e}{Style.RESET_ALL}")
            return False

    def _sync_folder(self, local_path, remote_path=None, skip_existing=False):
        """Sync a folder and all its contents recursively"""
        if remote_path is None:
            remote_path = os.path.basename(local_path)

        try:
            # Create remote directory if it doesn't exist
            if not self.is_directory(remote_path):
                try:
                    self.ftp.mkd(remote_path)
                    print(f"{Fore.CYAN}Created remote directory: {remote_path}{Style.RESET_ALL}")
                except error_perm as e:
                    print(f"{Fore.RED}✗ Failed to create directory {remote_path}: {e}{Style.RESET_ALL}")
                    return False
            else:
                print(f"{Fore.CYAN}Directory exists: {remote_path}{Style.RESET_ALL}")

            # Sync all items in the directory
            for item in os.listdir(local_path):
                local_item_path = os.path.join(local_path, item)
                remote_item_path = f"{remote_path}/{item}"

                if os.path.isfile(local_item_path):
                    self._sync_file(local_item_path, remote_item_path, skip_existing)
                elif os.path.isdir(local_item_path):
                    self._sync_folder(local_item_path, remote_item_path, skip_existing)

            print(f"{Fore.GREEN}✓ Synced folder: {local_path} -> {remote_path}{Style.RESET_ALL}")
            return True

        except Exception as e:
            print(f"{Fore.RED}✗ Failed to sync folder {local_path}: {e}{Style.RESET_ALL}")
            return False

    def sync_paths(self, local_paths, skip_existing=False):
        """Sync multiple files or folders"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return

        mode = "skip mode" if skip_existing else "replace mode"
        print(f"{Fore.CYAN}Syncing {len(local_paths)} item(s) ({mode})...{Style.RESET_ALL}")
        success_count = 0
        for local_path in local_paths:
            if self.sync_path(local_path, None, skip_existing):
                success_count += 1

        print(f"{Fore.GREEN}✓ Synced {success_count}/{len(local_paths)} item(s){Style.RESET_ALL}")

    def rename(self, old_name, new_name):
        """Rename a file or folder"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return False

        try:
            self.ftp.rename(old_name, new_name)
            print(f"{Fore.GREEN}✓ Renamed: {old_name} -> {new_name}{Style.RESET_ALL}")
            return True
        except error_perm as e:
            print(f"{Fore.RED}✗ Failed to rename {old_name}: {e}{Style.RESET_ALL}")
            return False

    def get_current_directory(self):
        """Get current working directory on FTP server"""
        if not self.connected:
            return None
        return self.ftp.pwd()

    def change_directory(self, path):
        """Change directory on FTP server"""
        if not self.connected:
            print(f"{Fore.RED}✗ Not connected to server{Style.RESET_ALL}")
            return False

        try:
            self.ftp.cwd(path)
            print(f"{Fore.GREEN}✓ Changed directory to: {self.ftp.pwd()}{Style.RESET_ALL}")
            return True
        except error_perm as e:
            print(f"{Fore.RED}✗ Failed to change directory: {e}{Style.RESET_ALL}")
            return False


def print_help():
    """Print help information"""
    help_text = f"""
{Fore.CYAN}{'='*60}
FTP Client - Available Commands
{'='*60}{Style.RESET_ALL}

{Fore.YELLOW}Connection:{Style.RESET_ALL}
  connect <host> <user> <password> [port]  - Connect to FTP server
  disconnect                                - Disconnect from server
  quit, exit                                - Exit the program

{Fore.YELLOW}Navigation:{Style.RESET_ALL}
  ls [path]                                 - List directory contents
  cd <path>                                 - Change directory
  pwd                                       - Print working directory

{Fore.YELLOW}File Operations:{Style.RESET_ALL}
  rm <file1> [file2] ...                    - Remove one or more files/directories
  rmdir <dir1> [dir2] ...                   - Remove one or more directories recursively
  upload <file1> [file2] ...                - Upload one or more files
  uploaddir <dir1> [dir2] ...               - Upload one or more folders recursively
  sync <path1> [path2] ...                  - Sync files/folders (upload new, replace existing)
  sync-skip <path1> [path2] ...             - Sync files/folders (upload new, skip existing)
  rename <old_name> <new_name>              - Rename file or folder

{Fore.YELLOW}Other:{Style.RESET_ALL}
  help                                      - Show this help message
"""
    print(help_text)


def main():
    """Main CLI loop"""
    parser = argparse.ArgumentParser(
        description='FTP Client with password authentication and advanced features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ftp_client.py
  python ftp_client.py -H ftp.example.com -u myuser
  python ftp_client.py -H ftp.example.com -u myuser -p mypassword
  python ftp_client.py --host ftp.example.com --user myuser --port 2121

Passwords with Special Characters:
  If your password contains special characters (|, &, ;, $, etc.), use one of these methods:

  1. Omit -p flag (RECOMMENDED - password won't appear in history):
     python ftp_client.py -H ftp.example.com -u myuser

  2. Use single quotes (Unix/Linux/Mac):
     python ftp_client.py -H ftp.example.com -u myuser -p 'my|p@ss$word'

  3. Use double quotes and escape special characters:
     python ftp_client.py -H ftp.example.com -u myuser -p "my|p@ss\\$word"
        """
    )
    parser.add_argument('-H', '--host', help='FTP server hostname or IP address')
    parser.add_argument('-u', '--user', help='FTP username')
    parser.add_argument('-p', '--password', help='FTP password (not recommended, will prompt if omitted)')
    parser.add_argument('-P', '--port', type=int, default=21, help='FTP port (default: 21)')

    args = parser.parse_args()

    client = FTPClient()

    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}FTP Client - Type 'help' for available commands{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    if args.host and args.user:
        password = args.password
        if not password:
            try:
                password = getpass.getpass(f"Password for {args.user}@{args.host}: ")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Connection cancelled{Style.RESET_ALL}\n")
                password = None

        if password:
            client.connect(args.host, args.user, password, args.port)
    elif args.host or args.user:
        print(f"{Fore.YELLOW}Warning: Both host and user are required for connection.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Use: python ftp_client.py -H host -u user{Style.RESET_ALL}\n")

    while True:
        try:
            prompt = f"{Fore.GREEN}ftp> {Style.RESET_ALL}" if client.connected else f"{Fore.RED}ftp (disconnected)> {Style.RESET_ALL}"
            command = input(prompt).strip()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in ['quit', 'exit']:
                if client.connected:
                    client.disconnect()
                print(f"{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
                break

            elif cmd == 'help':
                print_help()

            elif cmd == 'connect':
                if len(args) < 3:
                    print(f"{Fore.RED}Usage: connect <host> <user> <password> [port]{Style.RESET_ALL}")
                else:
                    host = args[0]
                    user = args[1]
                    password = args[2]
                    port = int(args[3]) if len(args) > 3 else 21
                    client.connect(host, user, password, port)

            elif cmd == 'disconnect':
                client.disconnect()

            elif cmd == 'ls':
                path = args[0] if args else '.'
                items = client.list_directory(path)
                for item in items:
                    print(item)

            elif cmd == 'pwd':
                if client.connected:
                    print(f"{Fore.CYAN}{client.get_current_directory()}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✗ Not connected{Style.RESET_ALL}")

            elif cmd == 'cd':
                if not args:
                    print(f"{Fore.RED}Usage: cd <path>{Style.RESET_ALL}")
                else:
                    client.change_directory(args[0])

            elif cmd == 'rm':
                if not args:
                    print(f"{Fore.RED}Usage: rm <file1> [file2] ...{Style.RESET_ALL}")
                else:
                    client.remove_files(args)

            elif cmd == 'rmdir':
                if not args:
                    print(f"{Fore.RED}Usage: rmdir <dir1> [dir2] ...{Style.RESET_ALL}")
                else:
                    if len(args) == 1:
                        client.remove_directory_recursive(args[0])
                    else:
                        client.remove_directories(args)

            elif cmd == 'upload':
                if not args:
                    print(f"{Fore.RED}Usage: upload <file1> [file2] ...{Style.RESET_ALL}")
                else:
                    if len(args) == 1:
                        client.upload_file(args[0])
                    else:
                        client.upload_files(args)

            elif cmd == 'uploaddir':
                if not args:
                    print(f"{Fore.RED}Usage: uploaddir <dir1> [dir2] ...{Style.RESET_ALL}")
                else:
                    if len(args) == 1:
                        client.upload_folder(args[0])
                    else:
                        client.upload_folders(args)

            elif cmd == 'rename':
                if len(args) < 2:
                    print(f"{Fore.RED}Usage: rename <old_name> <new_name>{Style.RESET_ALL}")
                else:
                    client.rename(args[0], args[1])

            elif cmd == 'sync':
                if not args:
                    print(f"{Fore.RED}Usage: sync <path1> [path2] ...{Style.RESET_ALL}")
                else:
                    if len(args) == 1:
                        client.sync_path(args[0], None, skip_existing=False)
                    else:
                        client.sync_paths(args, skip_existing=False)

            elif cmd == 'sync-skip':
                if not args:
                    print(f"{Fore.RED}Usage: sync-skip <path1> [path2] ...{Style.RESET_ALL}")
                else:
                    if len(args) == 1:
                        client.sync_path(args[0], None, skip_existing=True)
                    else:
                        client.sync_paths(args, skip_existing=True)

            else:
                print(f"{Fore.RED}✗ Unknown command: {cmd}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Type 'help' for available commands{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Use 'quit' or 'exit' to exit{Style.RESET_ALL}")
        except EOFError:
            print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}")
            if client.connected:
                client.disconnect()
            break
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
