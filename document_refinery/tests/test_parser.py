"""Tests for document parser."""

import pytest
from pathlib import Path
from document_refinery.ingestion.parser import DocumentParser, ParsedDocument


def test_parser_initialization():
    """Test parser initialization."""
    parser = DocumentParser({"chunk_size": 512, "overlap": 50})
    assert parser.chunk_size == 512
    assert parser.overlap == 50


def test_parse_text_file(tmp_path):
    """Test parsing a simple text file."""
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("# Test Document\n\nThis is a test paragraph.\n\n## Section 1\n\nContent here.")
    
    parser = DocumentParser({"chunk_size": 512, "overlap": 50})
    result = parser.parse(test_file)
    
    assert isinstance(result, ParsedDocument)
    assert result.title is not None
    assert len(result.chunks) > 0
    assert result.metadata["char_count"] > 0


def test_extract_title():
    """Test title extraction."""
    parser = DocumentParser({})
    content = "# My Document Title\n\nSome content here."
    test_path = Path("test.txt")
    
    title = parser._extract_title(content, test_path)
    assert title == "My Document Title"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
