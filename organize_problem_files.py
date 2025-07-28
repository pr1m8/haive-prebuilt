#!/usr/bin/env python3
"""Organize problematic files in haive-prebuilt.

This script helps organize files that have persistent syntax errors or are
problematic for formatting/linting, moving them to appropriate archive directories.
"""

import shutil
from pathlib import Path
from typing import List, Tuple

# Files with persistent syntax/formatting errors
PROBLEM_FILES = [
    # Files that still fail Black formatting
    "src/haive/prebuilt/company_researcher/models.py",
    "src/haive/prebuilt/journalism_/models.py",
    "src/haive/prebuilt/journalism_/state.py",
    "src/haive/prebuilt/journalism_/tools.py",
    "src/haive/prebuilt/perplexity/base/engines.py",
    "src/haive/prebuilt/scientific_paper_agent/nodes.py",
    "src/haive/prebuilt/search_and_summarize/tools.py",
    "src/haive/prebuilt/startup/ideation/models.py",
    "src/haive/prebuilt/startup/pitchdeck/agent.py",
    "src/haive/prebuilt/systemic_review_of_scientific_articles/nodes.py",
    "src/haive/prebuilt/tldr2/tools.py",
    "src/haive/prebuilt/weather_disaster_management/agent.py",
]

# Archive directories to create
ARCHIVE_DIRS = [
    "archive/company_researcher",
    "archive/journalism",
    "archive/perplexity",
    "archive/scientific_paper_agent",
    "archive/search_and_summarize",
    "archive/startup",
    "archive/systemic_review",
    "archive/tldr2",
    "archive/weather_disaster",
    "archive/syntax_errors",
]


def create_archive_structure() -> None:
    """Create archive directory structure."""
    print("📁 Creating archive directory structure...")

    for archive_dir in ARCHIVE_DIRS:
        Path(archive_dir).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {archive_dir}")


def move_problem_files() -> List[Tuple[str, str]]:
    """Move problematic files to archive."""
    moved_files = []

    print("\n📦 Moving problematic files to archive...")

    for file_path in PROBLEM_FILES:
        source = Path(file_path)

        if not source.exists():
            print(f"   ⚠️  File not found: {file_path}")
            continue

        # Determine destination based on module
        if "company_researcher" in file_path:
            dest_dir = "archive/company_researcher"
        elif "journalism_" in file_path:
            dest_dir = "archive/journalism"
        elif "perplexity" in file_path:
            dest_dir = "archive/perplexity"
        elif "scientific_paper_agent" in file_path:
            dest_dir = "archive/scientific_paper_agent"
        elif "search_and_summarize" in file_path:
            dest_dir = "archive/search_and_summarize"
        elif "startup" in file_path:
            dest_dir = "archive/startup"
        elif "systemic_review" in file_path:
            dest_dir = "archive/systemic_review"
        elif "tldr2" in file_path:
            dest_dir = "archive/tldr2"
        elif "weather_disaster" in file_path:
            dest_dir = "archive/weather_disaster"
        else:
            dest_dir = "archive/syntax_errors"

        destination = Path(dest_dir) / source.name

        try:
            shutil.move(str(source), str(destination))
            moved_files.append((file_path, str(destination)))
            print(f"   ✅ Moved: {file_path} → {destination}")
        except Exception as e:
            print(f"   ❌ Failed to move {file_path}: {e}")

    return moved_files


def update_init_file() -> None:
    """Update __init__.py to remove imports for archived modules."""
    init_file = Path("src/haive/prebuilt/__init__.py")

    if not init_file.exists():
        print("   ⚠️  __init__.py not found")
        return

    print("\n📝 Updating __init__.py to remove archived module imports...")

    try:
        with open(init_file, "r") as f:
            content = f.read()

        # Create backup
        backup_file = Path("src/haive/prebuilt/__init__.py.backup")
        with open(backup_file, "w") as f:
            f.write(content)

        # Comment out problematic imports
        lines = content.split("\n")
        updated_lines = []
        changes = 0

        for line in lines:
            if any(
                module in line
                for module in [
                    "journalism_",
                    "company_researcher",
                    "tldr2",
                    "weather_disaster",
                ]
            ):
                if line.strip() and not line.strip().startswith("#"):
                    updated_lines.append(f"# ARCHIVED: {line}")
                    changes += 1
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)

        if changes > 0:
            with open(init_file, "w") as f:
                f.write("\n".join(updated_lines))
            print(
                f"   ✅ Updated __init__.py - commented out {changes} archived imports"
            )
        else:
            print("   ℹ️  No import changes needed in __init__.py")

    except Exception as e:
        print(f"   ❌ Failed to update __init__.py: {e}")


def create_archive_readme() -> None:
    """Create README for archive directory."""
    readme_content = """# Archive Directory - Haive Prebuilt

This directory contains prebuilt modules that were moved from the main codebase due to:

## Syntax/Formatting Issues
Files that have persistent syntax errors or cannot be formatted with Black:
- Complex legacy code that needs significant refactoring
- Files with encoding issues or malformed syntax
- Modules with incomplete implementations

## Module Categories Archived

### Company Researcher
- Models with syntax errors in dictionary/class definitions

### Journalism 
- State management and tool files with formatting issues
- Complex model definitions that need restructuring

### Perplexity Integration
- Engine files with incomplete conditional expressions

### Scientific Paper Agent
- Node files with syntax parsing issues

### Search and Summarize
- Tool files with parameter definition errors

### Startup Tools
- Agent and model files with dictionary syntax issues

### TL;DR Tools
- Tool files with complex formatting problems

### Weather Disaster Management
- Agent files with syntax errors

## Restoration Process
To restore a module from archive:

1. **Fix Syntax Errors**: Use Python AST parsing to identify and fix syntax issues
2. **Update Imports**: Ensure all imports are valid and up-to-date
3. **Format Code**: Use Black/Ruff to format the code properly  
4. **Add Tests**: Ensure proper test coverage
5. **Update __init__.py**: Add back to main module exports
6. **Documentation**: Update any documentation references

## Alternative Approach
Consider rewriting these modules from scratch using current best practices rather than trying to fix the existing syntax errors.

Generated by: organize_problem_files.py
Date: $(date)
"""

    with open("archive/README.md", "w") as f:
        f.write(readme_content)

    print("\n📝 Created archive/README.md")


def main():
    """Main organization function."""
    print("🗂️  Haive-Prebuilt File Organization Script")
    print("=" * 50)

    # Create archive structure
    create_archive_structure()

    # Move known problem files
    moved_files = move_problem_files()

    # Update __init__.py
    update_init_file()

    # Create archive README
    create_archive_readme()

    # Summary
    print("\n📊 Organization Summary:")
    print(f"   📦 Files moved to archive: {len(moved_files)}")

    if moved_files:
        print("\n✅ Successfully moved files:")
        for source, dest in moved_files:
            print(f"   {source} → {dest}")

    print("\n🎉 Organization complete!")
    print("   Now try: trunk fmt --all")
    print("   Then:    trunk check --all")


if __name__ == "__main__":
    main()
