"""Unit tests for async submission behavior in the HTTP client."""

from core.client import FluxClient


def test_with_async_callback_injects_default_callback() -> None:
    """Long-running Flux operations should default to async submission."""
    client = FluxClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback({"action": "generate"})
    assert payload["callback_url"] == "https://api.acedata.cloud/health"


def test_with_async_callback_preserves_explicit_callback() -> None:
    """User-provided callbacks should not be overwritten."""
    client = FluxClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback(
        {"action": "generate", "callback_url": "https://example.com/webhook"}
    )
    assert payload["callback_url"] == "https://example.com/webhook"
