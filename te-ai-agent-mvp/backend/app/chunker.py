from pathlib import Path
from typing import Any


DEFAULT_MAX_CHARS = 1800
DEFAULT_OVERLAP_CHARS = 250


def split_markdown_sections(content: str) -> list[dict[str, str]]:
    """
    Split Markdown into logical sections using headings.

    Each section contains:
    - heading: the most recent Markdown heading
    - content: the text belonging to that heading
    """
    sections: list[dict[str, str]] = []

    current_heading = "Introduction"
    current_lines: list[str] = []
    in_code_block = False

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            current_lines.append(line)
            continue

        if not in_code_block and stripped.startswith("#"):
            if current_lines:
                section_content = "\n".join(current_lines).strip()
                if section_content:
                    sections.append(
                        {
                            "heading": current_heading,
                            "content": section_content,
                        }
                    )

            current_heading = stripped.lstrip("#").strip() or "Untitled Section"
            current_lines = []
            continue

        current_lines.append(line)

    if current_lines:
        section_content = "\n".join(current_lines).strip()
        if section_content:
            sections.append(
                {
                    "heading": current_heading,
                    "content": section_content,
                }
            )

    return sections


def split_into_units(content: str) -> list[str]:
    """
    Split section content into paragraph-like units while preserving
    fenced Markdown code blocks as complete units.
    """
    units: list[str] = []
    current_lines: list[str] = []
    in_code_block = False

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            current_lines.append(line)

            if not in_code_block:
                unit = "\n".join(current_lines).strip()
                if unit:
                    units.append(unit)
                current_lines = []

            continue

        if in_code_block:
            current_lines.append(line)
            continue

        if stripped == "":
            unit = "\n".join(current_lines).strip()
            if unit:
                units.append(unit)
            current_lines = []
            continue

        current_lines.append(line)

    if current_lines:
        unit = "\n".join(current_lines).strip()
        if unit:
            units.append(unit)

    return units


def split_long_unit(text: str, max_chars: int) -> list[str]:
    """
    Split a single oversized paragraph or code block into smaller pieces.

    This is a fallback for units that exceed max_chars.
    """
    if len(text) <= max_chars:
        return [text]

    pieces: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + max_chars, len(text))

        if end < len(text):
            preferred_break = text.rfind("\n", start, end)

            if preferred_break <= start:
                preferred_break = text.rfind(" ", start, end)

            if preferred_break > start:
                end = preferred_break

        piece = text[start:end].strip()

        if piece:
            pieces.append(piece)

        if end <= start:
            end = start + max_chars

        start = end

    return pieces


def build_overlap(previous_text: str, overlap_chars: int) -> str:
    """
    Return the trailing portion of the previous chunk for context overlap.
    """
    if not previous_text or overlap_chars <= 0:
        return ""

    overlap = previous_text[-overlap_chars:]

    first_newline = overlap.find("\n")
    if first_newline != -1 and first_newline < len(overlap) // 2:
        overlap = overlap[first_newline + 1 :]

    return overlap.strip()


def chunk_section(
    section_content: str,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap_chars: int = DEFAULT_OVERLAP_CHARS,
) -> list[str]:
    """
    Convert one Markdown section into size-controlled chunks.
    """
    units = split_into_units(section_content)

    chunks: list[str] = []
    current_units: list[str] = []

    for original_unit in units:
        for unit in split_long_unit(original_unit, max_chars):
            candidate_units = current_units + [unit]
            candidate = "\n\n".join(candidate_units).strip()

            if current_units and len(candidate) > max_chars:
                completed_chunk = "\n\n".join(current_units).strip()

                if completed_chunk:
                    chunks.append(completed_chunk)

                overlap = build_overlap(completed_chunk, overlap_chars)
                current_units = [overlap, unit] if overlap else [unit]
            else:
                current_units.append(unit)

    if current_units:
        completed_chunk = "\n\n".join(current_units).strip()

        if completed_chunk:
            chunks.append(completed_chunk)

    return chunks


def chunk_markdown(
    content: str,
    source: str = "unknown",
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap_chars: int = DEFAULT_OVERLAP_CHARS,
) -> list[dict[str, Any]]:
    """
    Convert a Markdown document into metadata-rich chunks.
    """
    if max_chars <= 0:
        raise ValueError("max_chars must be greater than zero")

    if overlap_chars < 0:
        raise ValueError("overlap_chars cannot be negative")

    if overlap_chars >= max_chars:
        raise ValueError("overlap_chars must be smaller than max_chars")

    sections = split_markdown_sections(content)
    chunks: list[dict[str, Any]] = []
    chunk_number = 1

    document_title = Path(source).stem.replace("_", " ").title()

    for section in sections:
        section_chunks = chunk_section(
            section_content=section["content"],
            max_chars=max_chars,
            overlap_chars=overlap_chars,
        )

        for section_chunk_number, chunk_content in enumerate(
            section_chunks,
            start=1,
        ):
            chunks.append(
                {
                    "chunk_id": f"{Path(source).stem}-{chunk_number}",
                    "source": source,
                    "document_title": document_title,
                    "heading": section["heading"],
                    "section_chunk_number": section_chunk_number,
                    "content": chunk_content,
                    "character_count": len(chunk_content),
                }
            )
            chunk_number += 1

    return chunks


def chunk_document(
    path: Path,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap_chars: int = DEFAULT_OVERLAP_CHARS,
) -> list[dict[str, Any]]:
    """
    Read and chunk one Markdown document.
    """
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    if not path.is_file():
        raise ValueError(f"Expected a file, received: {path}")

    content = path.read_text(encoding="utf-8")

    return chunk_markdown(
        content=content,
        source=path.name,
        max_chars=max_chars,
        overlap_chars=overlap_chars,
    )


def chunk_directory(
    directory: Path,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap_chars: int = DEFAULT_OVERLAP_CHARS,
) -> list[dict[str, Any]]:
    """
    Chunk every Markdown file in a directory.
    """
    if not directory.exists():
        raise FileNotFoundError(f"Documentation directory not found: {directory}")

    all_chunks: list[dict[str, Any]] = []

    for path in sorted(directory.glob("*.md")):
        all_chunks.extend(
            chunk_document(
                path=path,
                max_chars=max_chars,
                overlap_chars=overlap_chars,
            )
        )

    return all_chunks