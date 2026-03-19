import sys
import argparse
from .manager import start_process, list_processes, stop_process, get_pid_by_name  # type: ignore

def handle():
    if len(sys.argv) < 2:
        print("Usage: python main.py <command>")
        return

    cmd = sys.argv[1]

    if cmd == "run":
        parser = argparse.ArgumentParser(prog='minidock run', description='Run a containerized process')
        parser.add_argument('--name', help='Container name (must be unique)')
        parser.add_argument('--root', help='Root directory for isolation')
        parser.add_argument('command', nargs='+', help='Command to run')
        
        try:
            args = parser.parse_args(sys.argv[2:])  # type: ignore
            name = args.name
            root = args.root
            command = ' '.join(args.command)
            
            pid = start_process(name, command, root)
            if pid:
                msg = f"container '{name}' with PID: {pid}" if name else f"PID: {pid}"
                print(f"[MiniDock] Started {msg}")
        except SystemExit:
            pass

    elif cmd == "ps":
        procs = list_processes()
        print(f"{'PID':<8} | {'NAME':<15} | {'COMMAND':<30} | {'ROOT'}")
        print("-" * 70)
        
        for pid, proc in procs.items():
            name = proc.get("name") or "-"
            command = proc.get("command", "")
            
            if len(command) > 27:
                command = command[:25] + ".."
                
            root = proc.get("root") or "-"
            print(f"{str(pid):<8} | {name:<15} | {command:<30} | {root}")

    elif cmd == "stop":
        if len(sys.argv) < 3:
            print("Usage: python main.py stop <PID or NAME>")
            return

        target = sys.argv[2]
        
        if target.isdigit():
            pid = int(target)
        else:
            pid = get_pid_by_name(target)
            if not pid:
                print(f"[MiniDock] Error: Container '{target}' not found")
                return

        if stop_process(pid):
            print(f"[MiniDock] Stopped {target} (PID: {pid})")
        else:
            print(f"[MiniDock] Failed to stop {target}")

    else:
        print(f"[MiniDock] Unknown command '{cmd}'")