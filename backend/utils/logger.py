"""
Logger function shared by all agents
- INFO (yellow)
- SUCCESS (green)
- ERROR (red)
"""

import datetime

LOG_TO_FILE = False
COLORS = {
    "info": "\033[93m",
    "success": "\033[92m",
    "error": "\033[91m",
    "reset": "\033[0m"
}

def log(agent: str, message: str, level: str = 'info') -> None:
    color = COLORS.get(level, COLORS['info'])
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [{agent}] [{level.upper()}] {message}"

    print(f"{color}{formatted}{COLORS['reset']}")

__all__ = ["log"]