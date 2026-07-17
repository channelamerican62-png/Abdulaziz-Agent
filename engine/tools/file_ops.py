import os
import re
from typing import List, Dict, Any, Optional

def view_file_lines(filepath: str, start_line: int = 1, end_line: int = 200) -> str:
    """Read a specific range of lines from a file with line numbers (Claude Code style)."""
    if not os.path.exists(filepath):
        return f"[ERROR] File not found: {filepath}"
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        start_idx = max(0, start_line - 1)
        end_idx = min(total_lines, end_line)
        
        output = [f"File: {filepath} (Showing lines {start_line} to {end_idx} of {total_lines})"]
        for idx in range(start_idx, end_idx):
            output.append(f"{idx + 1}: {lines[idx].rstrip()}")
        
        return "\n".join(output)
    except Exception as e:
        return f"[ERROR] Could not read file {filepath}: {str(e)}"

def replace_code_chunk(filepath: str, target_content: str, replacement_content: str) -> str:
    """Replace an exact chunk of code inside a file autonomously."""
    if not os.path.exists(filepath):
        return f"[ERROR] File not found: {filepath}"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if target_content not in content:
            return f"[ERROR] Target content not found in {filepath}. Ensure exact whitespace and line matches."
        
        new_content = content.replace(target_content, replacement_content, 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return f"[SUCCESS] Successfully modified {filepath}."
    except Exception as e:
        return f"[ERROR] Failed to modify file: {str(e)}"

def search_workspace(directory: str, query: str, file_extensions: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Search for code patterns across all files in a directory."""
    results = []
    if not os.path.exists(directory):
        return results
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file_extensions and not any(file.endswith(ext) for ext in file_extensions):
                continue
            
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    for line_num, line in enumerate(f, 1):
                        if query.lower() in line.lower():
                            results.append({
                                "file": filepath,
                                "line": line_num,
                                "snippet": line.strip()
                            })
                            if len(results) >= 50:  # Cap at 50 results
                                return results
            except Exception:
                continue
    return results
