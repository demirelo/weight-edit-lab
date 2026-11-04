"""Audit Claude editor transcripts (stream-json) for the Laya reruns.

For each step: count tool calls, list paths touched outside the workspace and the
allowed read-only inputs, and count reads the sandbox blocked ("not permitted").

  python audit_transcripts.py [rep]     # default rep 1
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REP = sys.argv[1] if len(sys.argv) > 1 else "1"
# Read-only inputs an editor legitimately uses (venv, Laya code and weights, departments text).
ALLOWED = (os.path.join(HERE, "laya_lab.py"), os.path.join(HERE, "departments.py"), os.path.join(HERE, "hub"),
           os.path.abspath(os.path.join(HERE, "..", ".venv")), "/usr/", "/System/", "/opt/homebrew/", "/dev/", "/tmp", "/private/tmp")
PATH_RE = re.compile(r"(?<![\w.])(/(?:Users|private|tmp|opt|etc|var)[^\s'\"`;,)]+)")


def tool_events(log):
    for line in open(log, errors="replace"):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = ev.get("message", {})
        for c in msg.get("content", []) if isinstance(msg, dict) else []:
            if isinstance(c, dict) and c.get("type") in ("tool_use", "tool_result"):
                yield c


rows = []
for log in sorted(glob.glob(f"{HERE}/runs/seed*/*-r{REP}/step*/editor.log")):
    ws_marker = os.path.basename(os.path.dirname(os.path.dirname(log)))
    calls, outside, blocked = 0, set(), 0
    for c in tool_events(log):
        text = json.dumps(c.get("input", c.get("content", "")))
        if c["type"] == "tool_use":
            calls += 1
            for p in PATH_RE.findall(text):
                if ws_marker in p or any(p.startswith(a) for a in ALLOWED):
                    continue
                outside.add(p)
        elif "not permitted" in text.lower():
            blocked += 1
    rows.append({"log": os.path.relpath(log, HERE), "tool_calls": calls, "blocked_reads": blocked,
                 "outside_paths": sorted(outside)})
    flag = "  <-- CHECK" if outside or blocked else ""
    print(f"{rows[-1]['log']}: {calls} tool calls, {blocked} blocked, {len(outside)} outside paths{flag}")
    for p in sorted(outside)[:5]:
        print("     ", p)
json.dump(rows, open(f"{HERE}/results/transcript_audit_r{REP}.json", "w"), indent=1)
print(f"{len(rows)} steps audited; {sum(1 for r in rows if r['tool_calls'] == 0)} with no tool calls recorded")
