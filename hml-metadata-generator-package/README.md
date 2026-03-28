# HML Metadata Generator Skill Package

A skill for Claude Code that automatically generates and fills in descriptive metadata for Hasura DDN (Data Delivery Network) models, types, commands, and fields in .hml (Hasura Metadata Language) files.

## What This Skill Does

This skill helps you enhance Hasura DDN metadata files by:
- Automatically generating semantic descriptions for models, types, commands, and fields
- Improving PromptQL's understanding of your data models
- Maintaining consistency across your metadata
- Saving time on manual documentation

## Installation for Claude Code

1. **Create the skills directory** (if it doesn't exist):
   ```bash
   mkdir -p ~/.claude/skills
   ```

2. **Copy this skill package**:
   ```bash
   cp -r hml-metadata-generator-package ~/.claude/skills/hml-metadata-generator
   ```

3. **Verify installation**:
   ```bash
   ls ~/.claude/skills/hml-metadata-generator
   ```
   
   You should see:
   - `SKILL.md` - The main skill documentation
   - `scripts/` - Helper scripts
   - `references/` - Reference documentation

## Usage in Claude Code

Once installed, Claude Code will automatically have access to this skill. You can reference it in your prompts:

### Examples

**Generate metadata for a new HML file:**
```
Add comprehensive metadata descriptions to my users.hml file
```

**Update existing metadata:**
```
Review and improve the metadata in my data model HML files
```

**Batch process multiple files:**
```
Add metadata to all HML files in the ./metadata directory
```

## What's Included

### SKILL.md
The main skill documentation that Claude Code reads. Contains:
- Detailed instructions for generating metadata
- Best practices for descriptions
- Examples and patterns
- Error handling guidance

### scripts/add_metadata.py
A Python script that can:
- Parse HML files
- Generate AI-powered descriptions
- Intelligently insert metadata
- Handle various HML constructs (models, types, commands, fields)

### references/hml_structure.md
Reference documentation about HML file structure and syntax.

## Requirements

The Python script requires:
- Python 3.8+
- PyYAML (`pip install pyyaml`)
- Anthropic API access (for AI-generated descriptions)

## Tips for Best Results

1. **Be specific**: Tell Claude Code which files or directories to process
2. **Review output**: Always review generated metadata for accuracy
3. **Iterative refinement**: You can ask Claude Code to improve descriptions
4. **Context matters**: Provide context about your data model for better descriptions

## File Structure

```
hml-metadata-generator/
├── README.md                    # This file
├── SKILL.md                     # Main skill documentation
├── scripts/
│   └── add_metadata.py         # Metadata generation script
└── references/
    └── hml_structure.md        # HML structure reference
```

## Troubleshooting

**Skill not recognized:**
- Ensure the skill is in `~/.claude/skills/hml-metadata-generator`
- Check that `SKILL.md` exists and is readable

**Script errors:**
- Verify Python dependencies are installed
- Check that your HML files are valid YAML

**Poor metadata quality:**
- Provide more context about your data model
- Ask Claude Code to regenerate specific sections
- Review and refine iteratively

## Support

For issues or questions about:
- **The skill itself**: Modify the SKILL.md file or scripts as needed
- **Claude Code**: Visit https://docs.claude.com/claude-code
- **Hasura DDN**: Visit https://hasura.io/docs

## License

This skill package is provided as-is for use with Claude Code.
