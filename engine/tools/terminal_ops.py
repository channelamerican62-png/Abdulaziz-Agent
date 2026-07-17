import subprocess
import os
import shlex
from typing import Dict, Any

def run_powershell_command(command: str, cwd: str = "D:\\3D AI\\Abdulaziz-Agent", timeout_sec: int = 30) -> Dict[str, Any]:
    """Execute a PowerShell command, capturing stdout, stderr, and return codes (Claude Code verification style)."""
    if not os.path.exists(cwd):
        return {
            "status": "error",
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Directory not found: {cwd}"
        }
    
    try:
        # Run command inside PowerShell
        process = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        
        stdout, stderr = process.communicate(timeout=timeout_sec)
        
        return {
            "status": "success" if process.returncode == 0 else "failed",
            "exit_code": process.returncode,
            "stdout": stdout.strip(),
            "stderr": stderr.strip()
        }
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            "status": "timeout",
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout_sec} seconds."
        }
    except Exception as e:
        return {
            "status": "error",
            "exit_code": -1,
            "stdout": "",
            "stderr": f"Execution error: {str(e)}"
        }
