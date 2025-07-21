# macOS Command-Line Tool Comparator

A set of scripts designed to inventory and compare the command-line tools available on different versions of macOS. This tool helps you track changes, additions, and version updates of built-in utilities across OS releases.

It works in a two-stage process: first, a collection script gathers data from each target OS, and second, a merge script combines that data into a single, easy-to-read CSV comparison file.

## Features

-   **Robust Version Detection**: Intelligently finds command versions by trying multiple common flags (`--version`, `-V`, `-v`).
-   **Man Page Fallback**: If a version can't be found via flags, the script automatically searches the command's man page.
-   **Intelligent Status Analysis**: Automatically determines if a command was `Added`, `Removed`, `Upgraded`, `Downgraded`, or remained the `Same`.
-   **Man Page Extraction**: Saves a clean text version of every available man page for offline reading and analysis.
-   **Flexible Comparison**: The merge script is not hardcoded and can compare any two datasets you generate.
-   **Clear Output**: Generates a final CSV file that clearly shows the status of each tool across two operating systems.

## Requirements

To use this toolset, you'll need the following:

1.  **A macOS Environment**: The collection script is designed specifically for macOS.
2.  **Zsh**: The default shell in modern macOS.
3.  **GNU Core Utilities**: The collection script uses `timeout`. Install via Homebrew:
    ```zsh
    brew install coreutils
    ```
4.  **Python 3**: The merge script requires Python 3.
5.  **Python `packaging` library**: Used for accurate version comparison. Install via pip:
    ```zsh
    pip3 install packaging
    ```

## How to Use

The process involves running the collection script on each macOS machine you want to analyze, and then running the merge script to produce the final comparison.

### Step 1: Collect Data

Run the `collect_data.sh` script on each of your target machines. The script takes one argument: a short name for the OS you are analyzing.

**On your first machine (the 'old' version):**

```zsh
# Make the script executable first: chmod +x collect_data.sh
./collect_data.sh sequoia
```

This creates `command_data_sequoia.tsv` and `man_pages_sequoia/`.

**On your second machine (the 'new' version):**

```zsh
./collect_data.sh tahoe
```

This creates `command_data_tahoe.tsv` and `man_pages_tahoe/`.

### Step 2: Merge and Analyze

1.  Place both `.tsv` data files (`command_data_sequoia.tsv` and `command_data_tahoe.tsv`) in the same directory as the `merge_results.py` script.
2.  Run the Python script from your terminal. Provide the 'old' OS name first, and the 'new' OS name second.

    ```zsh
    python3 merge_results.py sequoia tahoe
    ```

3.  The script will generate the final report, `command_comparison.csv`, in the new format.

## Output Explained

The primary output is a semicolon-separated CSV file (`command_comparison.csv`) that you can easily view in a spreadsheet application.

| Command Name | macOS Sequoia | macOS Tahoe | Status     |
| :----------- | :------------ | :---------- | :--------- |
| `php`        | 8,2           | 8,3         | Upgraded   |
| `openssl`    | 3,0,8         | 3,0,8       | Same       |
| `vim`        | 9,0           | N/A         | Removed    |
| `zsh`        | 5,9           | 5,9         | Same       |
| `nano`       | N/A           | 7,2         | Added      |
| `gawk`       | 5,1,0         | 5,2,1       | Upgraded   |
| `xcodebuild` | 15,0,1        | 14,3,1      | Downgraded |

### Status Column Meanings

-   **Upgraded**: The tool exists on both systems, and the version on the newer OS is higher.
-   **Downgraded**: The tool exists on both systems, but the version on the newer OS is lower.
-   **Same**: The tool exists on both systems with the identical version string.
-   **Added**: The tool is present on the newer OS but not on the older one.
-   **Removed**: The tool was present on the older OS but has been removed from the newer one.
-   **Changed**: The tool exists on both, but its version format is non-standard (e.g., a date or hash) and has changed.
