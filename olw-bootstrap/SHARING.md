# Sharing the OLW Bootstrap Skill

## Overview

There are several ways to share your olw-bootstrap skill with others, from simple file copying to publishing in a package repository.

## Option 1: Direct File Sharing (Simplest)

### Via Archive
Create a zip/tar archive and share it:

```bash
# Create a zip archive
cd ~/.claude/skills/
zip -r olw-bootstrap.zip olw-bootstrap/

# Or create a tar.gz
tar -czf olw-bootstrap.tar.gz olw-bootstrap/

# Share the archive file
# Recipients extract to their ~/.claude/skills/ directory
```

**Recipients install by:**
```bash
cd ~/.claude/skills/
unzip olw-bootstrap.zip
# or
tar -xzf olw-bootstrap.tar.gz
```

### Via Cloud Storage
Upload the archive to:
- Google Drive / Dropbox / OneDrive
- GitHub Release attachments
- Company shared drive
- Email attachment (if small enough)

## Option 2: Git Repository (Recommended)

### Create a Git Repository

```bash
cd ~/.claude/skills/olw-bootstrap/

# Initialize git (if not already)
git init

# Create a comprehensive .gitignore if needed
cat > .gitignore << 'EOF'
# Test outputs
test-output/
*.test.hml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# Add all files
git add .

# Create initial commit
git commit -m "Initial release of olw-bootstrap skill v1.0.0

- Automatic concept extraction from domain context
- WikiPage v1 YAML generation
- Cross-linking with wiki:// protocol
- Comprehensive documentation
- 5 example domains
"
```

### Push to GitHub

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill.git
git branch -M main
git push -u origin main
```

**Others install by:**
```bash
cd ~/.claude/skills/
git clone https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill.git olw-bootstrap
```

### Repository Best Practices

Create these additional files in your repo:

**LICENSE** - Choose a license (MIT recommended):
```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

**CONTRIBUTING.md** - Guide for contributors:
```markdown
# Contributing to OLW Bootstrap

## How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Code of Conduct
Be respectful, collaborative, and constructive.
```

## Option 3: Claude Code Skill Marketplace (Future)

While there isn't an official marketplace yet, you can prepare for one:

### Create a manifest.json
```json
{
  "name": "olw-bootstrap",
  "version": "1.0.0",
  "author": "Your Name",
  "license": "MIT",
  "repository": "https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill",
  "description": "Generate comprehensive Operational Language Wiki systems from domain knowledge",
  "keywords": ["wiki", "documentation", "knowledge-management", "domain-modeling"],
  "category": "Documentation",
  "homepage": "https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill",
  "bugs": "https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill/issues",
  "requirements": {
    "claude_code_version": ">=1.0.0"
  },
  "install": {
    "method": "git",
    "url": "https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill.git"
  }
}
```

## Option 4: Package Manager (Advanced)

### Create an npm package (if applicable)

```bash
cd ~/.claude/skills/olw-bootstrap/

# Create package.json
cat > package.json << 'EOF'
{
  "name": "@your-org/claude-olw-bootstrap-skill",
  "version": "1.0.0",
  "description": "Generate comprehensive Operational Language Wiki systems",
  "main": "skill.json",
  "scripts": {
    "install": "echo 'Installing olw-bootstrap skill...'",
    "test": "bash TEST.md"
  },
  "keywords": ["claude", "skill", "wiki", "documentation"],
  "author": "Your Name",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill.git"
  }
}
EOF

# Publish to npm (requires npm account)
npm publish --access public
```

**Others install by:**
```bash
cd ~/.claude/skills/
npm install @your-org/claude-olw-bootstrap-skill
mv node_modules/@your-org/claude-olw-bootstrap-skill olw-bootstrap
```

## Option 5: Company Internal Sharing

### Internal Git Server
```bash
# GitLab, Bitbucket, Azure DevOps, etc.
git remote add origin https://your-company-git.com/skills/olw-bootstrap.git
git push -u origin main
```

### Shared Network Drive
```bash
# Copy to shared location
cp -r ~/.claude/skills/olw-bootstrap/ /Volumes/SharedDrive/claude-skills/

# Others copy from shared location
cp -r /Volumes/SharedDrive/claude-skills/olw-bootstrap ~/.claude/skills/
```

### Internal Package Registry
Use Artifactory, Nexus, or similar for your organization.

## Option 6: Documentation Site

Create a dedicated documentation site using:

### GitHub Pages
```bash
# In your repository
mkdir docs
cd docs

# Create index.html or use Jekyll/MkDocs
# Enable GitHub Pages in repository settings
```

### Read the Docs
```bash
# Create docs/conf.py for Sphinx
# Connect repository to readthedocs.org
```

## Installation Instructions for Recipients

### Standard Installation

Create an `INSTALL.md` file:

```markdown
# Installing OLW Bootstrap Skill

## Prerequisites
- Claude Code installed
- `~/.claude/skills/` directory exists

## Method 1: From Git Repository
\`\`\`bash
cd ~/.claude/skills/
git clone https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill.git olw-bootstrap
\`\`\`

## Method 2: From Archive
\`\`\`bash
cd ~/.claude/skills/
unzip olw-bootstrap.zip
# or
tar -xzf olw-bootstrap.tar.gz
\`\`\`

## Method 3: Manual Installation
1. Download all files
2. Create directory: `mkdir -p ~/.claude/skills/olw-bootstrap`
3. Copy all files to that directory

## Verification
\`\`\`bash
ls ~/.claude/skills/olw-bootstrap/
# Should show: skill.md, prompt.md, skill.json, README.md, etc.
\`\`\`

## Quick Test
In Claude Code:
\`\`\`
Use the olw-bootstrap skill to create a test wiki for a simple task tracker.
Output to: /tmp/test-wiki/
\`\`\`

## Troubleshooting
- Ensure all files are in `~/.claude/skills/olw-bootstrap/`
- Check file permissions: `chmod -R 755 ~/.claude/skills/olw-bootstrap/`
- Restart Claude Code if skill doesn't appear
\`\`\`
```

## Sharing Best Practices

### 1. Include Documentation
Ensure these files are included:
- [x] README.md
- [x] EXAMPLES.md
- [x] QUICK_REFERENCE.md
- [x] CHANGELOG.md
- [x] LICENSE (add this)
- [x] INSTALL.md (create this)

### 2. Version Clearly
- Use semantic versioning (1.0.0)
- Update VERSION file with each release
- Tag releases in git: `git tag v1.0.0`

### 3. Provide Examples
- Include multiple domain examples
- Show before/after results
- Provide test cases

### 4. Make it Discoverable
- Use clear, descriptive names
- Add relevant keywords/tags
- Include screenshots or demos
- Write a blog post or announcement

### 5. Maintain It
- Respond to issues and questions
- Accept pull requests
- Update for new Claude Code versions
- Document breaking changes

## Promoting Your Skill

### Channels
- Claude Code community forums
- GitHub discussions
- Reddit (r/ClaudeAI, r/ChatGPTCoding)
- Twitter/X with #ClaudeCode hashtag
- Dev.to or Medium blog posts
- Company internal channels
- LinkedIn posts

### Announcement Template
```markdown
🚀 New Claude Code Skill: OLW Bootstrap

Automatically generate comprehensive wiki systems from domain knowledge!

✨ Features:
- 15-25 interconnected pages per domain
- Automatic cross-linking
- Semantic search support
- WikiPage v1 compliant

📦 Install:
git clone https://github.com/YOUR_USERNAME/claude-olw-bootstrap-skill.git

📖 Docs: [link to README]
💡 Examples: Banking, E-commerce, Healthcare, SaaS

#ClaudeCode #Documentation #KnowledgeManagement
```

## License Considerations

### Recommended: MIT License
```
MIT License - Permissive, allows commercial use

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

### Alternative: Apache 2.0
More explicit patent protection, still permissive.

### For Internal Use Only
```
INTERNAL USE ONLY LICENSE

Copyright (c) 2025 [Company Name]

This software is proprietary and confidential.
Unauthorized copying, distribution, or use is strictly prohibited.
```

## Support

### Provide Support Channels
- GitHub Issues (for bug reports)
- GitHub Discussions (for questions)
- Email (for private inquiries)
- Slack/Discord (for community)

### Support Template (issues)
```markdown
**Describe the issue**
A clear description of what's wrong.

**Domain Context**
What domain were you trying to document?

**Expected Output**
What pages/content you expected.

**Actual Output**
What actually happened.

**Environment**
- Claude Code version:
- OS:
```

## Quick Share Commands

### Create a shareable package
```bash
#!/bin/bash
# package-skill.sh

SKILL_NAME="olw-bootstrap"
VERSION="1.0.0"
OUTPUT="${SKILL_NAME}-v${VERSION}.tar.gz"

cd ~/.claude/skills/
tar -czf "$OUTPUT" \
  --exclude=".git" \
  --exclude="test-output" \
  --exclude=".DS_Store" \
  "$SKILL_NAME/"

echo "Created: $OUTPUT"
echo "Share this file with others!"
```

### Installation script for recipients
```bash
#!/bin/bash
# install-olw-bootstrap.sh

SKILL_ARCHIVE="olw-bootstrap-v1.0.0.tar.gz"
INSTALL_DIR="$HOME/.claude/skills"

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
tar -xzf "$SKILL_ARCHIVE"

echo "✓ OLW Bootstrap skill installed!"
echo "Location: $INSTALL_DIR/olw-bootstrap"
```

## Next Steps

1. Choose your sharing method (Git recommended)
2. Add a LICENSE file
3. Create INSTALL.md with clear instructions
4. Test the installation process
5. Announce to your target audience
6. Maintain and improve based on feedback

Good luck sharing your skill! 🚀
