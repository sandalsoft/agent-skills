# Installing OLW Bootstrap Skill

## Prerequisites

- Claude Code installed and configured
- `~/.claude/skills/` directory exists (created automatically by Claude Code)

## Installation Methods

### Method 1: From Git Repository (Recommended)

```bash
cd ~/.claude/skills/
git clone https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill.git olw-bootstrap
```

This keeps the skill updatable with `git pull`.

### Method 2: From Archive File

If you received a `.zip` or `.tar.gz` file:

```bash
cd ~/.claude/skills/

# For zip files
unzip olw-bootstrap.zip

# For tar.gz files
tar -xzf olw-bootstrap.tar.gz
```

### Method 3: Manual Installation

1. Download all skill files
2. Create the directory:
   ```bash
   mkdir -p ~/.claude/skills/olw-bootstrap
   ```
3. Copy all files into that directory

## Verify Installation

Check that all required files are present:

```bash
ls ~/.claude/skills/olw-bootstrap/
```

You should see:
- skill.md
- prompt.md
- skill.json
- README.md
- EXAMPLES.md
- TEST.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- VERSION
- LICENSE
- .gitignore

## Test the Installation

In Claude Code, try a simple test:

```
Use the olw-bootstrap skill to create a test wiki.

Domain: Simple Task Tracker
Context:
- Task statuses: Todo, In Progress, Done
- Priorities: Low, Medium, High
- Assignees: Users who work on tasks

Output to: /tmp/test-wiki/
```

This should create several wiki pages in `/tmp/test-wiki/`.

## Verify Output

Check the generated files:

```bash
ls /tmp/test-wiki/
cat /tmp/test-wiki/task-tracker.hml
```

You should see valid WikiPage YAML files with cross-links.

## Troubleshooting

### Skill Not Found

**Error**: "skill 'olw-bootstrap' not found"

**Solutions**:
1. Verify files are in `~/.claude/skills/olw-bootstrap/` (note: singular "skills")
2. Check file permissions: `chmod -R 755 ~/.claude/skills/olw-bootstrap/`
3. Restart Claude Code
4. Ensure `skill.md` and `skill.json` exist

### Permission Denied

**Error**: Permission issues when writing files

**Solution**:
```bash
chmod -R 755 ~/.claude/skills/olw-bootstrap/
```

### Invalid YAML Output

**Error**: Generated YAML files won't parse

**Solution**:
- Ensure you have the latest version
- Check your domain context for special characters
- Report the issue with your input context

### Missing Documentation

If documentation files are missing, re-download or clone the repository.

## Updating the Skill

### If Installed via Git
```bash
cd ~/.claude/skills/olw-bootstrap/
git pull origin main
```

### If Installed from Archive
Download the new archive and replace the old files:
```bash
cd ~/.claude/skills/
rm -rf olw-bootstrap/
# Then reinstall using Method 2
```

## Uninstalling

To remove the skill:

```bash
rm -rf ~/.claude/skills/olw-bootstrap/
```

## Next Steps

1. Read the [README.md](README.md) for comprehensive documentation
2. Check [EXAMPLES.md](EXAMPLES.md) for usage examples
3. See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for common patterns
4. Test with your own domain context

## Getting Help

- **Documentation**: Read README.md and EXAMPLES.md
- **Issues**: Report bugs on GitHub (if published)
- **Questions**: Check EXAMPLES.md for similar use cases

## Version

Current Version: 1.0.0

Check [CHANGELOG.md](CHANGELOG.md) for version history and updates.
