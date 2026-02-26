#!/usr/bin/env python3
"""
Trinity Protocol: Activity Log Appender
"""
import sys
import os
import shutil
from datetime import datetime

ACTIVITY_FILE = "ACTIVITY.md"

def main():
    if not os.path.exists(ACTIVITY_FILE):
        print(f"Error: {ACTIVITY_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2 or not sys.argv[1]:
        print("Usage: python trinity-log.py \"<role>ROLE</role> — <action>Action</action> — [outcome]\"", file=sys.stderr)
        sys.exit(1)

    log_message = sys.argv[1]
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M]")
    entry = f"{timestamp} {log_message}"

    # Append the entry
    with open(ACTIVITY_FILE, "a") as f:
        f.write(entry + "\n")
    print(f"Logged: {entry}")

    # Log Rotation/Archival Logic (Archiving after 500 lines)
    with open(ACTIVITY_FILE, "r") as f:
        lines = f.readlines()
    
    if len(lines) > 500:
        archive_dir = os.path.join("docs", "archive")
        os.makedirs(archive_dir, exist_ok=True)
        archive_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_file = os.path.join(archive_dir, f"ACTIVITY_{archive_timestamp}.md")
        
        # Keep header (top 25) and last 50 lines, move the rest
        header_lines = []
        for i in range(min(25, len(lines))):
            header_lines.append(lines[i])
            
        archive_lines = []
        for i in range(25, max(25, len(lines) - 50)):
            archive_lines.append(lines[i])
            
        tail_lines = []
        for i in range(max(0, len(lines) - 50), len(lines)):
            tail_lines.append(lines[i])
        
        # Write to archive file
        with open(archive_file, "w") as f:
            f.writelines(header_lines)
            f.writelines(archive_lines)
        
        # Keep top 25 and bottom 50 in active log
        with open(ACTIVITY_FILE, "w") as f:
            f.writelines(header_lines)
            f.writelines(tail_lines)
            
        print(f"Log rotated. Older entries moved to {archive_file}")

if __name__ == "__main__":
    main()
