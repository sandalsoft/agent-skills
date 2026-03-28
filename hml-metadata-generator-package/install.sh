#!/bin/bash

# HML Metadata Generator Skill - Installation Script
# This script installs the skill into Claude Code's skills directory

set -e

SKILL_NAME="hml-metadata-generator"
SKILLS_DIR="${HOME}/.claude/skills"
INSTALL_DIR="${SKILLS_DIR}/${SKILL_NAME}"

echo "🚀 Installing HML Metadata Generator Skill for Claude Code"
echo ""

# Create skills directory if it doesn't exist
if [ ! -d "${SKILLS_DIR}" ]; then
    echo "📁 Creating Claude Code skills directory..."
    mkdir -p "${SKILLS_DIR}"
fi

# Check if skill already exists
if [ -d "${INSTALL_DIR}" ]; then
    echo "⚠️  Skill already exists at ${INSTALL_DIR}"
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Installation cancelled"
        exit 1
    fi
    echo "🗑️  Removing existing installation..."
    rm -rf "${INSTALL_DIR}"
fi

# Copy skill files
echo "📦 Copying skill files..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -r "${SCRIPT_DIR}" "${INSTALL_DIR}"

# Remove the install script from the destination
rm -f "${INSTALL_DIR}/install.sh"

echo ""
echo "✅ Installation complete!"
echo ""
echo "📍 Skill installed to: ${INSTALL_DIR}"
echo ""
echo "📚 Next steps:"
echo "   1. Install Python dependencies (optional):"
echo "      pip install -r ${INSTALL_DIR}/requirements.txt"
echo ""
echo "   2. Start using the skill in Claude Code:"
echo "      claude code"
echo ""
echo "   3. Try it out with a command like:"
echo "      'Add metadata descriptions to my HML files'"
echo ""
echo "💡 Tip: Read ${INSTALL_DIR}/README.md for more usage examples"
