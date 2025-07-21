# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a command-line utility project for comparing CLI tools across different macOS versions. It consists of two standalone scripts:
- `collect_data.sh`: Zsh script that collects command-line tool information on a macOS system
- `merge_results.py`: Python script that compares data from two different macOS versions

## Architecture

The project follows a simple two-phase workflow:
1. **Data Collection Phase**: Run `collect_data.sh` on each macOS system to generate `command_data_<os_name>.tsv` files
2. **Comparison Phase**: Run `merge_results.py` to compare the collected data and generate `command_comparison.csv`

## Key Implementation Details

### collect_data.sh
- Uses `/usr/libexec/PlistBuddy` to get OS name
- Requires GNU coreutils (`timeout` command) - install with `brew install coreutils`
- Creates `man_pages_<os_name>/` directory for extracted man pages
- Outputs tab-separated values with: command name, man page availability, location, version

### merge_results.py
- Python 3 script using only standard library modules
- Accepts two TSV files as arguments and optional output filename
- Generates CSV comparing: availability, location changes, version changes

## Development Commands

Since this is a simple script project without a build system:

```bash
# Make scripts executable (if needed)
chmod +x collect_data.sh
chmod +x merge_results.py

# Run data collection
./collect_data.sh

# Run comparison (example)
./merge_results.py command_data_Monterey.tsv command_data_Sequoia.tsv

# Check Python syntax
python3 -m py_compile merge_results.py
```

## Important Notes

- The project has no external Python dependencies
- GNU coreutils is required for the timeout command in collect_data.sh
- Scripts are designed to be run directly without installation
- Error handling is built into both scripts with informative messages
- The LICENSE file mentioned in README.MD is currently missing