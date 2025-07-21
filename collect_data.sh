#!/bin/zsh

#
# Part 1: Data Collector
# Usage: ./collect_data.sh <os_name>
# Example: ./collect_data.sh sequoia
#
# This script collects command information from a single macOS installation.
# It generates:
# 1. An intermediate data file: command_data_<os_name>.tsv
# 2. A directory with extracted man pages: man_pages_<os_name>/
#

# --- Configuration ---
# Directories to search for commands
local -a cmd_dirs
cmd_dirs=('/bin' '/sbin' '/usr/bin' '/usr/sbin' '/usr/local/bin' '/usr/local/sbin')

# --- Script Logic ---

# Check for OS name argument
if [[ -z "$1" ]]; then
    print "Error: Please provide an OS name."
    print "Usage: $0 <os_name>"
    print "Example: $0 sequoia"
    exit 1
fi

local os_name="$1"
local output_dir="man_pages_${os_name}"
local output_tsv="command_data_${os_name}.tsv"

# Create the output directory for man pages
mkdir -p "$output_dir"
print "Created directory for man pages: $output_dir"

# Create/truncate the TSV file and write the header
# Using tabs (\t) as a separator is safer than commas.
print "Command\tVersion\tHasManPage\tPath" > "$output_tsv"

print "Starting command search... this may take a few minutes."

# Iterate over each directory
for dir in "${cmd_dirs[@]}"; do
    # Check if directory exists
    if [[ ! -d "$dir" ]]; then
        continue
    fi

    # Iterate over each file in the directory
    for cmd_path in "$dir"/*; do
        # Check if the file is an executable and not a directory or symlink
        if [[ -x "$cmd_path" && ! -d "$cmd_path" && ! -L "$cmd_path" ]]; then
            local cmd_name
            local version
            local has_man_page="No"

            cmd_name=$(basename "$cmd_path")

            # 1. Get Version
            # Use timeout to prevent hangs. Capture only the first line.
            version=$(timeout 0.5s "$cmd_path" --version 2>&1 | head -n 1 | tr -d '\n' || print "N/A")
            if [[ -z "$version" ]]; then
                version="N/A"
            fi

            # 2. Check for Man Page and Extract It
            # 'man -w' returns the path to the man page file if it exists.
            local man_path
            man_path=$(man -w "$cmd_name" 2>/dev/null)

            if [[ -n "$man_path" && -e "$man_path" ]]; then
                has_man_page="Yes"
                # Save the formatted man page to a text file
                man "$cmd_name" | col -b > "${output_dir}/man_${cmd_name}_${os_name}.txt"
            fi

            # 3. Write data to TSV file
            print "$cmd_name\t$version\t$has_man_page\t$cmd_path" >> "$output_tsv"
        fi
    done
done

print "✅ Collection complete for '$os_name'."
print "Data file: $output_tsv"
print "Man pages saved in: $output_dir/"
sc
