# macOS Command-Line Tool Comparator

A set of scripts designed to inventory and compare the command-line tools available on different versions of macOS. This tool helps you track changes, additions, and version updates of built-in utilities across OS releases.

It works in a two-stage process: first, a collection script gathers data from each target OS, and second, a merge script combines that data into a single, easy-to-read CSV comparison file.

## Features

-   **Robust Version Detection**: Intelligently finds command versions by trying multiple common flags (`--version`, `-V`, `-v`).
-   **Man Page Fallback**: If a version can't be found via flags, the script automatically searches the command's man page.
-   **Man Page Extraction**: Saves a clean text version of every available man page for offline reading and analysis.
-   **Flexible Comparison**: The merge script is not hardcoded and can compare any two datasets you generate.
-   **Error Handling**: Both scripts include checks to handle missing data or unexpected formats gracefully.
-   **Clear Output**: Generates a final CSV file that clearly shows which tools are present on each OS and what their versions are.

## Requirements

To use this toolset, you'll need the following on your system(s):

1.  **A macOS Environment**: The collection script is designed specifically for macOS.
2.  **Zsh**: The default shell in modern macOS, so no action is needed.
3.  **GNU Core Utilities**: The collection script uses `timeout`. The easiest way to install this is via Homebrew.
    ```zsh
    brew install coreutils
    ```
4.  **Python 3**: The merge script requires Python 3. macOS typically comes with Python 3 pre-installed.

## How to Use

The process involves running the collection script on each macOS machine you want to analyze, and then running the merge script to produce the final comparison.

### Step 1: Collect Data on the First OS

On your first machine (e.g., running `macOS Sequoia`), follow these steps:

1.  Clone this repository or download the scripts.
2.  Open your terminal and navigate to the project directory.
3.  Make the collection script executable:
    ```zsh
    chmod +x collect_data.sh
    ```
4.  Run the script, providing a short name for the OS you are analyzing. This name will be used for the output files.
    ```zsh
    # Example for macOS Sequoia
    ./collect_data.sh sequoia
    ```
    This command will create:
    -   A data file: `command_data_sequoia.tsv`
    -   A directory with man pages: `man_pages_sequoia/`

### Step 2: Collect Data on the Second OS

Repeat the process from Step 1 on your second machine (e.g., running `macOS Tahoe`).

1.  Run the same collection script on the second machine.
    ```zsh
    # Example for macOS Tahoe
    ./collect_data.sh tahoe
    ```
    This command will create:
    -   A data file: `command_data_tahoe.tsv`
    -   A directory with man pages: `man_pages_tahoe/`

### Step 3: Merge the Results

Once you have the data from both systems, you can generate the final comparison report.

1.  Copy the `.tsv` file from one of the machines so that both `command_data_sequoia.tsv` and `command_data_tahoe.tsv` are in the same directory as the `merge_results.py` script.
2.  Run the Python merge script from your terminal, providing the two OS names you used in the previous steps as command-line arguments.
    ```zsh
    python3 merge_results.py sequoia tahoe
    ```
3.  The script will generate the final report. You can customize the output filename:
    ```zsh
    python3 merge_results.py sequoia tahoe --output macos_comparison_report.csv
    ```

## Output Explained

The scripts will produce three types of output:

1.  **Man Page Directories (`man_pages_<os_name>/`)**: These folders contain the extracted man pages as plain text files, named like `man_php_sequoia.txt`.

2.  **Intermediate Data Files (`command_data_<os_name>.tsv`)**: These are tab-separated files used by the merge script. They contain the raw data collected for a single OS.

3.  **Final Comparison CSV (`command_comparison.csv`)**: This is the main output file. It is a semicolon-separated file structured as follows:

| Command Name | Version                  | macOS Sequoia | macOS Tahoe |
| :----------- | :----------------------- | :-----------: | :---------: |
| `php`        | 8.3.1                    |      Yes      |     Yes     |
| `awk`        | 20200816 (from man page) |      Yes      |     Yes     |
| `emacs`      | N/A                      |      No       |     Yes     |
| `python3`    | 3.9.6                    |      Yes      |     No      |

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
