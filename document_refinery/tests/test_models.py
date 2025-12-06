"""Tests for model adapters."""

import pytest
from document_refinery.models.local_adapter import LocalModelAdapter
from document_refinery.models.adapter import ModelResponse


def test_local_adapter_initialization():
    """Test local adapter initialization."""
    adapter = LocalModelAdapter({
        "model_name": "test-model",
        "model_path": "./test"
    })
    assert adapter.model_name == "test-model"
    assert adapter.model_path == "./test"


def test_local_adapter_generate():
    """Test local adapter generate method."""
    adapter = LocalModelAdapter({
        "model_name": "test-model",
        "model_path": "./test"
    })
    
    response = adapter.generate("Test prompt")
    
    assert isinstance(response, ModelResponse)
    assert response.text is not None
    assert response.model_name == "test-model"
    assert response.total_tokens > 0


def test_local_adapter_batch_generate():
    """Test batch generation."""
    adapter = LocalModelAdapter({
        "model_name": "test-model",
        "model_path": "./test"
    })
    
    prompts = ["Prompt 1", "Prompt 2"]
    responses = adapter.batch_generate(prompts)
    
    assert len(responses) == 2
    assert all(isinstance(r, ModelResponse) for r in responses)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
