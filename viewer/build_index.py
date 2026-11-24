#!/usr/bin/env python3
"""Build index.json for the Mixmo history viewer.

Reads every commit on every branch of this repo and writes, for each one:
its ID, parents, date, title, full message, which top-level .html files it
contains, and a "lane" (which line of the timeline it is drawn on).

Usage (from the repo root, with all branches fetched):
    python3 viewer/build_index.py > _site/index.json
"""
import json
import subprocess
import sys
from datetime import datetime, timezone

# Branch order decides lanes: main first, then the rest, newest first.
MAIN = "main"


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True,
                          text=True).stdout


def branches():
    """Branch name -> tip commit. Uses remote branches (CI checkout) and
    falls back to local ones."""
    found = {}
    for ref_prefix in ("refs/remotes/origin/", "refs/heads/"):
        out = git("for-each-ref", "--format=%(refname)%00%(objectname)", ref_prefix)
        for line in out.splitlines():
            ref, sha = line.split("\0")
            name = ref[len(ref_prefix):]
            if name == "HEAD" or name in found:
                continue
            found[name] = sha
    if not found:
        sys.exit("no branches found")
    # main first, then the other branches newest tip first
    tip_time = {n: int(git("log", "-1", "--format=%ct", sha).strip()) for n, sha in found.items()}
    order = sorted(found, key=lambda n: (n != MAIN, -tip_time[n], n))
    return [(n, found[n]) for n in order]


def read_commits(tips):
    """sha -> commit info for everything reachable from the tips."""
    sep, end = "\x1f", "\x1e"
    fmt = sep.join(["%H", "%P", "%aI", "%s", "%B"]) + end
    out = git("log", "--format=" + fmt, *tips)
    commits = {}
    for rec in out.split(end):
        rec = rec.strip("\n")
        if not rec:
            continue
        sha, parents, date, title, body = rec.split(sep, 4)
        commits[sha] = {
            "sha": sha,
            "parents": parents.split() if parents else [],
            "date": date,
            "title": title,
            "message": body.strip(),
        }
    return commits


def html_files(sha):
    """Top-level .html files in a commit (the pages the viewer can open)."""
    out = git("ls-tree", "--name-only", sha)
    return sorted(n for n in out.splitlines() if n.lower().endswith(".html"))


def assign_lanes(branch_list, commits):
    """Give each commit a lane. Each branch's first-parent line gets a lane,
    in branch order; the side line of a merge (e.g. the 11 Nov fork) gets a
    lane of its own. A commit keeps the first lane that reaches it."""
    lanes = []           # [{"name": ..., "branch": ...}]
    lane_of = {}

    def walk(start, lane):
        c = start
        while c and c not in lane_of and c in commits:
            lane_of[c] = lane
            info = commits[c]
            # side lines of merges are walked later, after this line
            for p in info["parents"][1:]:
                pending.append((p, lanes[lane]["branch"]))
            c = info["parents"][0] if info["parents"] else None

    for name, tip in branch_list:
        pending = []
        if tip not in lane_of:
            lanes.append({"name": name, "branch": name})
            walk(tip, len(lanes) - 1)
        while pending:
            p, br = pending.pop(0)
            if p in lane_of:
                continue
            lanes.append({"name": f"{br} (side line)", "branch": br})
            walk(p, len(lanes) - 1)
    return lanes, lane_of


def reachable(tip):
    return set(git("rev-list", tip).split())


def main():
    branch_list = branches()
    commits = read_commits([t for _, t in branch_list])
    lanes, lane_of = assign_lanes(branch_list, commits)
    on_branch = {name: reachable(tip) for name, tip in branch_list}

    out = []
    for c in commits.values():
        c["files"] = html_files(c["sha"])
        c["lane"] = lane_of[c["sha"]]
        c["branches"] = [n for n, _ in branch_list if c["sha"] in on_branch[n]]
        out.append(c)
    # oldest first; ties broken so a parent comes before its child
    order = {sha: i for i, sha in enumerate(
        git("rev-list", "--topo-order", "--reverse",
            *[t for _, t in branch_list]).split())}
    out.sort(key=lambda c: (datetime.fromisoformat(c["date"]).astimezone(timezone.utc),
                            order[c["sha"]]))

    json.dump({
        "repo": "liangforstudy/mixmo",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "branches": [{"name": n, "tip": t} for n, t in branch_list],
        "lanes": lanes,
        "commits": out,
    }, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
