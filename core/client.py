"""HTTP client for Flux API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import FluxAPIError, FluxAuthError, FluxTimeoutError

# Force upstream async mode in MCP so tool calls return quickly with a task_id.
_ASYNC_CALLBACK_URL = "https://api.acedata.cloud/health"

# Context variable for per-request API token (used in HTTP/remote mode)
_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the API token for the current request context (HTTP mode)."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Get the API token from the current request context."""
    return _request_api_token.get()


class FluxClient:
    """Async HTTP client for AceDataCloud Flux API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the Flux API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"FluxClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise FluxAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _with_async_callback(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Ensure long-running media operations are submitted asynchronously."""
        request_payload = dict(payload)
        if not request_payload.get("callback_url"):
            request_payload["callback_url"] = _ASYNC_CALLBACK_URL
        return request_payload

    async def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Flux API.

        Args:
            endpoint: API endpoint path (e.g., "/flux/images")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary

        Raises:
            FluxAuthError: If authentication fails
            FluxAPIError: If the API request fails
            FluxTimeoutError: If the request times out
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"POST {url}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        logger.debug(f"Timeout: {request_timeout}s")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code == 401:
                    logger.error("Authentication failed: Invalid API token")
                    raise FluxAuthError("Invalid API token")

                if response.status_code == 403:
                    logger.error("Access denied: Check API permissions")
                    raise FluxAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()

                result = response.json()
                logger.success(f"Request successful! Task ID: {result.get('task_id', 'N/A')}")

                # Log summary of response
                if result.get("success"):
                    data = result.get("data", [])
                    if isinstance(data, list):
                        logger.info(f"Returned {len(data)} item(s)")
                        for i, item in enumerate(data, 1):
                            if "image_url" in item:
                                logger.info(f"  Image {i}: {item.get('image_url', 'N/A')}")
                else:
                    logger.warning(f"API returned success=false: {result.get('error', {})}")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise FluxTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except FluxAuthError:
                raise

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise FluxAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise FluxAPIError(message=str(e)) from e

    # Convenience methods for specific endpoints
    async def generate_image(self, **kwargs: Any) -> dict[str, Any]:
        """Generate image using the images endpoint."""
        logger.info(f"Generating image with action: {kwargs.get('action', 'generate')}")
        return await self.request("/flux/images", self._with_async_callback(kwargs))

    async def edit_image(self, **kwargs: Any) -> dict[str, Any]:
        """Edit image using the images endpoint with edit action."""
        logger.info(f"Editing image with model: {kwargs.get('model', 'flux-kontext-pro')}")
        return await self.request("/flux/images", self._with_async_callback(kwargs))

    async def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        task_id = kwargs.get("id") or kwargs.get("ids", [])
        logger.info(f"Querying task(s): {task_id}")
        return await self.request("/flux/tasks", kwargs)


# Global client instance
client = FluxClient()
