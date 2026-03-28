#!/bin/bash
# Package the olw-bootstrap skill for sharing

set -e

SKILL_NAME="olw-bootstrap"
VERSION=$(cat VERSION)
OUTPUT_DIR="./dist"
TIMESTAMP=$(date +%Y%m%d)

echo "📦 Packaging ${SKILL_NAME} v${VERSION}..."

# Create dist directory
mkdir -p "$OUTPUT_DIR"

# Create versioned archive
ARCHIVE_NAME="${SKILL_NAME}-v${VERSION}.tar.gz"
echo "Creating archive: ${ARCHIVE_NAME}"

tar -czf "${OUTPUT_DIR}/${ARCHIVE_NAME}" \
  --exclude=".git" \
  --exclude=".DS_Store" \
  --exclude="dist" \
  --exclude="test-output" \
  --exclude="*.test.hml" \
  -C .. \
  "${SKILL_NAME}"

# Create a dated archive as well
DATED_ARCHIVE="${SKILL_NAME}-v${VERSION}-${TIMESTAMP}.tar.gz"
cp "${OUTPUT_DIR}/${ARCHIVE_NAME}" "${OUTPUT_DIR}/${DATED_ARCHIVE}"

# Create zip version for Windows users
echo "Creating zip archive..."
ZIP_NAME="${SKILL_NAME}-v${VERSION}.zip"
cd ..
zip -r "${SKILL_NAME}/dist/${ZIP_NAME}" "${SKILL_NAME}" \
  -x "*.git*" \
  -x "*/.DS_Store" \
  -x "*/dist/*" \
  -x "*/test-output/*" \
  -x "*.test.hml"
cd "${SKILL_NAME}"

# Create checksums
echo "Generating checksums..."
cd "$OUTPUT_DIR"
shasum -a 256 "${ARCHIVE_NAME}" > "${ARCHIVE_NAME}.sha256"
shasum -a 256 "${ZIP_NAME}" > "${ZIP_NAME}.sha256"
cd ..

# Show results
echo ""
echo "✅ Package created successfully!"
echo ""
echo "📁 Output directory: ${OUTPUT_DIR}/"
echo ""
echo "📦 Archives created:"
ls -lh "${OUTPUT_DIR}"
echo ""
echo "🔐 Checksums:"
cat "${OUTPUT_DIR}/${ARCHIVE_NAME}.sha256"
cat "${OUTPUT_DIR}/${ZIP_NAME}.sha256"
echo ""
echo "📤 Share these files:"
echo "  - ${ARCHIVE_NAME} (for Mac/Linux)"
echo "  - ${ZIP_NAME} (for Windows)"
echo "  - Corresponding .sha256 files for verification"
echo ""
echo "🚀 Ready to share!"
