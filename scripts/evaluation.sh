#! /bin/bash

# evaluation.sh
# ------------
# Usage: ./evaluation.sh /path/to/X
#
# Scans each subdirectory of X for JSON files (excluding results.json)
# and runs src/evaluation.py on that directory.

set -euo pipefail
set -o xtrace

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 /path/to/X"
  exit 1
fi

INPUT_ROOT="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/src"
EVAL_SCRIPT="$SCRIPT_DIR/evaluation.py"

if [[ ! -d "$INPUT_ROOT" ]]; then
  echo "Error: '$INPUT_ROOT' is not a directory." >&2
  exit 1
fi

if [[ ! -f "$EVAL_SCRIPT" ]]; then
  echo "Error: Evaluation script not found at '$EVAL_SCRIPT'." >&2
  exit 1
fi

echo "Recursively scanning '$INPUT_ROOT' for directories with JSON outputs..."

# Find all JSON files (excluding results.json), extract their parent dirs, unique-sort them
mapfile -t DIRS_WITH_JSON < <(
  find "$INPUT_ROOT" -type f -name "*.json" ! -name "results.json" \
    -exec dirname {} \; | sort -u
)

if [[ ${#DIRS_WITH_JSON[@]} -eq 0 ]]; then
  echo "No JSON files found under '$INPUT_ROOT'." 
  exit 0
fi

for dir in "${DIRS_WITH_JSON[@]}"; do
  echo
  echo "››› Evaluating directory: $dir"
  python3 "$EVAL_SCRIPT" --input_folder "$dir"
done

echo
echo "All done."
