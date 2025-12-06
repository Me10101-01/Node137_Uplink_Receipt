"""
Document parser for ingestion pipeline.

Handles:
- File upload & parsing
- Text extraction
- Chunking and normalization
- Structured output (sections, clauses, definitions)
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import re
from dataclasses import dataclass, asdict


@dataclass
class DocumentChunk:
    """Represents a parsed chunk of a document."""
    id: str
    text: str
    chunk_type: str  # section, clause, paragraph, definition
    metadata: Dict[str, Any]
    start_char: int
    end_char: int


@dataclass
class ParsedDocument:
    """Represents a fully parsed document."""
    path: str
    title: Optional[str]
    chunks: List[DocumentChunk]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": self.path,
            "title": self.title,
            "chunks": [asdict(chunk) for chunk in self.chunks],
            "metadata": self.metadata,
        }


class DocumentParser:
    """
    Parse documents into structured chunks for analysis.
    
    Supports:
    - Text files (.txt, .md)
    - Future: PDF, DOCX, etc.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize parser with configuration.
        
        Args:
            config: Parser configuration including chunk_size, overlap, etc.
        """
        self.chunk_size = config.get("chunk_size", 512)
        self.overlap = config.get("overlap", 50)
    
    def parse(self, document_path: Path) -> ParsedDocument:
        """
        Parse a document into structured chunks.
        
        Args:
            document_path: Path to document file
            
        Returns:
            ParsedDocument with structured chunks
        """
        if not document_path.exists():
            raise FileNotFoundError(f"Document not found: {document_path}")
        
        # Read document content
        content = self._read_file(document_path)
        
        # Extract title (first line or filename)
        title = self._extract_title(content, document_path)
        
        # Parse into chunks
        chunks = self._parse_chunks(content)
        
        # Extract metadata
        metadata = self._extract_metadata(content, document_path)
        
        return ParsedDocument(
            path=str(document_path),
            title=title,
            chunks=chunks,
            metadata=metadata,
        )
    
    def _read_file(self, path: Path) -> str:
        """Read file content based on extension."""
        suffix = path.suffix.lower()
        
        if suffix in ['.txt', '.md']:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(
                f"Unsupported file type: {suffix}. "
                f"Supported types: .txt, .md"
            )
    
    def _extract_title(self, content: str, path: Path) -> Optional[str]:
        """Extract document title from content or filename."""
        lines = content.split('\n')
        
        # Try to find markdown header
        for line in lines[:10]:
            if line.startswith('#'):
                return line.lstrip('#').strip()
        
        # Try to find a title-like first line
        if lines and len(lines[0]) < 100:
            return lines[0].strip()
        
        # Fall back to filename
        return path.stem
    
    def _extract_metadata(self, content: str, path: Path) -> Dict[str, Any]:
        """Extract metadata from document."""
        return {
            "file_type": path.suffix,
            "file_size": len(content),
            "char_count": len(content),
            "word_count": len(content.split()),
            "line_count": len(content.split('\n')),
        }
    
    def _parse_chunks(self, content: str) -> List[DocumentChunk]:
        """
        Parse content into logical chunks.
        
        Strategy:
        1. Identify sections (headers, numbered items)
        2. Identify clauses (legal structure)
        3. Identify definitions
        4. Fall back to fixed-size chunking with overlap
        """
        chunks = []
        
        # Try section-based chunking first
        section_chunks = self._parse_sections(content)
        if section_chunks:
            chunks.extend(section_chunks)
        else:
            # Fall back to sliding window chunking
            chunks.extend(self._parse_sliding_window(content))
        
        return chunks
    
    def _parse_sections(self, content: str) -> List[DocumentChunk]:
        """Parse document into sections based on headers."""
        chunks = []
        lines = content.split('\n')
        current_section = []
        section_start = 0
        section_id = 0
        
        for i, line in enumerate(lines):
            # Detect section headers (markdown or numbered)
            is_header = (
                line.startswith('#') or
                re.match(r'^\d+\.', line.strip()) or
                re.match(r'^[A-Z][^a-z]{10,}', line.strip())  # ALL CAPS headers
            )
            
            if is_header and current_section:
                # Save previous section
                section_text = '\n'.join(current_section)
                chunks.append(DocumentChunk(
                    id=f"section_{section_id}",
                    text=section_text,
                    chunk_type="section",
                    metadata={"line_start": section_start, "line_end": i - 1},
                    start_char=section_start,
                    end_char=sum(len(l) for l in current_section),
                ))
                section_id += 1
                current_section = []
                section_start = i
            
            current_section.append(line)
        
        # Add final section
        if current_section:
            section_text = '\n'.join(current_section)
            chunks.append(DocumentChunk(
                id=f"section_{section_id}",
                text=section_text,
                chunk_type="section",
                metadata={"line_start": section_start, "line_end": len(lines) - 1},
                start_char=section_start,
                end_char=sum(len(l) for l in current_section),
            ))
        
        return chunks
    
    def _parse_sliding_window(self, content: str) -> List[DocumentChunk]:
        """Parse using sliding window with overlap."""
        chunks = []
        words = content.split()
        chunk_id = 0
        
        i = 0
        while i < len(words):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            chunks.append(DocumentChunk(
                id=f"chunk_{chunk_id}",
                text=chunk_text,
                chunk_type="paragraph",
                metadata={"word_start": i, "word_end": i + len(chunk_words)},
                start_char=i,
                end_char=i + len(chunk_text),
            ))
            
            chunk_id += 1
            i += self.chunk_size - self.overlap
        
        return chunks
