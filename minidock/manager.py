import os
import signal
import subprocess
import json
from .engine import run_process  # type: ignore

PROCESSES_FILE = os.path.join(os.path.dirname(__file__), 'processes.json')

def load_processes() -> dict:
    if not os.path.exists(PROCESSES_FILE):
        return {}
        
    try:
        with open(PROCESSES_FILE, 'r') as f:
            parsed = json.load(f)
            return {int(pid): proc for pid, proc in parsed.items()}
    except Exception:
        return {}

def save_processes():
    with open(PROCESSES_FILE, 'w') as f:
        json.dump(processes, f, indent=2)

processes: dict = load_processes()

def cleanup_processes():
    """Removes dead processes from state properly"""
    global processes
    dead_pids = []
    
    for pid in processes:
        if os.name == 'nt':
            check = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
            if "No tasks" in check.stdout or str(pid) not in check.stdout:
                dead_pids.append(pid)
        else:
            try:
                os.kill(pid, 0)
            except OSError:
                dead_pids.append(pid)
    
    for pid in dead_pids:
        processes.pop(pid, None)
    
    if dead_pids:
        save_processes()

def start_process(name, command, root=None):
    cleanup_processes()
    
    if name:
        for proc in processes.values():
            if proc.get("name") == name:
                print(f"[MiniDock] Error: Name '{name}' is already in use")
                return None
    
    pid = run_process(command, root)
    processes[pid] = {
        "name": name,
        "command": command,
        "root": root
    }
    save_processes()
    return pid

def list_processes():
    cleanup_processes()
    return processes

def get_pid_by_name(name):
    cleanup_processes()
    for pid, proc in processes.items():
        if proc.get("name") == name:
            return pid
    return None

def stop_process(pid):
    cleanup_processes()
    
    if pid not in processes:
        return False

    try:
        if os.name == 'nt':
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                capture_output=True,
                text=True
            )
        else:
            os.kill(pid, signal.SIGTERM)

    except Exception as e:
        print(f"[MiniDock] Error: {e}")

    # Remove process safely after stopping
    processes.pop(pid, None)
    save_processes()
    return True