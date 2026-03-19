# MiniDock 🚀

MiniDock is a lightweight, command-line process manager inspired by container runtimes like Docker.
It lets you safely run, track, and kill background tasks while keeping them isolated in their own active working directories.

---

## 📸 Demo



![Run](assets/screenshot1.png)
![PS](assets/screenshot2.png)
![Stop](assets/screenshot3.png)

---

## ✨ Features

* Run commands as isolated processes
* Track running processes using PID
* Stop processes (by PID or name)
* Basic working-directory isolation (`--root`)
* Cross-platform support (Windows / Linux / macOS)
* Persistent container storage via JSON (`processes.json`)
* Named container management (`--name`)

---

## ⚙️ Usage

### ▶️ Run a process

```bash
python main.py run "echo Hello"
```

### 📦 Run with name and isolation

```bash
python main.py run --name app1 --root sandbox "python app.py"
```

### 📋 List running processes

```bash
python main.py ps
```

Example output:

```
PID      | NAME            | COMMAND                        | ROOT
----------------------------------------------------------------------
1234     | app1            | timeout 30                     | sandbox
```

### ⛔ Stop a process

By PID:

```bash
python main.py stop 1234
```

By name:

```bash
python main.py stop app1
```

---

## 🧱 Project Structure

```text
MiniDock/
│
├── minidock/
│   ├── cli.py        # command parsing
│   ├── manager.py    # process lifecycle + tracking
│   ├── engine.py     # process execution
│
├── main.py           # entry point
└── README.md
```

---

## 🧠 How it works

* Uses Python `subprocess` to spawn processes
* Tracks processes in memory and disk (`processes.json`)
* Supports simple isolation via working directory (`cwd`)
* Uses:
  * `taskkill` on Windows
  * `SIGTERM` on Unix systems

---

## 🚧 Current Limitations

* No true containerization (no cgroups, namespaces, etc.)
* No resource limits (CPU / memory)
* Isolation is directory-based, not network or user-isolated

---

## 🔥 Future Improvements

* Logs system (`minidock logs <name>`)
* Web dashboard (FastAPI + React)
* Resource monitoring (CPU / memory limits)

---

## 🎯 Why this project

MiniDock was built to understand how container runtimes work at a low level —
especially process execution, isolation, and lifecycle management.

---



## 👤 Author

YASHVITHAA RANI KUMAR