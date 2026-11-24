# mftp

A command-line FTP client that tells you what it did. It handles recursive uploads and deletes, and its sync reports whether each file was uploaded, replaced or skipped. It also prompts for your password, so the password never has to appear in your shell history.

## Install

Requires Python 3.6 or later.

```bash
pip install git+https://github.com/MilanDroid/mftp.git
```

If your shell then says `mftp: command not found`, pip installed the command into a folder that isn't on your `PATH`. pip names that folder in a warning during install. Add it to your `PATH`. For example, with macOS's system Python 3.9:

```bash
echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

To install from a wheel file instead, see [INSTALL.md](INSTALL.md). To build a wheel or publish a release, see [DISTRIBUTING.md](DISTRIBUTING.md).

## Quick start

```bash
mftp -H ftp.example.com -u deploy
```

mftp prompts for the password. Leave out `-p`: a password passed on the command line ends up in your shell history and in the process list.

| Option | Meaning | Default |
|---|---|---|
| `-H`, `--host` | Server hostname or IP address | |
| `-u`, `--user` | Username | |
| `-p`, `--password` | Password. Avoid it; mftp prompts if you leave it out | |
| `-P`, `--port` | Port | `21` |

Run `mftp` with no options to start disconnected, then connect from inside the client with `connect`.

## Commands

| Command | What it does |
|---|---|
| `connect <host> <user> <password> [port]` | Connect to a server |
| `disconnect` | Close the connection |
| `ls [path]` | List a directory |
| `cd <path>` | Change directory |
| `pwd` | Show the current directory |
| `upload <file1> [file2] ...` | Upload one or more files |
| `uploaddir <dir1> [dir2] ...` | Upload one or more folders, recursively |
| `sync <path1> [path2] ...` | Upload files and folders, replacing anything already on the server |
| `sync-skip <path1> [path2] ...` | Upload files and folders, leaving anything already on the server untouched |
| `rm <file1> [file2] ...` | Delete one or more files |
| `rmdir <dir1> [dir2] ...` | Delete one or more folders and everything in them |
| `rename <old> <new>` | Rename a file or folder |
| `help` | List the commands |
| `quit`, `exit` | Leave mftp |

## Sync

`sync` and `sync-skip` check each path on the server first and say which of three things they did:

```
ftp> sync ./dist
Syncing 1 item(s) (replace mode)...
Directory exists: dist
↑ Uploading: ./dist/app.js -> dist/app.js
✓ Synced: ./dist/app.js -> dist/app.js
↻ Replacing: ./dist/index.html -> dist/index.html
✓ Synced: ./dist/index.html -> dist/index.html
✓ Synced folder: ./dist -> dist
✓ Synced 1/1 item(s)
```

`sync-skip` prints `⊘ Skipped (exists)` instead of replacing. Folders are synced recursively, and missing remote directories are created along the way.

## Security

FTP sends your password and your files unencrypted. Use mftp on networks you trust, or prefer SFTP or FTPS when the server supports them.

## License

MIT. See [LICENSE](LICENSE).
