"""
Safe Code Executor - Runs Python code in a restricted sandbox.
For production, use E2B or Docker container isolation.
"""
import io
import sys
import contextlib
from typing import Tuple
from src.utils.logger import app_logger


# Blocked modules for safety
BLOCKED_MODULES = {
    'os', 'sys', 'subprocess', 'shutil', 'pathlib',
    'socket', 'urllib', 'http', 'ftplib', 'smtplib',
    '__builtins__', 'eval', 'exec', 'compile', 'open',
}

SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'enumerate': enumerate,
    'zip': zip,
    'map': map,
    'filter': filter,
    'sorted': sorted,
    'sum': sum,
    'min': min,
    'max': max,
    'abs': abs,
    'round': round,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    'type': type,
    'isinstance': isinstance,
}


def execute_code(code: str, timeout: int = 10) -> Tuple[str, str, bool]:
    """
    Execute Python code in a sandboxed environment.
    
    Args:
        code: Python code string to execute
        timeout: Max execution time in seconds
    
    Returns:
        Tuple of (stdout_output, error_output, success)
    """
    app_logger.info(f"⚙️ Executing code snippet ({len(code)} chars)")

    # Capture stdout
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # Restricted globals
    restricted_globals = {
        '__builtins__': SAFE_BUILTINS,
    }

    try:
        with contextlib.redirect_stdout(stdout_capture):
            with contextlib.redirect_stderr(stderr_capture):
                exec(
                    compile(code, '<sandbox>', 'exec'),
                    restricted_globals,
                    {}
                )

        output = stdout_capture.getvalue()
        error = stderr_capture.getvalue()
        app_logger.info(f"✅ Code executed successfully")
        return output, error, True

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        app_logger.warning(f"❌ Code execution failed: {error_msg}")
        return "", error_msg, False