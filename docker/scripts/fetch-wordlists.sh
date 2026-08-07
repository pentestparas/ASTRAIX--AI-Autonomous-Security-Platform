#!/usr/bin/env bash
# fetch-wordlists.sh — download, dedupe, and organize wordlists + nuclei templates
# into the astraix-kali image.
#
# Sources (paths verified against GitHub tree API 2026-08):
#   https://github.com/amitlttwo/All-Wordlists        (root fuzz/dir/param lists + raft)
#   https://github.com/jeanphorn/wordlist             (passwords/ + usernames/)
#   https://github.com/trickest/wordlists             (inventory/, robots/, cloud/)
#   https://github.com/gmelodie/awesome-wordlists     (curated index of wordlists)
#   https://github.com/topics/wordlist                (discovery hub - index only)
#   https://github.com/topics/nuclei-templates        (discovery hub - index only)
#   https://github.com/projectdiscovery/nuclei-templates (canonical nuclei templates)
#
# Layout (inside the Kali image):
#   /opt/wordlists/
#     content/        directory/content busting lists (dirb, raft, dirbuster)
#     subdomains/     subdomain brute lists
#     passwords/      password lists
#     usernames/      username lists
#     params/         parameter/query fuzzing lists
#     filenames/      file/dir name lists
#     fuzz/           fuzz payload lists (fuzz.txt, params)
#     sources/        README/index files of the source repos (for provenance)
#     MANIFEST.md     what was fetched + line counts
#   /root/nuclei-templates/   nuclei templates (updated by nuclei -update-templates)
#   /usr/share/wordlists/     stock Kali tree with symlinks to our curated lists
#
# Designed to run at Docker build time (curl/sort/awk present in the base image).

set -euo pipefail

WL=/opt/wordlists
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$WL"/{content,subdomains,passwords,usernames,params,filenames,fuzz,sources}
MANIFEST="$WL/MANIFEST.md"
echo "# Wordlist + nuclei-templates manifest" > "$MANIFEST"
echo "" >> "$MANIFEST"

log() { echo "[wordlists] $*"; }

# fetch <url> <outfile> — fail hard on error (image build should fail on 404)
fetch() {
  local url="$1" out="$2"
  log "fetching $url"
  curl -fsSL --retry 3 --retry-delay 2 --connect-timeout 20 "$url" -o "$TMP/$out" 2>/dev/null \
    || { log "ERROR: failed to fetch $url"; return 1; }
}

# fetch_soft <url> <outfile> — don't fail the build on missing file
fetch_soft() {
  local url="$1" out="$2"
  log "fetching (soft) $url"
  curl -fsSL --retry 2 --retry-delay 2 --connect-timeout 15 "$url" -o "$TMP/$out" 2>/dev/null \
    && return 0 || log "  (missing, skipping) $url"; return 0
}

# dedupe <in> <out> — strip comments/blanks, sort -u
dedupe() {
  awk 'NF && $0 !~ /^#/ && $0 !~ /^[[:space:]]*$/ {print}' "$1" | sort -u -o "$2"
}

# ============================================================ AMITLT TWO / ALL-WORDLISTS
AMIT="https://raw.githubusercontent.com/amitlttwo/All-Wordlists/main"

# Directory/filename busting — raft lists live in filename-dirname-bruteforce/
RAFDIR="filename-dirname-bruteforce"
fetch_soft "${AMIT}/${RAFDIR}/raft-small-directories.txt"    a_raft_small.txt
fetch_soft "${AMIT}/${RAFDIR}/raft-medium-directories.txt"   a_raft_medium.txt
fetch_soft "${AMIT}/${RAFDIR}/raft-large-directories.txt"    a_raft_large.txt
fetch_soft "${AMIT}/${RAFDIR}/raft-small-directories-lowercase.txt" a_raft_small_lc.txt
fetch_soft "${AMIT}/dir.txt"                a_dir.txt
fetch_soft "${AMIT}/common_paths.txt"       a_common_paths.txt
fetch_soft "${AMIT}/fuzz.txt"               a_fuzz.txt
fetch_soft "${AMIT}/param.txt"              a_param.txt
fetch_soft "${AMIT}/Randomfiles.txt"        a_randomfiles.txt
fetch_soft "${AMIT}/api_seen_in_wild_paths.txt" a_api_paths.txt

for f in "$TMP"/a_raft_small.txt "$TMP"/a_raft_small_lc.txt "$TMP"/a_dir.txt "$TMP"/a_common_paths.txt; do
  if [ -s "$f" ]; then
    dedupe "$f" "${f}.d"
    cat "${f}.d" >> "$WL/content/all-dirs.txt"
  fi
done
sort -u -o "$WL/content/all-dirs.txt" "$WL/content/all-dirs.txt" 2>/dev/null || true
[ -f "$TMP/a_raft_medium.txt" ] && [ -s "$TMP/a_raft_medium.txt" ] && dedupe "$TMP/a_raft_medium.txt" "$WL/content/raft-medium-directories.txt"
[ -f "$TMP/a_raft_large.txt" ] && [ -s "$TMP/a_raft_large.txt" ] && dedupe "$TMP/a_raft_large.txt" "$WL/content/raft-large-directories.txt"
[ -f "$TMP/a_randomfiles.txt" ] && [ -s "$TMP/a_randomfiles.txt" ] && dedupe "$TMP/a_randomfiles.txt" "$WL/filenames/randomfiles.txt"

# Fuzz payloads
for f in "$TMP"/a_fuzz.txt "$TMP"/a_param.txt; do
  if [ -s "$f" ]; then
    dedupe "$f" "${f}.d"
    cat "${f}.d" >> "$WL/fuzz/all.txt"
  fi
done
sort -u -o "$WL/fuzz/all.txt" "$WL/fuzz/all.txt" 2>/dev/null || true
[ -f "$TMP/a_api_paths.txt" ] && [ -s "$TMP/a_api_paths.txt" ] && dedupe "$TMP/a_api_paths.txt" "$WL/params/api-paths.txt"

# ============================================================ JEANPHORN / WORDLIST
JEAN="https://raw.githubusercontent.com/jeanphorn/wordlist/master"
fetch_soft "${JEAN}/passwords/common.txt"        j_pw_common.txt
fetch_soft "${JEAN}/passwords/common_small.txt"  j_pw_small.txt
fetch_soft "${JEAN}/passwords/web.txt"           j_pw_web.txt
fetch_soft "${JEAN}/passwords/ssh.txt"           j_pw_ssh.txt
fetch_soft "${JEAN}/usernames/common.txt"        j_user_common.txt
fetch_soft "${JEAN}/usernames/admin.txt"         j_user_admin.txt

for f in "$TMP"/j_pw_common.txt "$TMP"/j_pw_small.txt "$TMP"/j_pw_web.txt "$TMP"/j_pw_ssh.txt; do
  if [ -s "$f" ]; then
    dedupe "$f" "${f}.d"
    cat "${f}.d" >> "$WL/passwords/jeanphorn.txt"
  fi
done
sort -u -o "$WL/passwords/jeanphorn.txt" "$WL/passwords/jeanphorn.txt" 2>/dev/null || true

for f in "$TMP"/j_user_common.txt "$TMP"/j_user_admin.txt; do
  if [ -s "$f" ]; then
    dedupe "$f" "${f}.d"
    cat "${f}.d" >> "$WL/usernames/jeanphorn.txt"
  fi
done
sort -u -o "$WL/usernames/jeanphorn.txt" "$WL/usernames/jeanphorn.txt" 2>/dev/null || true

# ============================================================ TRICKEST / WORDLISTS
TRICK="https://raw.githubusercontent.com/trickest/wordlists/main"
fetch_soft "${TRICK}/inventory/subdomains.txt"   t_sub_inv.txt
fetch_soft "${TRICK}/inventory/parameters.txt"   t_param_inv.txt
fetch_soft "${TRICK}/inventory/levels/level1.txt"    t_level1.txt
fetch_soft "${TRICK}/robots/top-1000.txt"        t_robots.txt

for f in "$TMP"/t_sub_inv.txt "$TMP"/t_level1.txt; do
  if [ -s "$f" ]; then
    dedupe "$f" "${f}.d"
    cat "${f}.d" >> "$WL/subdomains/all.txt"
  fi
done
sort -u -o "$WL/subdomains/all.txt" "$WL/subdomains/all.txt" 2>/dev/null || true

if [ -s "$TMP/t_param_inv.txt" ]; then
  dedupe "$TMP/t_param_inv.txt" "$WL/params/trickest-params.txt"
fi
if [ -s "$TMP/t_robots.txt" ]; then
  dedupe "$TMP/t_robots.txt" "$WL/fuzz/robots-top1000.txt"
fi

# ============================================================ ROCKYOU (from Kali package, avoids giant downloads)
# Kali ships /usr/share/wordlists/rockyou.txt.gz via wordlists package; the
# dirb package pulls in /usr/share/wordlists/dirb/*. Prefer those over the
# ~100MB trickest download.
if [ -f /usr/share/wordlists/rockyou.txt.gz ]; then
  log "unpacking stock rockyou.txt.gz"
  zcat /usr/share/wordlists/rockyou.txt.gz > "$WL/passwords/rockyou.txt" 2>/dev/null || true
  head -n 10000 "$WL/passwords/rockyou.txt" > "$WL/passwords/rockyou-top10k.txt"
fi

# ============================================================ SOURCES / provenance
fetch_soft "https://raw.githubusercontent.com/gmelodie/awesome-wordlists/master/README.md" src_awesome.md
fetch_soft "https://raw.githubusercontent.com/projectdiscovery/nuclei-templates/main/README.md" src_nuclei.md
[ -s "$TMP/src_awesome.md" ] && cp "$TMP/src_awesome.md" "$WL/sources/awesome-wordlists.md"
[ -s "$TMP/src_nuclei.md" ] && cp "$TMP/src_nuclei.md" "$WL/sources/nuclei-templates.md"

# ============================================================ NUCLEI TEMPLATES
if command -v nuclei >/dev/null 2>&1; then
  log "updating nuclei templates"
  nuclei -update-templates -silent >/dev/null 2>&1 || log "nuclei -update-templates failed (templates fall back to built-in)"
else
  log "nuclei not found - skipping template update (install nuclei first)"
fi

# ============================================================ STOCK KALI TREE
STOCK=/usr/share/wordlists
mkdir -p "$STOCK/dirb" "$STOCK/dirbuster"
ln -sfn "$WL/content/all-dirs.txt" "$STOCK/dirbuster/raft-small-directories.txt"
ln -sfn "$WL/content/all-dirs.txt" "$STOCK/dirbuster/raft-medium-directories.txt"
ln -sfn "$WL/content/raft-large-directories.txt" "$STOCK/dirbuster/raft-large-directories.txt"
ln -sfn "$WL/fuzz/all.txt" "$STOCK/dirb/common.txt"
ln -sfn "$WL/passwords/rockyou.txt" "$STOCK/rockyou.txt"
ln -sfn "$WL/subdomains/all.txt" "$STOCK/subdomains-top1mil-5000.txt"

# ============================================================ MANIFEST
{
  echo "## Fetched wordlists"
  find "$WL" -maxdepth 2 -type f -name '*.txt' -printf '%p\n' 2>/dev/null | sort \
    | while read -r f; do
        if [ -f "$f" ]; then
          lines=$(wc -l < "$f" | tr -d ' ')
          size=$(du -h "$f" | cut -f1)
          echo "- \`$f\` — $lines lines ($size)"
        fi
      done
  echo ""
  echo "## Nuclei templates"
  if [ -d /root/.local/nuclei-templates ]; then
    echo "- $(find /root/.local/nuclei-templates -name '*.yaml' | wc -l | tr -d ' ') templates"
  elif [ -d /root/nuclei-templates ]; then
    echo "- $(find /root/nuclei-templates -name '*.yaml' | wc -l | tr -d ' ') templates"
  else
    echo "- not updated at build time"
  fi
} >> "$MANIFEST"

log "done. Wordlist root: $WL"
