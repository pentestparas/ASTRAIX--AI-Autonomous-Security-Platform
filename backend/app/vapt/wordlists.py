"""Wordlist resolver — curated wordlists baked into the astraix-kali image.

Lists are fetched at Docker build time by `docker/scripts/fetch-wordlists.sh`
from:
  - https://github.com/amitlttwo/All-Wordlists    (raft dirs, dir, fuzz, params)
  - https://github.com/jeanphorn/wordlist         (passwords/ + usernames/)
  - https://github.com/trickest/wordlists         (inventory/, robots/, cloud/)
  - https://github.com/gmelodie/awesome-wordlists (index of curated lists)
  - https://github.com/topics/wordlist            (discovery hub)
  - https://github.com/projectdiscovery/nuclei-templates (nuclei templates)

Layout inside the Kali container:
  /opt/wordlists/
    content/      all-dirs.txt, raft-medium-directories.txt, raft-large-directories.txt
    subdomains/   all.txt
    passwords/    rockyou.txt, rockyou-top10k.txt, jeanphorn.txt
    usernames/    jeanphorn.txt
    params/       api-paths.txt, trickest-params.txt
    filenames/    randomfiles.txt
    fuzz/         all.txt, robots-top1000.txt
    sources/      provenance READMEs

IMPORTANT: command strings built here are executed INSIDE the astraix-kali
container. Paths are therefore resolved against the Kali image's filesystem,
NOT the backend's. `get_wordlist()` is deterministic: it always returns the
curated path (baked at build time) and never probes the backend FS. Actual
existence is verified lazily against the image by `wordlist_health()`.
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Optional

WORDLIST_ROOT = Path("/opt/wordlists")

# purpose -> relative path under WORDLIST_ROOT (inside the Kali image)
WORDLISTS = {
    # Content / directory busting
    "dirs": "content/all-dirs.txt",
    "dirs_medium": "content/raft-medium-directories.txt",
    "dirs_large": "content/raft-large-directories.txt",
    # Subdomains
    "subdomains": "subdomains/all.txt",
    # Passwords
    "rockyou": "passwords/rockyou.txt",
    "rockyou_top10k": "passwords/rockyou-top10k.txt",
    "passwords": "passwords/jeanphorn.txt",
    # Usernames
    "usernames": "usernames/jeanphorn.txt",
    # Parameters / fuzzing
    "params": "params/trickest-params.txt",
    "params_api": "params/api-paths.txt",
    "fuzz": "fuzz/all.txt",
    # Filenames
    "filenames": "filenames/randomfiles.txt",
    # Robots
    "robots": "fuzz/robots-top1000.txt",
}


def get_wordlist(purpose: str) -> str:
    """Return the path to the wordlist for the given purpose.

    Deterministic: always the curated /opt/wordlists path inside the Kali
    container (these are baked at image build time). No backend-FS probing —
    the returned string is only ever consumed by tools running in the image.
    """
    if purpose not in WORDLISTS:
        raise KeyError(f"unknown wordlist purpose: {purpose}")
    return str(WORDLIST_ROOT / WORDLISTS[purpose])


# --------------------------------------------------------------------------
# Health verification against the actual Kali image (cached).
# --------------------------------------------------------------------------

_KALI_IMAGE = "astraix-kali:latest"
_CACHE_TTL = 300  # seconds
_health_cache: dict = {"at": 0.0, "data": None}


def _probe_image() -> Optional[dict]:
    """Run one `wc -l` over every curated list inside the Kali image."""
    now = time.time()
    if _health_cache["data"] is not None and (now - _health_cache["at"]) < _CACHE_TTL:
        return _health_cache["data"]

    if not WORDLISTS:
        return {}
    find_expr = " ".join(f"-o -name {Path(p).name}" for p in WORDLISTS.values())[4:]
    cmd = (
        f"find /opt/wordlists -maxdepth 2 -type f -name '*.txt' -exec sh -c "
        f"'l=$(wc -l < \"$1\" | tr -d \" \"); echo \"$1 $l\"' _ {{}} \\;"
    )
    data = {}
    try:
        result = subprocess.run(
            ["docker", "run", "--rm", _KALI_IMAGE, "sh", "-c", cmd],
            capture_output=True, timeout=60, check=False,
        )
        if result.returncode == 0:
            for line in result.stdout.decode("utf-8", errors="ignore").splitlines():
                line = line.strip()
                if " " in line:
                    path, lines = line.rsplit(" ", 1)
                    data[path] = int(lines)
    except Exception:
        pass

    _health_cache.update(at=now, data=data or None)
    return data or None


def wordlist_health() -> dict:
    """Purpose -> {path, lines, present} verified inside the Kali image."""
    image_data = _probe_image() or {}
    out = {}
    for purpose, rel in WORDLISTS.items():
        path = str(WORDLIST_ROOT / rel)
        lines = image_data.get(path, 0)
        out[purpose] = {"path": path, "lines": lines, "present": lines > 0}
    return out


def list_wordlists() -> dict:
    """Alias for wordlist_health() — used by the API endpoint."""
    return wordlist_health()
