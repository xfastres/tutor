#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only tutor gate checker.

Prints problems only. Never writes workspace files.
Exit 0 when there is no ERROR. Exit non-zero on ERROR or unreadable input.
Semantic gaps that this checker cannot prove are WARN, not ERROR.

Usage:
  python check-gates.py [workspace_root]
  python check-gates.py --self-test

workspace_root defaults to the learning workspace named by this skill's
existing config (SKILL.md argument examples are not used). No personal
absolute path is hardcoded.
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path


PART_KEYS = ("conclusion", "reason", "boundary", "example")
PART_VALUES = {"pass", "partial", "missing"}
ASSISTANCE = {
    "independent",
    "light_hint",
    "strong_hint",
    "answer_exposed",
    "unknown",
}
SCORING_TYPES = {
    "recognition",
    "explanation",
    "prediction",
    "diagnosis",
    "generation",
    "execution",
    "transfer",
    "boundary",
    "interview",
}
RETRY_SLOT = 1
BLOCK_CAP = 6
PLAN_CAP = BLOCK_CAP - RETRY_SLOT


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_workspace(root: Path) -> Path | None:
    """Resolve a workspace from files this skill already points at.

    Order: TUTOR_WORKSPACE env, then a relative learning path written in
    this skill's README/workspace docs, then the nearest learning/* that
    contains WORKSPACE.yaml. Never a hardcoded personal absolute path.
    """
    env = os.environ.get("TUTOR_WORKSPACE", "").strip()
    if env:
        candidate = Path(env)
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        return candidate

    text = ""
    for name in ("README.md", "workspace.md", "SKILL.md"):
        path = root / name
        if path.is_file():
            text += "\n" + path.read_text(encoding="utf-8")
    for match in re.finditer(r"learning/[A-Za-z0-9_\-]+/", text):
        rel = match.group(0).rstrip("/")
        for base in (Path.cwd(), root.parent.parent.parent, root.parent.parent):
            candidate = (base / rel).resolve()
            if (candidate / "WORKSPACE.yaml").is_file():
                return candidate

    for base in (Path.cwd(), root.parent.parent.parent, root.parent.parent):
        learning = base / "learning"
        if not learning.is_dir():
            continue
        found = sorted(p.parent for p in learning.glob("*/WORKSPACE.yaml"))
        if len(found) == 1:
            return found[0].resolve()
    return None


def strip_comment(line: str) -> str:
    out = []
    quote = None
    for i, ch in enumerate(line):
        if quote:
            out.append(ch)
            if ch == quote and (i == 0 or line[i - 1] != "\\"):
                quote = None
            continue
        if ch in "'\"":
            quote = ch
            out.append(ch)
            continue
        if ch == "#":
            break
        out.append(ch)
    return "".join(out).rstrip()


def unquote(value: str):
    value = value.strip()
    if value in ("", "null", "Null", "NULL", "~", "None"):
        return None
    if value in ("true", "True", "yes"):
        return True
    if value in ("false", "False", "no"):
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [unquote(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_yaml(text: str):
    """Small YAML subset: maps, lists, scalars, nested indent. No tags."""
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = strip_comment(raw)
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        if "\t" in stripped[:indent]:
            raise ValueError("tabs are not accepted")
        lines.append((indent, stripped.strip()))

    def parse_block(index: int, indent: int):
        if index >= len(lines):
            return None, index
        kind = "list" if lines[index][1].startswith("- ") or lines[index][1] == "-" else "map"
        if kind == "list":
            items = []
            while index < len(lines) and lines[index][0] == indent and (
                lines[index][1].startswith("- ") or lines[index][1] == "-"
            ):
                body = lines[index][1][1:].strip()
                index += 1
                if body == "":
                    child, index = parse_block(index, indent + 2)
                    items.append(child)
                    continue
                if ":" in body and not body.startswith(('"', "'")):
                    key, _, rest = body.partition(":")
                    key = key.strip()
                    rest = rest.strip()
                    node = {}
                    if rest in ("", "|", ">"):
                        if index < len(lines) and lines[index][0] > indent:
                            child, index = parse_block(index, lines[index][0])
                            node[key] = child
                        else:
                            node[key] = None
                    else:
                        node[key] = unquote(rest)
                    while index < len(lines) and lines[index][0] > indent and not (
                        lines[index][0] == indent and lines[index][1].startswith("-")
                    ):
                        if lines[index][1].startswith("-"):
                            break
                        child_indent, child_text = lines[index]
                        if ":" not in child_text:
                            raise ValueError("expected key: %s" % child_text)
                        ckey, _, crest = child_text.partition(":")
                        ckey = ckey.strip()
                        crest = crest.strip()
                        index += 1
                        if crest in ("", "|", ">"):
                            if index < len(lines) and lines[index][0] > child_indent:
                                child, index = parse_block(index, lines[index][0])
                                node[ckey] = child
                            else:
                                node[ckey] = None
                        else:
                            node[ckey] = unquote(crest)
                    items.append(node)
                    continue
                items.append(unquote(body))
            return items, index
        node = {}
        while index < len(lines) and lines[index][0] == indent and not lines[index][1].startswith("-"):
            text_line = lines[index][1]
            if ":" not in text_line:
                raise ValueError("expected key: %s" % text_line)
            key, _, rest = text_line.partition(":")
            key = key.strip()
            rest = rest.strip()
            index += 1
            if rest in ("", "|", ">"):
                if index < len(lines) and lines[index][0] > indent:
                    child, index = parse_block(index, lines[index][0])
                    node[key] = child
                else:
                    node[key] = None
            else:
                node[key] = unquote(rest)
        return node, index

    if not lines:
        return None
    value, index = parse_block(0, lines[0][0])
    if index != len(lines):
        raise ValueError("unparsed yaml near: %s" % lines[index][1])
    return value


class Report:
    def __init__(self):
        self.errors = []
        self.warns = []

    def error(self, message: str):
        self.errors.append(message)

    def warn(self, message: str):
        self.warns.append(message)

    def emit(self) -> int:
        for item in self.errors:
            print("ERROR " + item)
        for item in self.warns:
            print("WARN " + item)
        return 1 if self.errors else 0


def load_yaml_file(path: Path, report: Report, label: str):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        report.error("%s unreadable: %s" % (label, exc))
        return None
    try:
        return parse_yaml(text)
    except Exception as exc:  # noqa: BLE001 - surface parse failure, do not write
        report.error("%s YAML parse failed: %s" % (label, exc))
        return None


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def lesson_number(name: str):
    match = re.search(r"(\d+)", name)
    return int(match.group(1)) if match else None


def is_r0(ev: dict) -> bool:
    task = str(ev.get("task_id") or "")
    return bool(re.search(r"R0", task, re.I))


def is_interview_opening(ev: dict) -> bool:
    return ev.get("type") == "interview" and ev.get("source") == "review"


def is_practice(ev: dict) -> bool:
    task = str(ev.get("task_id") or "")
    return bool(re.search(r"(?:^|-)P\d", task))


def is_examiner(ev: dict) -> bool:
    task = str(ev.get("task_id") or "")
    source = str(ev.get("source") or "")
    return source == "examiner" or bool(re.search(r"(?:^|-)E\d", task))


def interview_ok(ev: dict) -> bool:
    if "corrected" in ev:
        # a system-fault correction never supports expression strong
        return False
    parts = ev.get("parts")
    if not isinstance(parts, dict):
        return False
    if any(parts.get(key) != "pass" for key in PART_KEYS):
        return False
    return ev.get("followup") == "pass" and ev.get("result") == "passed"


def supports_independent_pass(ev: dict) -> bool:
    if "corrected" in ev:
        # a system-fault correction never supports facet ok
        return False
    return ev.get("assistance") == "independent" and ev.get("result") == "passed"


def collect_evidence(workspace: Path, report: Report):
    folder = workspace / "evidence"
    by_id = {}
    by_lesson = {}
    if not folder.is_dir():
        report.warn("%s missing; evidence checks skipped" % folder.name)
        return by_id, by_lesson
    paths = sorted(folder.glob("*.yaml")) + sorted(folder.glob("*.yml"))
    for path in paths:
        if path.name == ".gitkeep":
            continue
        data = load_yaml_file(path, report, path.name)
        if not isinstance(data, dict):
            if data is not None:
                report.error("%s top level is not a mapping" % path.name)
            continue
        items = data.get("evidence")
        if items is None:
            # historical multi-file evidence: one record or a bare list
            items = data.get("items") or []
            if isinstance(data.get("id"), str):
                items = [data]
        if not isinstance(items, list):
            report.error("%s evidence is not a list" % path.name)
            continue
        lesson = data.get("lesson_id")
        for ev in items:
            if not isinstance(ev, dict) or not ev.get("id"):
                report.warn("%s has an evidence item without id" % path.name)
                continue
            ev_id = str(ev["id"])
            if ev_id in by_id:
                report.error("%s duplicates %s also in %s" % (path.name, ev_id, by_id[ev_id]["file"]))
            by_id[ev_id] = {"file": path.name, "ev": ev, "lesson_id": lesson or ev.get("lesson_id")}
            key = str(lesson or ev.get("lesson_id") or path.stem)
            by_lesson.setdefault(key, []).append(ev)
    return by_id, by_lesson


def check_interviews(by_lesson, report: Report):
    for lesson, items in sorted(by_lesson.items()):
        for ev in items:
            if ev.get("type") != "interview":
                continue
            ev_id = ev.get("id")
            parts = ev.get("parts")
            if not isinstance(parts, dict) or any(key not in parts for key in PART_KEYS):
                report.warn("%s %s interview parts incomplete; semantic mapping not fully checked" % (lesson, ev_id))
            else:
                for key in PART_KEYS:
                    if parts.get(key) not in PART_VALUES:
                        report.error("%s %s parts.%s=%r not in pass|partial|missing" % (lesson, ev_id, key, parts.get(key)))
            follow = ev.get("followup")
            if follow is None:
                report.warn("%s %s interview followup absent" % (lesson, ev_id))
            elif follow not in PART_VALUES:
                report.error("%s %s followup=%r not in pass|partial|missing" % (lesson, ev_id, follow))
            if follow == "missing" and ev.get("result") == "passed":
                report.error("%s %s followup missing but result passed" % (lesson, ev_id))
            if ev.get("assistance") not in (None, "independent") and ev.get("result") == "passed":
                report.error(
                    "%s %s assistance=%s same-item correction recorded as independent pass"
                    % (lesson, ev_id, ev.get("assistance"))
                )
            elif "assistance" not in ev:
                report.warn("%s %s interview has no assistance; historical record not reclassified" % (lesson, ev_id))


def check_same_item_corrections(by_lesson, by_id, ks_by_cap, report: Report):
    for lesson, items in sorted(by_lesson.items()):
        for ev in items:
            if ev.get("type") == "interview":
                continue
            if "assistance" not in ev:
                report.warn("%s %s has no assistance; historical record not reclassified" % (lesson, ev.get("id")))
                continue
            if ev.get("assistance") in (None, "independent", "unknown"):
                continue
            if ev.get("result") != "passed":
                continue
            ev_id = str(ev.get("id"))
            used = []
            for cap, ks in ks_by_cap.items():
                for facet in as_list(ks.get("facets")):
                    if not isinstance(facet, dict):
                        continue
                    ids = [str(x) for x in as_list(facet.get("evidence_ids"))]
                    if ev_id in ids and facet.get("state") == "ok":
                        used.append("%s/%s state=ok" % (cap, facet.get("id")))
                transition = ks.get("last_transition") or {}
                reasons = [str(x) for x in as_list(transition.get("reason_evidence_ids"))]
                if ev_id in reasons:
                    used.append("%s last_transition" % cap)
            if used:
                report.error(
                    "%s %s assistance=%s result=passed used as independent pass supporting %s"
                    % (lesson, ev_id, ev.get("assistance"), ", ".join(used))
                )
            else:
                report.error(
                    "%s %s assistance=%s result=passed; same-item correction cannot be an independent pass"
                    % (lesson, ev_id, ev.get("assistance"))
                )


def load_ks(workspace: Path, report: Report):
    folder = workspace / "KNOWLEDGE-STATE"
    found = {}
    if not folder.is_dir():
        report.warn("KNOWLEDGE-STATE missing")
        return found
    for path in sorted(folder.glob("*.yaml")):
        data = load_yaml_file(path, report, path.name)
        if not isinstance(data, dict):
            continue
        ks = data.get("knowledge_state") if isinstance(data.get("knowledge_state"), dict) else data
        cap = str(ks.get("id") or path.stem)
        found[cap] = ks
    return found


def check_expression(ks_by_cap, by_id, report: Report):
    for cap, ks in sorted(ks_by_cap.items()):
        dims = ks.get("dimensions") or {}
        if not isinstance(dims, dict):
            continue
        if dims.get("expression") != "strong":
            continue
        cited = []
        for facet in as_list(ks.get("facets")):
            if isinstance(facet, dict) and facet.get("id") == "interview-expression":
                cited.extend(str(x) for x in as_list(facet.get("evidence_ids")))
        for line in as_list(ks.get("evidence")):
            match = re.search(r"EV-\d+", str(line))
            if match:
                ev = by_id.get(match.group(0), {}).get("ev")
                if ev and ev.get("type") == "interview":
                    cited.append(match.group(0))
        transition = ks.get("last_transition") or {}
        for ev_id in as_list(transition.get("reason_evidence_ids")):
            ev = by_id.get(str(ev_id), {}).get("ev")
            if ev and ev.get("type") == "interview":
                cited.append(str(ev_id))
        cited = list(dict.fromkeys(cited))
        if not cited:
            report.error("%s expression strong without an interview evidence id" % cap)
            continue
        good = []
        for ev_id in cited:
            ev = by_id.get(ev_id, {}).get("ev")
            if not ev:
                report.warn("%s expression cites %s but that EV was not loaded" % (cap, ev_id))
                continue
            if ev.get("type") != "interview":
                continue
            if interview_ok(ev):
                good.append(ev_id)
            else:
                report.error(
                    "%s expression strong cites %s result=%s followup=%s; need passed and followup pass"
                    % (cap, ev_id, ev.get("result"), ev.get("followup"))
                )
        if not good and not any(
            (by_id.get(ev_id, {}).get("ev") or {}).get("type") == "interview" for ev_id in cited
        ):
            report.error("%s expression strong has no loaded interview evidence that passes with followup" % cap)


def check_facet_ok(ks_by_cap, by_id, report: Report):
    for cap, ks in sorted(ks_by_cap.items()):
        for facet in as_list(ks.get("facets")):
            if not isinstance(facet, dict) or facet.get("state") != "ok":
                continue
            ids = [str(x) for x in as_list(facet.get("evidence_ids"))]
            loaded = []
            for ev_id in ids:
                ev = by_id.get(ev_id, {}).get("ev")
                if ev:
                    loaded.append(ev)
                else:
                    report.warn("%s/%s state=ok cites %s not loaded; independence not verified" % (cap, facet.get("id"), ev_id))
            if not loaded:
                continue
            modern = [ev for ev in loaded if "assistance" in ev]
            if not modern:
                report.warn(
                    "%s/%s state=ok cites only pre-assistance evidence %s; independence not verified"
                    % (cap, facet.get("id"), ",".join(ids))
                )
                continue
            if not any(supports_independent_pass(ev) for ev in modern):
                report.error(
                    "%s/%s state=ok but none of %s is assistance=independent result=passed"
                    % (cap, facet.get("id"), ",".join(ids))
                )


def protocol_lesson(number, meta) -> bool:
    """Count cap applies from the protocol named in WORKSPACE.yaml.

    v9.1.1 starts at L0014. Earlier lessons keep their historical counts
    and are not failed for exceeding the current block cap.
    """
    if number is None:
        return False
    protocol = str((meta or {}).get("protocol") or "")
    if protocol in (
        "v9.1.1",
        "9.1.1",
        "v9.1.2",
        "9.1.2",
        "v9.2",
        "9.2",
        "v9.3",
        "9.3",
        "v9.4",
        "9.4",
        "v9.4.1",
        "9.4.1",
        "v9.5",
        "9.5",
    ):
        return number >= 14
    return False


def plan_lesson_type(text: str):
    head = "\n".join(text.splitlines()[:40])
    match = re.search(r"课型[:：]\s*`?(NEW_CONCEPT|PRACTICE|REVIEW|MOCK)", head)
    if match:
        return match.group(1)
    if re.search(r"新概念课|先讲后测", head):
        return "NEW_CONCEPT"
    if re.search(r"复习课|练习课|先测后讲", head):
        return "REVIEW"
    return None


def plan_r0_targets(text: str):
    targets = []
    for line in text.splitlines():
        if not re.search(r"\bR0\b", line):
            continue
        if "面试口述" in line and "R0" not in line.split("面试口述")[0]:
            continue
        for match in re.finditer(r"([a-z0-9\-]+)\s*/\s*([a-z0-9\-]+)", line):
            targets.append((match.group(1), match.group(2)))
    return targets


def interview_enabled(workspace: Path) -> bool:
    """Opt-in interview training. Unique source: MISSION-FORMAT.md 「面试模式」.

    Missing or empty 面试线 is OFF. Explicit 不适用 is OFF.
    Grandfather: any **S-I* success criterion, or a 面试线 that schedules
    oral/mock practice without 不适用, is ON.
    """
    mission = workspace / "MISSION.md"
    if not mission.is_file():
        return False
    text = mission.read_text(encoding="utf-8")
    section = re.search(r"面试线(.*?)(\n## |\Z)", text, re.S)
    if section:
        body = section.group(1)
        if "不适用" in body:
            return False
        if re.search(r"S-I\d", body) or re.search(r"适用|模拟口述|模拟面|求职", body):
            return True
    for line in text.splitlines():
        if "面试线" in line and "不适用" in line:
            return False
    if re.search(r"\*\*S-I\d+", text):
        return True
    for line in text.splitlines():
        if "面试线" in line and "不适用" not in line and re.search(r"模拟|口述|面试", line):
            return True
    return False


def interview_na(workspace: Path, report: Report) -> bool:
    return not interview_enabled(workspace)


def planned_counts(text: str):
    """Count distinct planned scoring tasks. Conditional tasks are not counted."""
    rows = []
    in_table = False
    for line in text.splitlines():
        if re.match(r"\|\s*task_id\s*\|", line):
            in_table = True
            continue
        if in_table:
            if not line.strip().startswith("|"):
                break
            if re.match(r"\|\s*-+", line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells:
                rows.append(cells)
    r0 = p = e = oral = 0
    details = []
    for cells in rows:
        task = cells[0]
        kind = cells[1] if len(cells) > 1 else ""
        if re.search(r"X\d|探测|不计分", task + kind):
            continue
        blob = " ".join(cells)
        if re.search(r"仅当|条件|失败才", blob):
            continue
        if re.search(r"R0", task):
            r0 += 1
            details.append(task + ":R0")
        elif re.search(r"口述|面试", kind) or re.search(r"(?:^|-)I\d", task):
            oral += 1
            details.append(task + ":oral")
        elif re.search(r"(?:^|-)P\d", task):
            p += 1
            details.append(task + ":P")
        elif re.search(r"(?:^|-)E\d", task) or "考官" in kind:
            e += 1
            details.append(task + ":E")
    return {"r0": r0, "p": p, "e": e, "oral": oral, "details": details}


def evidence_counts(items):
    r0 = p = e = oral = 0
    details = []
    for ev in items:
        if ev.get("type") not in SCORING_TYPES and ev.get("type") is not None:
            continue
        label = str(ev.get("id"))
        if is_interview_opening(ev) or (ev.get("type") == "interview" and not is_examiner(ev)):
            oral += 1
            details.append(label + ":oral")
        elif is_r0(ev):
            r0 += 1
            details.append(label + ":R0")
        elif is_practice(ev):
            p += 1
            details.append(label + ":P")
        elif is_examiner(ev):
            e += 1
            details.append(label + ":E")
        else:
            details.append(label + ":other")
    return {"r0": r0, "p": p, "e": e, "oral": oral, "details": details, "n": r0 + p + e + oral}


def check_plans(workspace: Path, by_lesson, meta, report: Report):
    lessons = workspace / "lessons"
    if not lessons.is_dir():
        report.warn("lessons/ missing; plan checks skipped")
        return
    na = interview_na(workspace, report)
    for path in sorted(lessons.glob("*.plan.md")):
        text = path.read_text(encoding="utf-8")
        number = lesson_number(path.name)
        lesson = "L%04d" % number if number is not None else path.stem
        kind = plan_lesson_type(text)
        targets = plan_r0_targets(text)
        items = by_lesson.get(lesson, [])
        for ev in items:
            if ev.get("type") != "interview" or ev.get("source") == "examiner":
                continue
            cap = ev.get("capability_id")
            facet = ev.get("facet_id")
            if not targets:
                report.warn("%s %s opening interview has no parseable R0 target in %s" % (lesson, ev.get("id"), path.name))
                continue
            if not any(cap == c and facet == f for c, f in targets):
                report.error(
                    "%s %s interview target %s/%s does not match R0 %s"
                    % (
                        lesson,
                        ev.get("id"),
                        cap,
                        facet,
                        ", ".join("%s/%s" % pair for pair in targets),
                    )
                )
        counts = planned_counts(text)
        started = "未开始" not in text and bool(items)
        if protocol_lesson(number, meta) and started:
            got = evidence_counts(items)
            if got["n"] > BLOCK_CAP:
                message = "%s scoring interactions %d > %d: %s" % (
                    lesson,
                    got["n"],
                    BLOCK_CAP,
                    ", ".join(got["details"]),
                )
                report.error(message)
            if kind == "NEW_CONCEPT" and got["r0"] != 1 and got["r0"] != 0:
                report.error("%s NEW_CONCEPT R0 count %d, want 1: %s" % (lesson, got["r0"], ", ".join(got["details"])))
            if kind in ("PRACTICE", "REVIEW") and got["r0"] > 3:
                report.error("%s %s R0 count %d > 3: %s" % (lesson, kind, got["r0"], ", ".join(got["details"])))
        elif protocol_lesson(number, meta):
            total = counts["r0"] + counts["p"] + counts["e"] + counts["oral"]
            if total > BLOCK_CAP:
                report.error(
                    "%s plan scoring interactions %d > %d: %s"
                    % (lesson, total, BLOCK_CAP, ", ".join(counts["details"]))
                )
            if kind == "NEW_CONCEPT" and counts["r0"] not in (0, 1):
                report.error("%s plan NEW_CONCEPT R0=%d, want 1" % (lesson, counts["r0"]))
            if kind in ("PRACTICE", "REVIEW") and counts["r0"] > 3:
                report.error("%s plan %s R0=%d > 3" % (lesson, kind, counts["r0"]))
        if na and re.search(r"(面试口述(?!：不排)|E-F)", text):
            report.warn("%s interview mode is off but plan still mentions oral/E-F" % lesson)


def check_review_queue(workspace: Path, report: Report):
    """Active RQ rows must point at a knowledge id that has a KS file."""
    path = workspace / "REVIEW-QUEUE.md"
    if not path.is_file():
        return
    ks_ids = set()
    ks_dir = workspace / "KNOWLEDGE-STATE"
    if ks_dir.is_dir():
        for item in ks_dir.glob("*.yaml"):
            ks_ids.add(item.stem)
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or not re.match(r"RQ-\d+", cells[0]):
            continue
        status = cells[4].lower() if len(cells) > 4 else ""
        if status in ("done", "failed", "status"):
            continue
        kid = cells[1] if len(cells) > 1 else ""
        if not kid or kid in ("知识 ID", "---", "----"):
            continue
        if ks_ids and kid not in ks_ids:
            report.error("REVIEW-QUEUE %s knowledge_id %s has no KNOWLEDGE-STATE file" % (cells[0], kid))


def check_routing_contract(skill_md: Path, failures: list):
    """Deterministic: SKILL.md still lists the v9.4 entry routes."""
    if not skill_md.is_file():
        failures.append("routing: SKILL.md missing")
        return
    text = skill_md.read_text(encoding="utf-8")
    if "## 入口路由" not in text:
        failures.append("routing: missing 入口路由 heading")
    required = (
        "继续 / 下一课 / 接着上次",
        "开始训练",
        "我想学 X / 新主题",
        "讲讲 X / 这题为什么",
        "考我",
        "模拟面",
        "今天只听",
        "15 分钟",
        "不要出题",
        "面试模式默认关",
    )
    for token in required:
        if token not in text:
            failures.append("routing: SKILL.md missing %s" % token)


def check_g5_claims(workspace: Path, report: Report):
    """A plan that claims G5 pass while this run already found evidence errors is inconsistent.

    The specific EV errors are reported by the evidence checks. This only adds the
    gate-claim contradiction so a written pass cannot hide them.
    """
    # intentionally no second copy of EV rules; claim check happens after emit pairing
    return None


def check_workspace(workspace: Path) -> Report:
    report = Report()
    if not workspace.is_dir():
        report.error("workspace not found: %s" % workspace)
        return report
    if not (workspace / "WORKSPACE.yaml").is_file():
        report.error("WORKSPACE.yaml missing under %s" % workspace)
        return report
    meta = load_yaml_file(workspace / "WORKSPACE.yaml", report, "WORKSPACE.yaml")
    by_id, by_lesson = collect_evidence(workspace, report)
    ks = load_ks(workspace, report)
    check_interviews(by_lesson, report)
    check_same_item_corrections(by_lesson, by_id, ks, report)
    check_expression(ks, by_id, report)
    check_facet_ok(ks, by_id, report)
    check_plans(workspace, by_lesson, meta if isinstance(meta, dict) else {}, report)
    check_review_queue(workspace, report)
    check_g5_claims(workspace, report)
    claimed = []
    lessons = workspace / "lessons"
    if lessons.is_dir():
        for path in lessons.glob("*.plan.md"):
            text = path.read_text(encoding="utf-8")
            if re.search(r"G5\s*证据[:：]\s*pass", text):
                number = lesson_number(path.name)
                if number is not None:
                    claimed.append((path.name, "L%04d" % number))
    error_blob = "\n".join(report.errors)
    for name, lesson in claimed:
        if lesson in error_blob or any(lesson in item for item in report.errors):
            report.error("%s records G5 pass but %s has evidence/state errors above" % (name, lesson))
    return report


def snapshot(root: Path):
    digest = hashlib.sha256()
    files = [p for p in root.rglob("*") if p.is_file()]
    for path in sorted(files):
        digest.update(str(path.relative_to(root)).encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest(), len(files)


def write_fixture(root: Path):
    (root / "evidence").mkdir(parents=True)
    (root / "KNOWLEDGE-STATE").mkdir()
    (root / "lessons").mkdir()
    (root / "WORKSPACE.yaml").write_text(
        "timezone: Asia/Shanghai\nprotocol: v9.1.1\nlast_ev: 10\n",
        encoding="utf-8",
    )
    (root / "MISSION.md").write_text(
        "# Mission\n\n## 面试线\n\n- 适用\n",
        encoding="utf-8",
    )
    (root / "evidence" / "L0001.yaml").write_text(
        "\n".join([
            'lesson_id: "L0001"',
            "evidence:",
            '  - id: "EV-0001"',
            '    task_id: "0001-R0a"',
            '    capability_id: "locking-read"',
            '    facet_id: "range-waits"',
            '    type: "prediction"',
            '    result: "passed"',
            '    source: "review"',
            '    assistance: "independent"',
            '  - id: "EV-0002"',
            '    task_id: "0001-I0"',
            '    capability_id: "other-cap"',
            '    facet_id: "other-facet"',
            '    type: "interview"',
            '    result: "passed"',
            '    source: "review"',
            '    assistance: "independent"',
            "    parts:",
            '      conclusion: "pass"',
            '      reason: "pass"',
            '      boundary: "pass"',
            '      example: "pass"',
            '    followup: "missing"',
            '  - id: "EV-0003"',
            '    task_id: "0001-P2"',
            '    capability_id: "main"',
            '    facet_id: "insert-ok"',
            '    type: "generation"',
            '    result: "passed"',
            '    source: "lesson"',
            '    assistance: "light_hint"',
            '  - id: "EV-0004"',
            '    task_id: "0001-P1"',
            '    capability_id: "main"',
            '    facet_id: "insert-ok"',
            '    type: "prediction"',
            '    result: "passed"',
            '    source: "lesson"',
            '    assistance: "independent"',
            "",
        ]),
        encoding="utf-8",
    )
    (root / "KNOWLEDGE-STATE" / "main.yaml").write_text(
        "\n".join([
            "knowledge_state:",
            '  id: "main"',
            "  dimensions:",
            '    expression: "strong"',
            "  facets:",
            '    - id: "insert-ok"',
            '      state: "ok"',
            '      evidence_ids: ["EV-0003"]',
            '    - id: "interview-expression"',
            '      state: "ok"',
            '      evidence_ids: ["EV-0002"]',
            "  last_transition:",
            "    reason_evidence_ids: [\"EV-0003\"]",
            "",
        ]),
        encoding="utf-8",
    )
    (root / "lessons" / "0001-demo.plan.md").write_text(
        "\n".join([
            "# L0001",
            "课型：NEW_CONCEPT",
            "R0：0001-R0a ← locking-read / range-waits",
            "G5 证据：pass",
            "",
            "| task_id | 类型 |",
            "|---|---|",
            "| 0001-R0a | 复习 |",
            "| 0001-I0 | 面试口述 |",
            "| 0001-P1 | 补全 |",
            "",
        ]),
        encoding="utf-8",
    )


def set_ev_result(text: str, ev_id: str, result: str) -> str:
    lines = text.splitlines()
    current = None
    for i, line in enumerate(lines):
        if re.search(r'id:\s*"%s"' % re.escape(ev_id), line):
            current = ev_id
        elif re.search(r'id:\s*"EV-', line):
            current = None
        if current == ev_id and re.search(r"^\s*result:", line):
            lines[i] = re.sub(r'result:\s*"\w+"', 'result: "%s"' % result, line)
            current = None
    return "\n".join(lines) + "\n"


def self_test() -> int:
    import tempfile

    failures = []

    def run_case(name, mutate, expect_error, forbid=(), expect_warn=()):
        with tempfile.TemporaryDirectory(prefix="tutor-gate-") as tmp:
            root = Path(tmp)
            write_fixture(root)
            mutate(root)
            before, nfiles = snapshot(root)
            report = check_workspace(root)
            after, nfiles2 = snapshot(root)
            blob = "\n".join(report.errors)
            warn_blob = "\n".join(report.warns)
            if before != after or nfiles != nfiles2:
                failures.append(name + ": fixture hash changed")
            missing = [token for token in expect_error if token not in blob]
            if missing:
                failures.append(name + ": missing " + ",".join(missing) + "\n" + blob)
            banned = [token for token in forbid if token in blob]
            if banned:
                failures.append(name + ": unexpected " + ",".join(banned) + "\n" + blob)
            missing_w = [token for token in expect_warn if token not in warn_blob]
            if missing_w:
                failures.append(name + ": missing warn " + ",".join(missing_w) + "\n" + warn_blob)

    def noop(_root):
        return None

    # baseline fixture is the bad case used by several asserts; split below
    run_case(
        "followup-missing-passed",
        noop,
        ["EV-0002 followup missing but result passed", "EV-0002 interview target"],
    )
    run_case(
        "same-item-hinted-pass",
        noop,
        ["EV-0003", "independent pass", "insert-ok"],
    )
    run_case(
        "expression-strong-bad-evidence",
        noop,
        ["expression strong cites EV-0002"],
    )

    def hint_not_passed(root: Path):
        path = root / "evidence" / "L0001.yaml"
        text = set_ev_result(path.read_text(encoding="utf-8"), "EV-0003", "partial")
        ks = (root / "KNOWLEDGE-STATE" / "main.yaml").read_text(encoding="utf-8")
        ks = ks.replace('evidence_ids: ["EV-0003"]', 'evidence_ids: ["EV-0004"]')
        ks = ks.replace('["EV-0003"]', '["EV-0004"]')
        ks = ks.replace('expression: "strong"', 'expression: "partial"')
        ks = ks.replace('evidence_ids: ["EV-0002"]', 'evidence_ids: []')
        (root / "evidence" / "L0001.yaml").write_text(text, encoding="utf-8")
        (root / "KNOWLEDGE-STATE" / "main.yaml").write_text(ks, encoding="utf-8")

    run_case(
        "hinted-correction-not-passed-silent",
        hint_not_passed,
        [],
        ["EV-0003 assistance"],
    )

    def matched_oral(root: Path):
        text = (root / "evidence" / "L0001.yaml").read_text(encoding="utf-8")
        text = text.replace('capability_id: "other-cap"', 'capability_id: "locking-read"')
        text = text.replace('facet_id: "other-facet"', 'facet_id: "range-waits"')
        text = text.replace('followup: "missing"', 'followup: "pass"')
        text = set_ev_result(text, "EV-0003", "partial")
        ks = (root / "KNOWLEDGE-STATE" / "main.yaml").read_text(encoding="utf-8")
        ks = ks.replace('expression: "strong"', 'expression: "partial"')
        ks = ks.replace('evidence_ids: ["EV-0003"]', 'evidence_ids: ["EV-0004"]')
        ks = ks.replace('reason_evidence_ids: ["EV-0003"]', 'reason_evidence_ids: ["EV-0004"]')
        (root / "evidence" / "L0001.yaml").write_text(text, encoding="utf-8")
        (root / "KNOWLEDGE-STATE" / "main.yaml").write_text(ks, encoding="utf-8")

    run_case("matching-oral-and-independent", matched_oral, [], ["ERROR"])

    def practice_two(root: Path):
        (root / "lessons" / "0002-practice.plan.md").write_text(
            "\n".join([
                "# L0002",
                "课型：REVIEW",
                "进度：last_done=— | 考官=未开始",
                "",
                "| task_id | 类型 | 题干摘要 |",
                "|---|---|---|",
                "| 0002-R0a | 复习 | |",
                "| 0002-R0b | 复习 | |",
                "| 0002-P1 | 变式 | |",
                "| 0002-E1 | 考官 | |",
                "| 0002-E2 | 考官 | |",
                "",
            ]),
            encoding="utf-8",
        )

    run_case("practice-r0-two-under-cap", practice_two, [], ["L0002 plan"])

    def over_six(root: Path):
        (root / "WORKSPACE.yaml").write_text(
            "timezone: Asia/Shanghai\nprotocol: v9.1.1\nlast_ev: 10\n",
            encoding="utf-8",
        )
        (root / "evidence" / "L0014.yaml").write_text(
            "lesson_id: \"L0014\"\nevidence:\n"
            + "\n".join(
                [
                    '  - id: "EV-100%d"\n    task_id: "0014-P%d"\n    capability_id: "main"\n    facet_id: null\n    type: "prediction"\n    result: "passed"\n    source: "lesson"\n    assistance: "independent"'
                    % (i, i)
                    for i in range(1, 8)
                ]
            ),
            encoding="utf-8",
        )
        (root / "lessons" / "0014-over.plan.md").write_text(
            "课型：REVIEW\n进度：last_done=0014-P7 | 考官=done\n",
            encoding="utf-8",
        )

    run_case("over-six", over_six, ["L0014 scoring interactions 7 > 6", "EV-1001:P"])

    def bad_yaml(root: Path):
        (root / "evidence" / "L0003.yaml").write_text("evidence: [\n  - id: [", encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="tutor-gate-") as tmp:
        root = Path(tmp)
        write_fixture(root)
        bad_yaml(root)
        before, _n = snapshot(root)
        report = check_workspace(root)
        after, _n2 = snapshot(root)
        if before != after:
            failures.append("bad-yaml: checker wrote files")
        if not report.errors:
            failures.append("bad-yaml: expected non-zero")
        elif not any("YAML parse failed" in item for item in report.errors):
            failures.append("bad-yaml: parse error not reported: " + " | ".join(report.errors))

    def interview_off(root: Path):
        (root / "MISSION.md").write_text("# Mission\n\n## Why\n\nlearn sql\n", encoding="utf-8")

    run_case(
        "interview-off-missing-section",
        interview_off,
        [],
        [],
        ["interview mode is off"],
    )

    def interview_na_section(root: Path):
        (root / "MISSION.md").write_text("# Mission\n\n## 面试线\n\n不适用\n", encoding="utf-8")

    run_case(
        "interview-off-explicit-na",
        interview_na_section,
        [],
        [],
        ["interview mode is off"],
    )

    def interview_on_si(root: Path):
        (root / "MISSION.md").write_text(
            "# Mission\n\n## Success\n\n- **S-I1** 能 60 秒讲清锁\n",
            encoding="utf-8",
        )
        (root / "lessons" / "0001-demo.plan.md").write_text(
            "# L0001\n课型：NEW_CONCEPT\n进度：last_done=— | 考官=未开始\n",
            encoding="utf-8",
        )

    run_case("interview-on-si-grandfather", interview_on_si, [], ["interview mode is off"])

    def rq_dangling(root: Path):
        (root / "REVIEW-QUEUE.md").write_text(
            "| id | 知识 ID | due | 做什么 | status | 结果 |\n"
            "|----|---------|-----|--------|--------|------|\n"
            "| RQ-0099 | missing-cap | 2026-10-24 | REPAIR：x | scheduled | |\n",
            encoding="utf-8",
        )

    run_case("rq-dangling", rq_dangling, ["RQ-0099", "missing-cap"])

    def ks_missing_ev(root: Path):
        ks = (root / "KNOWLEDGE-STATE" / "main.yaml").read_text(encoding="utf-8")
        ks = ks.replace('evidence_ids: ["EV-0004"]', 'evidence_ids: ["EV-9999"]')
        ks = ks.replace('evidence_ids: ["EV-0003"]', 'evidence_ids: ["EV-9999"]')
        (root / "KNOWLEDGE-STATE" / "main.yaml").write_text(ks, encoding="utf-8")

    run_case("ks-cites-missing-ev", ks_missing_ev, [], [], ["EV-9999 not loaded"])

    def old_protocol(root: Path):
        (root / "WORKSPACE.yaml").write_text(
            "timezone: Asia/Shanghai\nprotocol: v9.0\nlast_ev: 10\n",
            encoding="utf-8",
        )
        (root / "evidence" / "L0001.yaml").write_text(
            "lesson_id: \"L0001\"\nevidence:\n"
            + "\n".join(
                [
                    '  - id: "EV-10%d"\n    task_id: "0001-P%d"\n    capability_id: "main"\n    facet_id: null\n    type: "prediction"\n    result: "passed"\n    source: "lesson"\n    assistance: "independent"'
                    % (i, i)
                    for i in range(1, 8)
                ]
            ),
            encoding="utf-8",
        )

    run_case("old-protocol-no-block-cap", old_protocol, [], ["scoring interactions 7 > 6"])

    def missing_field(root: Path):
        (root / "KNOWLEDGE-STATE" / "broken.yaml").write_text(
            "knowledge_state:\n  id: [\n    - broken",
            encoding="utf-8",
        )

    run_case("missing-field-yaml", missing_field, ["YAML parse failed"])

    def resume_unfinished(root: Path):
        (root / "lessons" / "0004-resume.plan.md").write_text(
            "\n".join([
                "# L0004",
                "课型：NEW_CONCEPT",
                "教学深度：standard",
                "进度：last_done=0004-P2 | 待重试=— | 考官=未开始",
                "",
            ]),
            encoding="utf-8",
        )

    run_case("resume-unfinished-plan", resume_unfinished, [], ["L0004 scoring"])

    check_routing_contract(skill_root() / "SKILL.md", failures)

    if failures:
        print("SELF-TEST FAIL")
        for item in failures:
            print(item)
        return 1
    print("SELF-TEST PASS")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("-")]
    if args:
        workspace = Path(args[0])
        if not workspace.is_absolute():
            workspace = (Path.cwd() / workspace).resolve()
    else:
        workspace = default_workspace(skill_root())
        if workspace is None:
            print("ERROR workspace root not given and no WORKSPACE.yaml found from skill config")
            return 2
    return check_workspace(workspace).emit()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
