#!/usr/bin/env python3
"""Lay out the GitHub Pages site (liangforstudy.github.io/mixmo/).

    /                      newest Mixmo.html on main
    /<file>.html           every other top-level page on main, by name
    /viewer/viewer.html    the history viewer (also at /viewer/)
    /viewer/index.json     the viewer's version list
    /<branch>/             newest Mixmo.html on that branch (e.g. /pooltoy/)
    /<branch>/<file>.html  every top-level page on that branch, by name

Usage (from the repo root, with all branches fetched):
    python3 viewer/build_site.py _site
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_index import MAIN, branches, git, html_files  # noqa: E402

MAIN_PAGE = ["Mixmo.html", "tripod-walk-editor.html"]


def publish(sha, folder):
    """Copy a commit's top-level pages into folder; its main page also as
    index.html. Returns the page names."""
    os.makedirs(folder, exist_ok=True)
    files = html_files(sha)
    for f in files:
        data = subprocess.run(["git", "show", f"{sha}:{f}"], check=True,
                              capture_output=True).stdout
        with open(os.path.join(folder, f), "wb") as fh:
            fh.write(data)
    main = next((f for f in MAIN_PAGE if f in files), files[0] if files else None)
    if main:
        with open(os.path.join(folder, main), "rb") as src, \
                open(os.path.join(folder, "index.html"), "wb") as dst:
            dst.write(src.read())
    return files


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "_site"
    os.makedirs(out, exist_ok=True)
    for name, tip in branches():
        folder = out if name == MAIN else os.path.join(out, name)
        files = publish(tip, folder)
        print(f"{'/' if name == MAIN else '/' + name + '/'}: {', '.join(files) or 'no pages'} ({tip[:7]})")
    here = os.path.dirname(os.path.abspath(__file__))
    vdir = os.path.join(out, "viewer")
    if os.path.exists(vdir):
        sys.exit("a branch is named 'viewer', which the history viewer's folder needs")
    os.makedirs(vdir)
    for name in ("viewer.html", "index.html"):
        with open(os.path.join(here, "viewer.html"), "rb") as src, open(os.path.join(vdir, name), "wb") as dst:
            dst.write(src.read())
    with open(os.path.join(vdir, "index.json"), "w") as fh:
        subprocess.run([sys.executable, os.path.join(here, "build_index.py")], check=True, stdout=fh)
    open(os.path.join(out, ".nojekyll"), "w").close()


if __name__ == "__main__":
    main()
