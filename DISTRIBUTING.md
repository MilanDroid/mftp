# Distribution Guide for mFTP

This guide is for developers/maintainers who want to build and distribute this package.

## Building Distribution Packages

### Prerequisites

Install the build tools:
```bash
pip install build wheel twine
```

### Building

From the project root directory:

```bash
python -m build
```

This creates two files in the `dist/` directory:
- `mftp_client-1.0.0-py3-none-any.whl` - Universal wheel (works on any platform)
- `mftp_client-1.0.0.tar.gz` - Source distribution

### What Gets Included

The build process includes:
- `ftp_client.py` - Main application code
- `README.md` - Documentation
- `LICENSE` - License file
- `requirements.txt` - Dependencies
- `setup.py` and `pyproject.toml` - Package metadata

What's excluded (via `.gitignore`):
- Virtual environments (`.venv`, `venv`, etc.)
- Build artifacts (`build/`, `__pycache__/`, etc.)
- IDE files (`.idea/`, `.vscode/`)
- Git files (`.git/`)

## Distribution Methods

### Method 1: Share Wheel File (Recommended)

The wheel file (`mftp_client-1.0.0-py3-none-any.whl`) is the best way to distribute:

**Advantages:**
- Works on all platforms (Windows, macOS, Linux)
- Faster installation than source
- No build tools required on target system
- Consistent installation experience

**How to share:**
1. Upload to a file server/cloud storage
2. Email to users
3. Include in software packages
4. Host on internal package repository

**Installation:**
```bash
pip install mftp_client-1.0.0-py3-none-any.whl
```

### Method 2: Publish to PyPI

Make the package available to everyone via `pip install`:

1. Create accounts:
   - Production: [pypi.org](https://pypi.org)
   - Testing: [test.pypi.org](https://test.pypi.org)

2. Test upload first:
   ```bash
   twine upload --repository testpypi dist/*
   ```

3. Production upload:
   ```bash
   twine upload dist/*
   ```

4. Users can then install with:
   ```bash
   pip install mftp-client
   ```

### Method 3: Private PyPI Server

For internal distribution, set up a private package server:

1. **Using devpi:**
   ```bash
   pip install devpi-server devpi-client
   devpi-init
   devpi-server --start
   ```

2. **Using pypiserver:**
   ```bash
   pip install pypiserver
   pypi-server -p 8080 ./dist
   ```

3. **Install from private server:**
   ```bash
   pip install mftp-client --index-url http://your-server:8080
   ```

### Method 4: Git Repository

Users can install directly from Git:

```bash
# From GitHub
pip install git+https://github.com/antony/mftp.git

# From specific branch
pip install git+https://github.com/antony/mftp.git@main

# From specific tag
pip install git+https://github.com/antony/mftp.git@v1.0.0
```

### Method 5: Source Tarball

Distribute the `.tar.gz` file for users who want to build from source:

```bash
pip install mftp_client-1.0.0.tar.gz
```

## Version Management

### Updating the Version

When releasing a new version, update these files:

1. `setup.py`:
   ```python
   version="1.1.0",
   ```

2. `pyproject.toml`:
   ```toml
   version = "1.1.0"
   ```

3. Create a git tag:
   ```bash
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin v1.1.0
   ```

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- `MAJOR`: Breaking changes
- `MINOR`: New features (backward compatible)
- `PATCH`: Bug fixes

## Testing Before Distribution

### 1. Local Installation Test

```bash
# Clean previous installations
pip uninstall mftp-client -y

# Install from wheel
pip install dist/mftp_client-1.0.0-py3-none-any.whl

# Test the command
mftp --help
mftp
```

### 2. Virtual Environment Test

```bash
# Create fresh environment
python -m venv test-env
source test-env/bin/activate  # or test-env\Scripts\activate on Windows

# Install and test
pip install dist/mftp_client-1.0.0-py3-none-any.whl
mftp --help

# Clean up
deactivate
rm -rf test-env
```

### 3. Multi-Platform Testing

Test on:
- macOS (if available)
- Linux (Ubuntu/Debian and RHEL/CentOS)
- Windows 10/11

Use VMs or Docker containers for cross-platform testing.

## Checklist Before Distribution

- [ ] Version number updated in `setup.py` and `pyproject.toml`
- [ ] `README.md` updated with new features/changes
- [ ] `LICENSE` file present
- [ ] All tests pass
- [ ] Built fresh packages with `python -m build`
- [ ] Tested installation from wheel file
- [ ] Git tag created for release
- [ ] Release notes written

## CI/CD Automation

### GitHub Actions Example

Create `.github/workflows/release.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - run: pip install build twine
      - run: python -m build
      - run: twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

## Security Considerations

### 1. Dependency Security

Regularly update dependencies:
```bash
pip list --outdated
pip install --upgrade colorama
```

### 2. PyPI Token Security

When publishing to PyPI:
- Use API tokens (not passwords)
- Store tokens securely (GitHub Secrets, environment variables)
- Never commit tokens to version control

### 3. Package Signing

Sign packages for added security:
```bash
gpg --detach-sign -a dist/mftp_client-1.0.0-py3-none-any.whl
```

## Support and Maintenance

### Issue Tracking

Direct users to report issues:
- GitHub Issues: https://github.com/antony/mftp/issues
- Email support
- Internal ticketing system

### Documentation

Keep updated:
- `README.md` - User documentation
- `INSTALL.md` - Installation instructions
- `DISTRIBUTING.md` - This file
- Inline code comments

## File Checklist for Distribution

Essential files in your repository:
- [x] `ftp_client.py` - Main code
- [x] `setup.py` - Setup configuration
- [x] `pyproject.toml` - Modern packaging config
- [x] `requirements.txt` - Dependencies
- [x] `README.md` - User documentation
- [x] `LICENSE` - License file
- [x] `MANIFEST.in` - Package data specification
- [x] `.gitignore` - Git ignore rules
- [x] `INSTALL.md` - Installation guide
- [x] `DISTRIBUTING.md` - This guide

Generated during build (don't commit):
- `dist/` - Distribution packages
- `build/` - Build artifacts
- `*.egg-info/` - Package metadata
- `__pycache__/` - Python cache

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
- [PEP 517](https://www.python.org/dev/peps/pep-0517/) - Build system requirements
- [PEP 518](https://www.python.org/dev/peps/pep-0518/) - pyproject.toml specification