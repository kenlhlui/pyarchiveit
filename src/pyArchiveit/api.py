"""A module for interacting with the Archive-it API."""

import logging

from .httpx_client import HTTPXClient

logger = logging.getLogger(__name__)


class ArchiveItAPI:
    """A client for interacting with the Archive-it API."""

    def __init__(
        self,
        account_name: str,
        account_password: str,
        base_url: str = "https://partner.archive-it.org/api/",
        default_timeout: float | None = 30.0,
    ) -> None:
        """Initialize the ArchiveItAPI client with authentication and base URL.

        Args:
            account_name (str): The account name for authentication.
            account_password (str): The account password for authentication.
            base_url (str): The base URL for the API endpoints. Defaults to Archive-it API base URL.
            default_timeout (float | None): Default timeout in seconds. Defaults to 30.0. Use None for no timeout.

        """
        self.http_client = HTTPXClient(
            account_name=account_name,
            account_password=account_password,
            base_url=base_url,
            default_timeout=default_timeout,
        )

    def __enter__(self) -> "ArchiveItAPI":
        """Enter context manager."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> bool:
        """Exit context manager and close the HTTP client."""
        self.close()
        return False

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self.http_client.close()

    def get_seed_list(
        self,
        collection_id: str | int | list[str | int],
        limit: int = -1,
        format: str = "json",
        timeout: float | None = None,
    ) -> list[dict]:
        """Get seeds for a given collection ID or list of collection IDs.

        Args:
            collection_id (str | int | list[str | int]): Collection ID or list of Collection IDs.
            limit (int): Maximum number of seeds to retrieve per collection. Defaults to -1 (no limit).
            format (str): The format of the response (json or xml). Defaults to "json".
            timeout (float | None): Timeout in seconds for this request. Uses client default if not specified.

        Returns:
            list[dict]: List of seeds from all requested collections.

        Raises:
            httpx.HTTPStatusError: If the API request fails.
            httpx.TimeoutException: If the request times out.

        """
        # Normalize input to a list
        collection_ids = (
            [collection_id] if isinstance(collection_id, (str, int)) else collection_id
        )

        all_seeds = []

        for coll_id in collection_ids:
            logger.info(f"Fetching seeds for collection ID: {coll_id}")
            try:
                response = self.http_client.get(
                    "seed",
                    params={"collection": coll_id, "limit": limit, "format": format},
                    timeout=timeout,
                )
                data = response.json()

                # API returns a list of seeds
                if isinstance(data, list):
                    all_seeds.extend(data)
                    logger.info(
                        f"Retrieved {len(data)} seeds for collection ID: {coll_id}"
                    )
                else:
                    logger.warning(
                        f"Unexpected response format for collection ID {coll_id}: {type(data)}"
                    )
            except Exception as e:
                logger.error(f"Failed to fetch seeds for collection ID {coll_id}: {e}")
                raise

        return all_seeds
