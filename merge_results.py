import csv
import os
import argparse
from collections import defaultdict
from typing import Dict, DefaultDict, Optional

# --- NEW: Dependency Check ---
# We use the 'packaging' library for robust version comparison.
# This block checks if it's installed and provides instructions if it's not.
try:
    from packaging.version import parse as parse_version, InvalidVersion
except ImportError:
    print("Error: The required 'packaging' library is not found.")
    print("Please install it by running: pip3 install packaging")
    exit(1)

#
# Part 2: Results Merger (v3 - with Status Logic)
#
# This script merges data and calculates the status (e.g., Upgraded, Added).
#
# Usage: python3 merge_results.py <os1_name> <os2_name>
# Example: python3 merge_results.py sequoia tahoe
#

def determine_status(v1_raw: Optional[str], v2_raw: Optional[str]) -> str:
    """Compares two version strings to determine the command's status."""

    # Helper to clean version strings for comparison
    def clean_ver(v_str):
        if not v_str or v_str == "N/A":
            return None
        return v_str.replace(" (from man page)", "").strip()

    v1 = clean_ver(v1_raw)
    v2 = clean_ver(v2_raw)

    if v1 and not v2:
        return "Removed"
    if not v1 and v2:
        return "Added"
    if not v1 and not v2:
        return "Unknown" # Should not happen if command is in the list

    # At this point, both versions are present
    if v1 == v2:
        return "Same"

    try:
        # Use the powerful packaging.version.parse for accurate comparison
        parsed_v1 = parse_version(v1)
        parsed_v2 = parse_version(v2)

        if parsed_v2 > parsed_v1:
            return "Upgraded"
        elif parsed_v2 < parsed_v1:
            return "Downgraded"
        else: # Covers cases where versions are equivalent, e.g., 1.2 and 1.2.0
            return "Same"
    except InvalidVersion:
        # Fallback for non-standard versions (e.g., dates, hashes)
        return "Changed"

def format_version_for_display(version_str: Optional[str]) -> str:
    """Cleans and formats a version string for the final output."""
    if not version_str or version_str == "N/A":
        return "N/A"

    clean_version = version_str.replace(" (from man page)", "").strip()
    # Format according to user preference (comma as decimal separator)
    return clean_version.replace('.', ',')

def read_data_file(os_name: str, all_commands: DefaultDict[str, Dict]):
    """Reads a TSV file and populates the command dictionary."""
    file_path = f"command_data_{os_name}.tsv"
    if not os.path.exists(file_path):
        print(f"Warning: Data file not found for '{os_name}'. Skipping. Searched for: {file_path}")
        return

    print(f"Reading data from {file_path}...")
    with open(file_path, mode='r', newline='', encoding='utf-8') as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        next(reader, None) # Skip header
        for i, row in enumerate(reader, 2):
            if len(row) < 2:
                print(f"Warning: Skipping malformed row {i} in {file_path}.")
                continue
            command_name, version = row[0], row[1]
            all_commands[command_name][f"{os_name}_version"] = version

def main():
    """Main function to parse arguments and execute the merge process."""
    parser = argparse.ArgumentParser(
        description="Compares command-line tools between two macOS versions.",
        epilog="Example: python3 merge_results.py sequoia tahoe"
    )
    parser.add_argument("os1_name", help="The name of the 'old' OS (e.g., 'sequoia')")
    parser.add_argument("os2_name", help="The name of the 'new' OS (e.g., 'tahoe')")
    parser.add_argument(
        "-o", "--output",
        default="command_comparison.csv",
        help="The name of the final output CSV file (default: command_comparison.csv)"
    )
    args = parser.parse_args()

    os1, os2, final_csv_file = args.os1_name, args.os2_name, args.output
    all_commands: DefaultDict[str, Dict] = defaultdict(dict)

    read_data_file(os1, all_commands)
    read_data_file(os2, all_commands)

    if not all_commands:
        print("Error: No command data was loaded. Aborting.")
        return

    print(f"\nData read successfully. Now generating report at {final_csv_file}...")
    with open(final_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow([
            "Command Name", f"macOS {os1.capitalize()}", f"macOS {os2.capitalize()}", "Status"
        ])

        for command_name in sorted(all_commands.keys()):
            data = all_commands[command_name]
            v1_raw = data.get(f"{os1}_version")
            v2_raw = data.get(f"{os2}_version")

            status = determine_status(v1_raw, v2_raw)
            v1_display = format_version_for_display(v1_raw)
            v2_display = format_version_for_display(v2_raw)

            writer.writerow([command_name, v1_display, v2_display, status])

    print(f"✅ Report complete! Output saved to: {final_csv_file}")

if __name__ == "__main__":
    main()
