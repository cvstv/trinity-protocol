#!/usr/bin/env python3
"""
Trinity Protocol: Test Execution Gate
"""
import sys
import os
import re
import subprocess
from datetime import datetime

INDEX_FILE = os.path.join("docs", "sprints", "INDEX.md")
ACTIVITY_FILE = "ACTIVITY.md"

def main():
    if not os.path.exists(INDEX_FILE):
        print(f"Error: {INDEX_FILE} not found. Ensure you are in the project root.", file=sys.stderr)
        sys.exit(1)
        
    if len(sys.argv) < 2:
        print("Usage: python trinity-test.py \"<test-command>\"", file=sys.stderr)
        print("Example: python trinity-test.py \"npm test\"", file=sys.stderr)
        sys.exit(1)
        
    test_command = sys.argv[1]
    print(f"Executing: {test_command}")
    
    # Run the test command
    result = subprocess.run(test_command, shell=True, capture_output=True, text=True)
    
    tests_passed = result.returncode == 0
    status_str = "true" if tests_passed else "false"
    
    print("\n--- Command Output ---")
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    print("----------------------\n")
    
    # Update INDEX.md
    with open(INDEX_FILE, "r") as f:
        content = f.read()
        
    # Check if tests_passing exists, replace it, otherwise add it
    if re.search(r'^tests_passing:', content, re.MULTILINE):
        content = re.sub(r'^tests_passing:\s*(true|false)', f"tests_passing: {status_str}", content, count=1, flags=re.MULTILINE)
    else:
        # Insert it before the end of the frontmatter
        content = content.replace("---\n\n# Sprint Index", f"tests_passing: {status_str}\n---\n\n# Sprint Index")
        
    with open(INDEX_FILE, "w") as f:
        f.write(content)
        
    # Append to ACTIVITY.md
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M]")
    outcome = "Passed" if tests_passed else "Failed"
    log_message = f"{timestamp} <role>BUILDER</role> — <action>Automated Tests</action> — Tests {outcome}: {test_command}"
    
    if os.path.exists(ACTIVITY_FILE):
        with open(ACTIVITY_FILE, "a") as f:
            f.write(log_message + "\n")
            
    if tests_passed:
        print(f"✅ Tests PASSED. Updated INDEX.md (tests_passing: true)")
    else:
        print(f"❌ Tests FAILED (Exit Code {result.returncode}). Updated INDEX.md (tests_passing: false)", file=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
