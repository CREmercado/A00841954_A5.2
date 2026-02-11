#!/bin/bash

mkdir -p results/reports

SOURCE_FILE=$1

if [ -z "$SOURCE_FILE" ]; then
    echo "Usage: ./generate_reports.sh <source_file.py>"
    exit 1
fi

BASE_NAME=$(basename "$SOURCE_FILE" .py)

FLAKE8_OUTPUT=$(flake8 "$SOURCE_FILE")

{
echo "Flake8 Report"
echo "Date: $(date)"
echo "-----------------------------------"

if [ -z "$FLAKE8_OUTPUT" ]; then
    echo "No flake8 issues found."
else
    echo "$FLAKE8_OUTPUT"
fi

} > "results/reports/${BASE_NAME}_flake8_report.txt"


# -----------------------------
# Pylint Report
# -----------------------------
{
echo "Pylint Report"
echo "Date: $(date)"
echo "-----------------------------------"
pylint "$SOURCE_FILE" --output-format=text
} > "results/reports/${BASE_NAME}_pylint_report.txt"


echo "Reports generated successfully."
