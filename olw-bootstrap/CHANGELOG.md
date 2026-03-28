# Changelog

All notable changes to the olw-bootstrap skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-04

### Added
- Initial release of olw-bootstrap skill
- Automatic concept extraction from domain context
- WikiPage v1 YAML generation
- Cross-linking with wiki:// protocol
- Semantic alias generation
- Structured section organization
- Support for multiple input sources (config files, docs, direct description)
- Comprehensive coverage across 8 concept categories:
  - Core entities
  - Classifications/segments
  - Products/services
  - Metrics/measurements
  - Processes/operations
  - Events/patterns
  - Strategic concepts
  - Data/transaction concepts
- Todo list integration for progress tracking
- Examples for 5 different domains (banking, e-commerce, healthcare, SaaS, supply chain)
- Comprehensive documentation (README, EXAMPLES, TEST)
- Quality validation guidelines

### Features
- Generates 15-25 interconnected wiki pages per domain
- Maintains institutional terminology consistency
- Creates bidirectional conceptual relationships
- Includes calculation examples for metrics
- Provides business context and strategic implications
- Supports hybrid input (config file + additional context)

### Documentation
- skill.md: Public skill description
- prompt.md: Detailed agent instructions (8,865 bytes)
- skill.json: Machine-readable configuration
- README.md: Comprehensive user guide (4,143 bytes)
- EXAMPLES.md: Five detailed usage examples (6,942 bytes)
- TEST.md: Testing procedures and validation
- CHANGELOG.md: Version history
- .gitignore: Exclusion patterns

### Capabilities
- Analyzes domain context and institutional knowledge
- Creates interconnected wiki page systems
- Generates WikiPage v1 YAML files
- Establishes semantic cross-linking
- Provides comprehensive domain coverage

## [1.1.0] - 2025-11-04

### Changed
- **BREAKING**: Changed output file extension from `.yaml` to `.hml` (Hasura Metadata Language)
- Updated all documentation to reference `.hml` files instead of `.yaml` files
- Updated skill capability description to "Generates WikiPage v1 HML files"
- Modified package.sh to exclude `*.test.hml` instead of `*.test.yaml`
- Updated .gitignore patterns for `.hml` test files

### Documentation
- Updated prompt.md with `.hml` file extension examples
- Updated QUICK_REFERENCE.md with `.hml` validation commands
- Updated TEST.md with `.hml` test examples
- Updated EXAMPLES.md with `.hml` references
- Updated INSTALL.md verification examples
- Updated SHARING.md .gitignore example

### Notes
- Files still use YAML syntax internally (HML is YAML-based)
- This change aligns with Hasura DDN metadata standards
- Existing workflows expecting `.yaml` files will need to be updated

## [1.2.0] - 2025-11-04

### Changed
- **BREAKING**: Updated wiki link syntax from `wiki://page-name` to `[Title](<wiki://Title>)` markdown format
- Wiki links must now use exact case-sensitive match to `WikiPage.definition.title` value
- Updated Cross-Linking Strategy section in prompt.md with new format and examples
- Updated all WikiPage structure examples to demonstrate new link format
- Updated Content Guidelines for Details and Sections to use new syntax

### Documentation
- Updated prompt.md with comprehensive examples of new link format
- Updated skill.md to clarify the new cross-linking format requirement
- Added explicit instructions about case-sensitive title matching
- Provided clear before/after examples in Cross-Linking Strategy section

### Impact
- All generated wiki pages will now use markdown-style links for better readability
- Links are more explicit and easier to identify in text
- Format aligns with standard markdown link syntax
- Improves compatibility with markdown processors and viewers

### Migration Notes
- Existing wikis using `wiki://page-name` format will need to be updated to `[Page Name](<wiki://Page Name>)`
- Title must exactly match the WikiPage definition title (case-sensitive)
- Example: `wiki://lending-rate` becomes `[Lending Rate](<wiki://Lending Rate>)`

## [1.2.1] - 2025-12-09

### Changed
- Clarified throughout documentation that output files use `.hml` extension
- Updated WikiPage v1 Specification section in skill.md to explicitly state "saved as `.hml` files"
- Enhanced Output section in skill.md with explicit `.hml` extension example
- Updated WikiPage Structure Requirements in prompt.md to clarify `.hml` file format
- Enhanced Output Format section in prompt.md with more specific `.hml` guidance

### Documentation
- Updated skill.md: Added explicit `.hml` extension references and examples
- Updated prompt.md: Clarified that YAML syntax is used within `.hml` files
- Added file naming example in Output Format: `merchant-risk-profile.hml`

### Notes
- This is a documentation clarification release; no functional changes
- Reinforces the v1.1.0 change to `.hml` file extension
- Ensures consistency across all documentation

## [Unreleased]

### Planned
- Support for custom WikiPage templates
- Automatic diagram generation (Mermaid) for concept relationships
- Wiki validation tool to check for broken links
- Multi-language support for internationalized wikis
- Version control integration for wiki page histories
- Automatic alias suggestion using LLM
- Wiki metrics dashboard (page count, link density, coverage)
- Import from existing documentation formats (Confluence, Notion, etc.)
- Export to alternative formats (Markdown, HTML, PDF)

### Future Enhancements
- Interactive wiki graph visualization
- Automated wiki maintenance and updates
- Integration with knowledge graph systems
- Support for multimedia content (images, videos)
- Collaborative editing workflows
- Wiki analytics and usage tracking
