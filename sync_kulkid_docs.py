#!/usr/bin/env python3
"""
sync_kulkid_docs.py
Scans docs/compliance for the 5 authoritative KUL KID documents,
extracts version (from filename first), writes docs/kulkid_docs_index.json,
and optionally triggers fetch_kulkid_data if changes are detected.

Usage:
  python sync_kulkid_docs.py
  RUN_FETCH=1 python sync_kulkid_docs.py
  python sync_kulkid_docs.py --run-fetch
"""
from __future__ import annotations
import argparse, json, os, re, sys, time, importlib
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent
COMPLIANCE_DIR = REPO_ROOT / "docs" / "compliance"
INDEX_PATH = REPO_ROOT / "docs" / "kulkid_docs_index.json"

# Expected documents and simple glob patterns (flexible on spacing/case)
EXPECTED = {
    "compliance_part1": {"pattern": re.compile(r"^kul\s*kid\s*compliance\s*part\s*1.*\.pdf$", re.I)},
    "compliance_part2": {"pattern": re.compile(r"^kul\s*kid\s*compliance\s*part\s*2.*\.pdf$", re.I)},
    "appendix":         {"pattern": re.compile(r"^appendix[_\s-]*kulkid.*\.pdf$", re.I)},
    "tagkart":          {"pattern": re.compile(r"^kul[_\s-]*kid[_\s-]*tag.*\.docx$", re.I)},
    "produktmal":       {"pattern": re.compile(r"^kul[_\s-]*kid[_\s-]*produkt.*mal.*\.docx$", re.I)},
}

VERSION_RX = re.compile(r"(?:v|versjon[_\s-]*)?(\d+\.\d+(?:\.\d+)?)", re.I)

def iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()

def find_file(entry_pattern: re.Pattern, base: Path) -> Path | None:
    if not base.exists(): return None
    for p in base.iterdir():
        if p.is_file() and entry_pattern.search(p.name):
            return p
    return None

def version_from_name(name: str) -> str | None:
    m = VERSION_RX.search(name)
    return m.group(1) if m else None

def read_existing_index() -> dict:
    if INDEX_PATH.exists():
        try:
            return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def build_snapshot() -> dict:
    snapshot = {}
    for key, conf in EXPECTED.items():
        p = find_file(conf["pattern"], COMPLIANCE_DIR)
        if not p:
            snapshot[key] = {"path": None, "filename": None, "version": None, "mtime": None}
            continue
        ver = version_from_name(p.name)
        # Fallback: leave version None if not in filename; content extraction is optional
        snapshot[key] = {
            "path": str(p.as_posix()),
            "filename": p.name,
            "version": ver,
            "mtime": iso(p.stat().st_mtime),
        }
    snapshot["_generated_at"] = iso(time.time())
    return snapshot

def diff(old: dict, new: dict) -> dict:
    changes = {"added": [], "removed": [], "modified": []}
    old_keys = set(k for k in old.keys() if not k.startswith("_"))
    new_keys = set(k for k in new.keys() if not k.startswith("_"))

    for k in sorted(new_keys - old_keys):
        changes["added"].append(k)
    for k in sorted(old_keys - new_keys):
        changes["removed"].append(k)
    for k in sorted(new_keys & old_keys):
        if old.get(k) != new.get(k):
            changes["modified"].append(k)
    return changes

def should_run_fetch(args_run: bool) -> bool:
    if args_run: return True
    return os.environ.get("RUN_FETCH", "") in ("1", "true", "yes")

def trigger_fetch():
    # Tries common entrypoints in fetch_kulkid_data.py
    try:
        mod = importlib.import_module("fetch_kulkid_data")
    except Exception as e:
        print(f"⚠️  Could not import fetch_kulkid_data: {e}")
        return False

    for fn in ("main", "sync", "run"):
        if hasattr(mod, fn) and callable(getattr(mod, fn)):
            try:
                print(f"▶️  Running fetch_kulkid_data.{fn}() …")
                getattr(mod, fn)()
                print("✅ fetch_kulkid_data completed.")
                return True
            except Exception as e:
                print(f"⚠️  fetch_kulkid_data.{fn}() failed: {e}")
    print("⚠️  No callable entrypoint (main/sync/run) found in fetch_kulkid_data.py")
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-fetch", action="store_true", help="Run fetch_kulkid_data if changes detected.")
    args = parser.parse_args()

    COMPLIANCE_DIR.mkdir(parents=True, exist_ok=True)

    old_idx = read_existing_index()
    new_idx = build_snapshot()
    changes = diff(old_idx, new_idx)

    # Write index
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(new_idx, indent=2, ensure_ascii=False), encoding="utf-8")

    # Report
    print("📄 Wrote:", INDEX_PATH.as_posix())
    if any(changes.values()):
        print("🔁 Changes detected:")
        for k, items in changes.items():
            if not items: continue
            print(f"  - {k}: {', '.join(items)}")
    else:
        print("✅ No changes vs existing index.")

    # If any file path is missing, call that out clearly
    missing = [k for k,v in new_idx.items() if not k.startswith("_") and (not v.get('path'))]
    if missing:
        print("⚠️  Missing expected documents:", ", ".join(missing))

    if any(changes.values()) and should_run_fetch(args.run_fetch):
        trigger_fetch()

if __name__ == "__main__":
    main()
