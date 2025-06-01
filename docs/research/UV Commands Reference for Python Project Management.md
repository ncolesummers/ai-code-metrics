# UV Commands Reference for Python Project Management

UV is an extremely fast Python package and project manager written in Rust that serves as a drop-in replacement for pip, pip-tools, pipx, poetry, pyenv, virtualenv, and more. This comprehensive reference covers all aspects of UV commands organized into 10 key categories.

## 1. Core UV Commands for Python Project Management

### Basic Project Commands
- **`uv init [project-name]`** - Initialize a new Python project
  - `--app` - Create an application project (default)
  - `--lib` - Create a library project with src layout
  - `--package` - Create a packaged project with build system
  - `--build-backend <backend>` - Choose build system (hatchling, setuptools, etc.)
  - `--bare` - Create minimal project without extra files
  - Example: `uv init my-app --lib`

- **`uv run [command]`** - Run commands in the project environment
  - Automatically syncs environment before running
  - `--frozen` - Don't update lockfile
  - `--locked` - Error if lockfile is outdated
  - `--no-sync` - Skip environment sync
  - `--python <version>` - Use specific Python version
  - Example: `uv run python script.py`

- **`uv sync`** - Sync project environment with lockfile
  - `--all-extras` - Include all optional dependencies
  - `--extra <name>` - Include specific extras
  - `--dev` / `--no-dev` - Include/exclude dev dependencies
  - `--frozen` - Use lockfile as-is without updates
  - `--locked` - Error if lockfile needs updates
  - Example: `uv sync --all-extras --dev`

- **`uv lock`** - Create/update lockfile (uv.lock)
  - `--locked` - Error if lockfile would change
  - `--upgrade` - Upgrade all packages
  - `--upgrade-package <name>` - Upgrade specific package
  - Example: `uv lock --upgrade-package requests`

### Help and Version Commands
- **`uv help [command]`** - Display detailed help for commands
- **`uv --version`** / **`uv -V`** - Show UV version
- **`uv self version`** - Show detailed version with build info

## 2. Project Initialization and Setup Commands

### Project Creation
- **`uv init`** - Create new project in current directory
  - `--app` - Application project (default, no build system)
  - `--lib` - Library project with src/ layout and build system
  - `--package` - Force build system inclusion
  - `--build-backend <name>` - Specify build backend (hatchling, setuptools, flit-core, pdm-backend, maturin, scikit-build-core)
  - `--no-package` - Exclude build system
  - `--no-readme` - Skip README creation
  - `--no-pin-python` - Don't create .python-version file
  - Example: `uv init my-lib --lib --build-backend hatchling`

### Python Version Management
- **`uv python install <version>`** - Install Python version
  - Supports version specifiers: `3.11`, `3.11.5`, `pypy@3.8`
  - Downloads from pre-built distributions
  - Example: `uv python install 3.11 3.12`

- **`uv python pin <version>`** - Pin Python version for project
  - Creates .python-version file
  - Example: `uv python pin 3.11`

- **`uv python list`** - List available Python installations
  - `--only-installed` - Show only installed versions

## 3. Dependency Management Commands

### Adding Dependencies
- **`uv add <package>`** - Add dependency to project
  - `--dev` - Add to development dependencies
  - `--group <name>` - Add to specific dependency group
  - `--optional <extra>` - Add to optional dependencies
  - `--editable` - Install in editable mode
  - `--index <url>` - Use specific package index
  - `--extra-index-url <url>` - Add extra index
  - Version constraints: `uv add "requests>=2.0,<3.0"`
  - Git dependencies: `uv add git+https://github.com/user/repo.git`
  - Local paths: `uv add ./local-package`
  - Example: `uv add "fastapi[all]" --dev`

- **`uv add -r requirements.txt`** - Add from requirements file
- **`uv add -c constraints.txt`** - Add with constraints

### Removing Dependencies
- **`uv remove <package>`** - Remove dependency
  - `--dev` - Remove from dev dependencies
  - `--group <name>` - Remove from specific group
  - `--optional <extra>` - Remove from optional dependencies
  - Example: `uv remove requests`

### Dependency Information
- **`uv tree`** - Show dependency tree
  - `--depth <n>` - Limit tree depth
  - `--package <name>` - Show tree for specific package

## 4. Virtual Environment Management

### Environment Creation
- **`uv venv [path]`** - Create virtual environment
  - Default path: `.venv`
  - `--python <version>` - Use specific Python version
  - `--seed` - Install seed packages (pip, setuptools, wheel)
  - `--prompt <name>` - Set environment prompt
  - Example: `uv venv .venv --python 3.11`

### Environment Activation
Virtual environments can be activated using standard methods:
- **Linux/macOS**: `source .venv/bin/activate`
- **Windows**: `.venv\Scripts\activate`
- **Fish**: `source .venv/bin/activate.fish`
- **PowerShell**: `.venv\Scripts\Activate.ps1`

### Environment Variables
- **`UV_PROJECT_ENVIRONMENT`** - Override default .venv location
- **`VIRTUAL_ENV`** - Respected with `--active` flag

## 5. Package Installation and Upgrade Commands

### Installation (pip interface)
- **`uv pip install <package>`** - Install packages
  - `--system` - Install to system Python
  - `--python <path>` - Install to specific Python
  - `--editable` - Editable installation
  - `--no-deps` - Skip dependencies
  - `--force-reinstall` - Force reinstallation
  - `--compile-bytecode` - Compile .py to .pyc files
  - Example: `uv pip install django==4.2`

- **`uv pip install -r requirements.txt`** - Install from requirements
- **`uv pip install -e .`** - Install current project in editable mode

### Synchronization
- **`uv pip sync requirements.txt`** - Sync environment exactly with requirements
  - Uninstalls packages not in requirements
  - `--python <path>` - Target specific Python

### Compilation
- **`uv pip compile requirements.in`** - Generate locked requirements
  - `-o requirements.txt` - Output file
  - `--universal` - Platform-independent resolution
  - `--upgrade` - Upgrade all packages
  - `--upgrade-package <name>` - Upgrade specific package
  - Example: `uv pip compile requirements.in -o requirements.txt`

### Self-Management
- **`uv self update`** - Update UV itself
  - Only works with standalone installer
  - `uv pip install --upgrade uv` for pip installations

## 6. Development Workflow Commands

### Script Execution
- **`uv run <script.py>`** - Run Python script in project environment
- **`uv run python -m <module>`** - Run module
- **`uv run --python <version> <script>`** - Run with specific Python
- **`uv run --isolated <script>`** - Run in isolated environment

### Script Dependencies (PEP 723)
- **`uv add --script <script.py> <package>`** - Add inline dependency
  - Adds dependency metadata to script file
  - Example: `uv add --script example.py requests`

### Testing and Quality
- **`uv run pytest`** - Run tests
- **`uv run ruff check`** - Lint code
- **`uv run mypy .`** - Type checking
- **`uv run black .`** - Format code

### Environment Files
- **`uv run --env-file .env <command>`** - Load environment variables
  - `UV_ENV_FILE` environment variable
  - `--no-env-file` to disable

## 7. Build and Publishing Commands

### Building
- **`uv build`** - Build project distributions
  - Creates both wheel (.whl) and source distribution (.tar.gz)
  - `--sdist` - Build only source distribution
  - `--wheel` - Build only wheel
  - `--out-dir <dir>` - Output directory (default: dist/)
  - `--no-sources` - Ignore tool.uv.sources during build
  - Example: `uv build --wheel`

### Publishing
- **`uv publish`** - Publish to package index
  - `--index-url <url>` - Custom index URL
  - `--token <token>` - Authentication token
  - `--username <name>` / `--password <pass>` - Basic auth
  - `--check-url <url>` - Check if files already exist
  - `--skip-existing` - Skip files that already exist
  - Example: `uv publish --token $PYPI_TOKEN`

### Export
- **`uv export`** - Export lockfile to other formats
  - `-o requirements.txt` - Export to requirements.txt
  - `--format requirements-txt` - Specify format
  - `--no-dev` - Exclude dev dependencies
  - Example: `uv export -o requirements.txt --no-dev`

## 8. Configuration Options and Settings

### Configuration Files
UV reads configuration from:
1. `pyproject.toml` - Project-level (under `[tool.uv]`)
2. `uv.toml` - Project-level (takes precedence over pyproject.toml)
3. `~/.config/uv/uv.toml` - User-level
4. `/etc/uv/uv.toml` - System-level

### Key Configuration Settings
```toml
[tool.uv]
# Python version management
python = "3.11"
managed-python = true

# Index configuration
index-url = "https://pypi.org/simple"
extra-index-url = ["https://download.pytorch.org/whl/cpu"]

# Environment settings
no-cache = false
cache-dir = "/path/to/cache"

# Build settings
compile-bytecode = true
no-build-isolation = false
no-build-isolation-package = ["torch"]

# Dependency sources
[tool.uv.sources]
my-package = { path = "../my-package", package = true }

# Workspace configuration
[tool.uv.workspace]
members = ["packages/*"]
exclude = ["old-packages/*"]

# Index definitions
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"
```

### Environment Variables
- **`UV_CACHE_DIR`** - Cache directory location
- **`UV_CONFIG_FILE`** - Path to config file
- **`UV_NO_CACHE`** - Disable caching
- **`UV_INDEX_URL`** - Default index URL
- **`UV_PYTHON`** - Python version/path to use
- **`UV_SYSTEM_PYTHON`** - Allow system Python usage
- **`UV_FROZEN`** - Run in frozen mode
- **`UV_LOCKED`** - Require lockfile to be up-to-date
- **`UV_NO_SYNC`** - Skip environment sync
- **`UV_COMPILE_BYTECODE`** - Compile bytecode
- **`UV_TOOL_DIR`** - Tool installation directory
- **`UV_PROJECT_ENVIRONMENT`** - Project environment path

### Command-line Options
Common flags available across commands:
- **`--cache-dir <dir>`** - Override cache directory
- **`--no-cache`** - Disable cache usage
- **`--offline`** - Work offline only
- **`--quiet` / `-q`** - Reduce output verbosity
- **`--verbose` / `-v`** - Increase output verbosity
- **`--config-file <path>`** - Use specific config file
- **`--no-config`** - Ignore config files

## 9. Advanced Features and Lesser-Known Commands

### Tools Interface
- **`uvx <command>`** / **`uv tool run <command>`** - Run tool in ephemeral environment
  - `--from <package>` - Specify package providing command
  - `--with <package>` - Include additional packages
  - Example: `uvx ruff check` or `uvx --from httpie http`

- **`uv tool install <package>`** - Install tool permanently
  - `--force` - Overwrite existing installation
  - Example: `uv tool install ruff`

- **`uv tool list`** - List installed tools
- **`uv tool upgrade <tool>`** - Upgrade installed tool
- **`uv tool uninstall <tool>`** - Remove installed tool
- **`uv tool dir`** - Show tools directory
- **`uv tool update-shell`** - Add tool bin directory to PATH

### Cache Management
- **`uv cache dir`** - Show cache directory location
- **`uv cache info`** - Show cache usage information
- **`uv cache clean`** - Clear entire cache
- **`uv cache prune`** - Remove unused cache entries
  - `--ci` - Optimize for CI environments

### Workspace Commands
- **`uv sync --workspace`** - Sync entire workspace
- **`uv run --package <name> <command>`** - Run command in workspace member
- **`uv lock --upgrade-package <name>`** - Upgrade package across workspace

### Lockfile Features
- **Lock file format**: `uv.lock` (TOML-based, human-readable)
- **Cross-platform**: Universal lockfile for all platforms
- **Version control**: Should be committed to source control
- **Export**: Can export to requirements.txt or pylock.toml

### Resolution Control
- **`--resolution <strategy>`** - Control dependency resolution
  - `highest` - Prefer latest versions (default)
  - `lowest-direct` - Minimize direct dependency versions
- **`--prerelease <strategy>`** - Handle pre-releases
  - `disallow` - Exclude pre-releases (default)
  - `allow` - Allow pre-releases
  - `if-necessary` - Use if no stable versions
- **`--upgrade` / `--upgrade-package <name>`** - Force upgrades

### Build Isolation Control
```toml
[tool.uv]
no-build-isolation-package = ["package-name"]
```
- Disables build isolation for specific packages
- Useful for packages with heavy build dependencies

### Override and Constraint Files
- **Override files**: Force specific versions regardless of dependencies
- **Constraint files**: Add bounds without triggering installation
- **Build constraint files**: Control build-time dependency versions

## 10. Best Practices and Common Workflows

### Project Setup Workflow
```bash
# 1. Create new project
uv init my-project --lib

# 2. Add dependencies
uv add "fastapi[all]" uvicorn

# 3. Add development dependencies
uv add --dev pytest black ruff mypy

# 4. Run the project
uv run python -m my_project
```

### Dependency Management Best Practices
1. **Use version constraints appropriately**:
   - `uv add "django>=4.2,<5.0"` for major version bounds
   - `uv add "requests~=2.28.0"` for compatible versions

2. **Organize dependencies by purpose**:
   - Core dependencies in `dependencies`
   - Development tools in dev group
   - Optional features in `optional-dependencies`

3. **Pin Python version**: Use `.python-version` file for consistency

### Development Workflow
```bash
# Daily workflow
uv sync                    # Sync environment
uv run pytest            # Run tests
uv run ruff check .       # Lint code
uv run mypy .            # Type check
uv lock --upgrade         # Update lockfile
```

### CI/CD Integration
```bash
# In CI pipelines
uv sync --locked --all-extras --dev  # Exact environment
uv run pytest --cov                  # Run tests with coverage
uv build                             # Build distributions
```

### Docker Best Practices
```dockerfile
# Multi-stage build for optimal layer caching
FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Install dependencies first (better caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project

# Then copy and install project
COPY . .
RUN uv sync
```

### Performance Optimization
1. **Enable bytecode compilation** for production:
   - `UV_COMPILE_BYTECODE=1` or `--compile-bytecode`

2. **Use cache in CI**:
   - Mount cache directory for faster builds
   - Use `uv cache prune --ci` to optimize cache size

3. **Optimize resolution**:
   - Use `--frozen` when lockfile is current
   - Use `--no-deps` for single package installs

### Migration from Other Tools
- **From pip**: Use `uv pip` interface as drop-in replacement
- **From Poetry**: Convert `poetry.lock` using export/import
- **From Pipenv**: Convert `Pipfile.lock` to requirements.txt first
- **From conda**: Use UV for package management, conda for environments

### Workspace Management
```bash
# Create workspace
uv init --lib albatross
cd albatross
uv init --lib packages/bird-feeder

# Add workspace member as dependency
uv add bird-feeder --source workspace

# Work with workspace
uv sync --workspace        # Sync all members
uv run --package bird-feeder pytest  # Test specific member
```

### Troubleshooting Commands
- **`uv cache clean`** - Clear cache if resolution issues
- **`uv lock --upgrade`** - Force dependency updates
- **`--verbose`** - Debug resolution problems
- **`--offline`** - Work without network
- **`uv tree`** - Understand dependency relationships

This comprehensive reference covers all major UV functionality for Python project management. UV's speed and unified interface make it an excellent replacement for multiple Python packaging tools while providing modern features like lockfiles, workspaces, and robust dependency resolution.