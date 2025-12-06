"""Basic tests for Document Refinery core functionality."""

import pytest
from pathlib import Path
from document_refinery.core import DocumentRefinery
from document_refinery.models.local_adapter import LocalModelAdapter


def test_document_refinery_initialization():
    """Test that DocumentRefinery can be initialized."""
    refinery = DocumentRefinery()
    assert refinery is not None
    assert refinery.config is not None


def test_add_model():
    """Test adding a model to the refinery."""
    refinery = DocumentRefinery()
    model = LocalModelAdapter({
        "model_name": "test-model",
        "model_path": "./test"
    })
    refinery.add_model("test", model)
    assert "test" in refinery.models


def test_parser_initialization():
    """Test that parser is initialized."""
    refinery = DocumentRefinery()
    assert refinery.parser is not None


def test_evaluation_harness_initialization():
    """Test that evaluation harness is initialized."""
    refinery = DocumentRefinery()
    assert refinery.harness is not None
    assert refinery.harness.red_team is not None
    assert refinery.harness.blue_team is not None
    assert refinery.harness.purple_team is not None


def test_report_generator_initialization():
    """Test that report generator is initialized."""
    refinery = DocumentRefinery()
    assert refinery.report_generator is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
