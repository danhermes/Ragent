# 🧠 Ragent CLI (v0.3) – Dispatch & Task System

This conversational CLI is used to launch and manage Ragent projects via the Blanee assistant. Project types include: `code`, `write`, `plan`.

---

## 🧭 Usage

```bash
python HQ_cli.py
```

### Example Session

```bash
(Blanee) > assign
(Blanee) > What is the type for this task?
> set type code
> set project export_cleaner
> set deliverables technical_design.md, pipeline.py
> set constraints No internet access

(Blanee) > Task task_YYYYMMDD_HHMMSS is ready and created.
```

---

## 🔧 System Modules

| File              | Role                                      |
|-------------------|-------------------------------------------|
| `hq_cli.py` | Entry point and input/output only         |
| `commands.py`     | Handles dispatching commands              |
| `tasks.py`        | Manages task metadata, folders, .goal     |
| `blane_state.py`  | Stores step-by-step session state         |

---

## 📁 Project Output Structure

```
/projects/{project_name}/
  goals/
    {project}.goal.md
/tasks/
  task_{id}.json
blane_state.json
```

---

## 🧪 CLI Commands

| Command        | Description                      |
|----------------|----------------------------------|
| `assign`       | Starts a new task setup session  |
| `set`          | Sets a field value               |
| `status`       | Lists all known tasks            |
| `exit`         | Quit CLI                         |

---

## 🧠 Future

- Meeting auto-scheduling
- Interactive task reviews
- Voice + GUI integrations
