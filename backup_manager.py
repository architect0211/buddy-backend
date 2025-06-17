# backup_manager.py – Snapshot engine for Buddy aiE2™

import os
import shutil
import datetime

BACKUP_ROOT = os.path.abspath("../backup_archive/snapshots")
LOG_FILE = os.path.abspath("../backup_archive/backup_log.txt")

BACKUP_TARGETS = [
    "../runtime_memory",
    "../glass_cards",
    "../core_memory",
    "../scrolls",
    "../code"
]

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

def log_backup(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M]")
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{timestamp} [snapshot] {message}\n")

def create_snapshot():
    timestamp = get_timestamp()
    snapshot_dir = os.path.join(BACKUP_ROOT, timestamp)
    os.makedirs(snapshot_dir, exist_ok=True)

    for target in BACKUP_TARGETS:
        if not os.path.exists(target):
            print(f"⚠️ Skipping missing path: {target}")
            continue
        name = os.path.basename(target)
        destination = os.path.join(snapshot_dir, name)
        try:
            shutil.copytree(target, destination)
            print(f"✅ Backed up {name} to {snapshot_dir}")
        except Exception as e:
            print(f"❌ Failed to back up {name}: {e}")

    log_backup(f"Snapshot created at {timestamp}.")


# Manual run:
if __name__ == "__main__":
    create_snapshot()
