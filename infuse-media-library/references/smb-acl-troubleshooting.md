# SMB/NAS ACL Troubleshooting

Most media libraries live on a NAS, mounted over SMB. SMB has permission semantics that diverge from local POSIX in ways that look like bugs but aren't. This reference catalogs the patterns.

## The headline symptom

```bash
$ ls -la "Elf (2003)/"
drwx------ 1 eric staff 16384 Nov 8 2021 .
-rwx------ 1 eric staff 8.5G Nov 8 2021 Elf.2003.1080p.BluRay.x264-CiNEFiLE.mkv

$ touch "Elf (2003)/test.txt"
touch: cannot touch 'Elf (2003)/test.txt': Permission denied
```

The POSIX bits say you own the folder and have rwx. The write rejects anyway. **Something is layered on top of POSIX** — a POSIX ACL (`getfacl`), an NFSv4 ACL, or a server-side share permission that overrides the Unix bits.

## Diagnostic checklist

Before assuming a folder is writable, run a real write probe:

```bash
# Probe top level
touch "/Volumes/data/movies/.wtest" && rm "/Volumes/data/movies/.wtest" && echo "OK top" || echo "FAIL top"

# Probe a representative subfolder
touch "Elf (2003)/.wtest" && rm "Elf (2003)/.wtest" && echo "OK sub" || echo "FAIL sub"
```

In a script:

```python
def writable(path: str) -> bool:
    test = os.path.join(path, f".wtest-{os.getpid()}")
    try:
        with open(test, "w") as f:
            f.write("test")
        os.unlink(test)
        return True
    except (OSError, PermissionError):
        return False
```

If the probe fails, you need to fix the NAS-side permissions before running any mutation script.

## SMB-specific gotchas

**1. Directory moves across folder boundaries often fail.** Renaming a file across folders works. Renaming a *directory* across folders frequently returns `Permission denied`, even when both source and destination are writable. The reason: SMB implements cross-folder directory rename as a server-side copy+delete, which the server may refuse on protected directories. Workaround: `cp -R` to copy, then explicitly delete the source. Verify the copy first.

**2. Renaming a directory within the same parent works.** `mv .trickplay-folder new-name.trickplay` succeeds. `mv new-name.trickplay subdir/` may fail. Use this pattern: rename in place first, then move.

**3. `ls` shows the wrong owner/group.** SMB maps server-side users to your local UID/GID. A folder created on the NAS as `nobody:users` may show as `eric:staff` after mounting. The POSIX bits are usually still meaningful, but ownership is a translation, not ground truth.

**4. Extended attributes show as `@` in `ls -la`.** A trailing `@` after the permission string (`drwx------@`) means macOS extended attributes are set. Often harmless but can occasionally interfere with rename ops. Clear with `xattr -cr <path>` if suspect.

**5. macOS caches SMB metadata.** After fixing permissions server-side, the Mac may still report the old perms until you unmount and remount. `sudo umount -f /Volumes/data` then reconnect via Finder (`Cmd+K → smb://user@nas/share`) or `open smb://user@nas/share`.

## Server-side fixes by NAS

### Unraid

Standard recipe — works for 95% of Unraid permission issues:

```bash
# SSH into Unraid or use Tools → Web Terminal
chown -R nobody:users /mnt/user/<share>/
chmod -R u+rwX,g+rwX,o+rwX /mnt/user/<share>/

# Strip lingering POSIX ACLs (the layer that overrides the Unix bits)
setfacl -R -b /mnt/user/<share>/

# Verify
ls -la /mnt/user/<share>/ | head
getfacl /mnt/user/<share>/ | head   # should show only default user/group/other
```

You can also do **Tools → New Permissions** in the GUI — same effect, slower because it crawls every file.

Common Unraid auth gotcha: the SMB user you connect as on the Mac (e.g. `admin@nas`) must match a user listed in the share's "Write list" under **Shares → <share> → SMB Security Settings**. If you connect as a read-only user, no amount of chmod on the server helps.

### Synology DSM

1. **DSM GUI**: Control Panel → Shared Folder → Edit → Permissions tab → set Read/Write for your user. Then Advanced → Apply to subfolders/files → "Replace all existing permissions" (this is the recursive bit; off by default).
2. **SSH** (DSM 7+):
   ```bash
   sudo chown -R <user>:users /volume1/<share>/
   sudo chmod -R u+rwX,g+rwX /volume1/<share>/
   sudo synoacltool -enforce-inherit /volume1/<share>/
   ```

### QNAP QTS

1. **GUI**: File Station → right-click share → Properties → Permission → set RW for user → check "Apply changes to existing files and folders."
2. **SSH**:
   ```bash
   chown -R <user>:everyone /share/<share>/
   chmod -R u+rwX,g+rwX /share/<share>/
   ```

### TrueNAS / FreeNAS

1. **GUI**: Storage → Pools → expand dataset → ⋮ menu → Edit Permissions → set user/group/perms → check **Apply permissions recursively** → Save.
2. **CLI** (TrueNAS Scale):
   ```bash
   chown -R <user>:<group> /mnt/<pool>/<dataset>/
   chmod -R 775 /mnt/<pool>/<dataset>/
   ```
   For datasets using NFSv4 ACLs (default on TrueNAS Core), use `setfacl` with the TrueNAS ACL spec rather than chmod.

## Side effects of bulk permission changes

A `chmod -R` or `chown -R` over millions of files can:

- **Take a long time.** Several minutes for a TB-scale library is normal.
- **Trigger reindexing.** Plex/Jellyfin/Sonarr may re-scan the whole library after permission changes if they detect mtime changes.
- **Break other consumers.** If Sonarr/Radarr/Bazarr run as a specific user, make sure that user retains access. Setting `o+w` (world-writable) is the brute-force fix but is a security loss on a NAS that's shared.

Always tell the user what you're about to recommend before they run a recursive chmod/chown — they may have an automation pipeline depending on current perms.

## When to suspect ACLs are the cause

- A folder shows the right POSIX bits but rejects writes anyway.
- Some folders in the same share work; others don't, with no apparent rhyme.
- Folders created by media-server apps (Infuse, Plex, Sonarr) seem stricter than folders you created yourself.
- `getfacl <path>` returns extra `user:`/`group:` lines beyond the default three (`user::`, `group::`, `other::`).

Whenever you see these patterns, `setfacl -R -b <path>` on the server clears the ACL layer and lets the POSIX bits take effect.
