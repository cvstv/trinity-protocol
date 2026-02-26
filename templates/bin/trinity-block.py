#!/usr/bin/env python3
"""
Trinity Protocol: Block Counter Manager
"""
import sys
import os
import re

INDEX_FILE = os.path.join("docs", "sprints", "INDEX.md")

def main():
    if not os.path.exists(INDEX_FILE):
        print(f"Error: {INDEX_FILE} not found. Ensure you are in the project root.", file=sys.stderr)
        sys.exit(1)
        
    if len(sys.argv) < 2:
        print("Usage: python trinity-block.py [increment|reset|set <count>|get]", file=sys.stderr)
        sys.exit(1)
        
    action = sys.argv[1]
    
    with open(INDEX_FILE, "r") as f:
        content = f.read()
        
    # Find active blocks count using regex
    match = re.search(r'^blocks:\s*(\d+)$', content, re.MULTILINE)
    if match is None:
        print(f"Error: Could not find 'blocks: N' in {INDEX_FILE} YAML frontmatter.", file=sys.stderr)
        sys.exit(1)
        
    current_blocks = int(match.group(1))
    
    def update_blocks(new_count):
        new_content = re.sub(r'^blocks:\s*\d+$', f"blocks: {new_count}", content, count=1, flags=re.MULTILINE)
        with open(INDEX_FILE, "w") as f:
            f.write(new_content)
        print(f"Block count updated to {new_count}")

    if action == "increment":
        update_blocks(current_blocks + 1)
    elif action == "reset":
        update_blocks(0)
    elif action == "set":
        if len(sys.argv) < 3:
            print("Error: Must provide a number for 'set'", file=sys.stderr)
            sys.exit(1)
        try:
            new_count = int(sys.argv[2])
            update_blocks(new_count)
        except ValueError:
            print("Error: Block count must be an integer", file=sys.stderr)
            sys.exit(1)
    elif action == "get":
        print(current_blocks)
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        print("Usage: python trinity-block.py [increment|reset|set <count>|get]", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
