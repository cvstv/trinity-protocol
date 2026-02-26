#!/usr/bin/env python3
"""
Trinity Protocol: State Transition Manager
"""
import sys
import os
import re

INDEX_FILE = os.path.join("docs", "sprints", "INDEX.md")

VALID_STATUSES = [
    "in-review", "approved", "blocked", "in-progress", 
    "builder-blocked", "complete", "diff-blocked", "merged", "human-review"
]

def main():
    if not os.path.exists(INDEX_FILE):
        print(f"Error: {INDEX_FILE} not found. Ensure you are in the project root.", file=sys.stderr)
        sys.exit(1)
        
    if len(sys.argv) < 2:
        print("Usage: python trinity-transition.py <new-status>", file=sys.stderr)
        print(f"Valid statuses: {', '.join(VALID_STATUSES)}", file=sys.stderr)
        sys.exit(1)
        
    new_status = sys.argv[1]
    
    if new_status not in VALID_STATUSES:
        print(f"Error: '{new_status}' is not a valid sprint status.", file=sys.stderr)
        print(f"Valid statuses: {', '.join(VALID_STATUSES)}", file=sys.stderr)
        sys.exit(1)
        
    with open(INDEX_FILE, "r") as f:
        content = f.read()
        
    # Determine the implied next role based on the status
    next_role = "UNKNOWN"
    if new_status in ["in-review", "complete"]:
        next_role = "ARCHITECT"
    elif new_status in ["approved", "in-progress", "diff-blocked"]:
        next_role = "BUILDER"
    elif new_status in ["blocked", "builder-blocked", "merged"]:
        next_role = "ORCHESTRATOR"
    elif new_status == "human-review":
        next_role = "HUMAN"
        
    # Update the status in the YAML frontmatter
    content = re.sub(r'^sprint_status:\s*.*$', f"sprint_status: {new_status}", content, count=1, flags=re.MULTILINE)
    
    # Update the active_role in the YAML frontmatter
    content = re.sub(r'^active_role:\s*.*$', f"active_role: {next_role}", content, count=1, flags=re.MULTILINE)
    
    with open(INDEX_FILE, "w") as f:
        f.write(content)
        
    print(f"Transitioned to {new_status}. Next dispatched role: {next_role}")

if __name__ == "__main__":
    main()
