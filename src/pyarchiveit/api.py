"""A module for interacting with the Archive-it API."""

import logging
from typing import Any

from httpx import Response
from pydantic import ValidationError

from pyarchiveit.model_validator import ModelValidator

from .exceptions import InvalidAuthError
from .httpx_client import HTTPXClient
from .models import SeedCreate, SeedKeys, SeedUpdate

logger = logging.getLogger(__name__)


class ArchiveItAPI:
    """A client for interacting with the Archive-it API."""

    def __init__(
        self,
        account_name: str,
        account_password: str,
        base_url: str = "https://partner.archive-it.org/api/",
        default_timeout: float | None = None,
    ) -> None:
        """Initialize the ArchiveItAPI client with authentication and base URL.

        Args:
            account_name (str): The account name for authentication.
            account_password (str): The account password for authentication.
            base_url (str): The base URL for the API endpoints. Defaults to Archive-it API base URL.
            default_timeout (float | None): Default timeout in seconds. Defaults to None. Use None for no timeout.

        """
        # validate authentication upon initialization
        self.SUCCESS_STATUS_CODES = range(200, 300)
        self.httpx_client = HTTPXClient(
            base_url=base_url,
            auth=(account_name, account_password),
            follow_redirects=True,
            timeout=default_timeout,
        )
        self._validate_auth()

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
        self.httpx_client.close()

    def _request(self, method: str, endpoint: str) -> Response:
        """Make an HTTP request using the HTTPXClient. Mainly for internal/Debug use.

        Args:
            method (str): HTTP method (get, post, patch, delete, etc.)
            endpoint (str): API endpoint

        Returns:
            httpx.Response: The HTTP response

        """
        return self.httpx_client.request(method, endpoint)

    def _validate_auth(self) -> None:
        """Validate authentication credentials."""
        response = self.httpx_client.get("auth")

        if response.status_code in {401, 403}:
            msg = "Invalid authentication credentials."
            raise InvalidAuthError(msg)

        if response.json().get("id") is None:
            msg = "Authentication failed."
            raise InvalidAuthError(msg)

        logger.info("Authentication credentials are valid.")

    def get_seed_list(
        self,
        collection_id: str | int | list[str | int],
        limit: int = -1,
        sort: str | None = None,
        format: str = "json",
    ) -> list:
        r"""Get seeds for a given collection ID or list of collection IDs.

        Args:
            collection_id (str | int | list[str | int]): Collection ID or list of Collection IDs.
            limit (int): Maximum number of seeds to retrieve per collection. Defaults to -1 (no limit).
            sort (str | None): Sort order based on the result. Negative values (-) indicate ascending order. Defaults to None.<br><br>See the available fields in the API documentation (Data Models > Seed).<br><br>Example values: "id", "-id", "last_updated_date", "-last_updated_date".
            format (str): The format of the response (json or xml). Defaults to "json".

        Returns:
            list[SeedKeys]: List of validated seed objects from all requested collections.

        Raises:
            httpx.HTTPStatusError: If the API request fails.
            httpx.TimeoutException: If the request times out.
            ValidationError: If the API returns invalid seed data.
            ValueError: If the `sort` parameter is invalid.

        """
        # Pydantic validate sort parameter is a valid field
        if sort:
            sort_field = sort.lstrip("-")
            if sort_field not in SeedKeys.model_fields:
                msg = f"Invalid sort field: {sort_field}. Must be one of: {list(SeedKeys.model_fields.keys())}"
                logger.error(msg)
                raise ValueError(msg)

        # Normalize input to a list
        collection_ids = (
            [collection_id] if isinstance(collection_id, (str, int)) else collection_id
        )

        all_seeds = []

        for coll_id in collection_ids:
            logger.info(f"Fetching seeds for collection ID: {coll_id}")
            response = self.httpx_client.get(
                "seed",
                params={
                    "collection": coll_id,
                    "limit": limit,
                    "format": format,
                    "sort": sort,
                },
            )

            data = response.json()

            # API returns a list of seeds
            if isinstance(data, list):
                # Validate each seed using Pydantic
                validated_seeds: list[dict[str, Any]] = [
                    ModelValidator.validate(
                        SeedKeys, seed, f"collection {coll_id}"
                    ).model_dump()
                    for seed in data
                ]
                all_seeds.extend(validated_seeds)
                logger.info(f"Retrieved {len(data)} seeds for collection ID: {coll_id}")
            else:
                logger.warning(
                    f"Unexpected response format for collection ID {coll_id}: {type(data)}"
                )
        return ModelValidator.validate_list(
            SeedKeys, all_seeds, "all seeds", source="api"
        )

    def update_seed_metadata(
        self,
        seed_id: str | int,
        metadata: dict,
    ) -> dict:
        """Update metadata for a specific seed.

        Args:
            seed_id (str | int): The ID of the seed to update.
            metadata (dict): The metadata to update for the seed.

        Raises:
            ValidationError: If the metadata structure is invalid.

        """
        logger.info(f"Updating metadata for seed ID: {seed_id}")

        # Validate metadata structure using Pydantic
        try:
            seed_update = SeedUpdate(metadata=metadata)
        except ValidationError as e:
            logger.error(f"Invalid metadata structure for seed ID {seed_id}: {e}")
            raise

        response = self.httpx_client.patch(
            f"seed/{seed_id}",
            data=seed_update.model_dump(exclude_none=True, mode="python"),
        )

        return response.json()

    def create_seed(
        self,
        url: str,
        collection_id: str | int,
        crawl_definition_id: str | int,
        other_params: dict | None = None,
        metadata: dict | None = None,
    ) -> dict:
        """Create a new seed in a specified collection with given crawl definition.

        Args:
            url (str): The URL of the seed to create.
            collection_id (str | int): The ID of the collection to add the seed to.
            crawl_definition_id (str | int): The ID of the crawl definition to associate with the seed.
            other_params (dict | None): Additional parameters for the seed creation.
            metadata (dict | None): Metadata to set for the seed after creation.

        Returns:
            dict: The validated created seed data returned by the API.

        Raises:
            ValidationError: If the input data or metadata structure is invalid.

        """
        logger.info(f"Creating new seed in collection ID: {collection_id}")

        # Handle metadata from other_params
        if other_params and "metadata" in other_params:
            other_params_metadata = other_params.pop("metadata")
            # Combine with metadata parameter if provided
            if metadata:
                metadata.update(other_params_metadata)
            else:
                metadata = other_params_metadata

        # Validate input using Pydantic
        try:
            seed_create = SeedCreate(
                url=url,
                collection=collection_id,
                crawl_definition=crawl_definition_id,
            )
        except ValidationError as e:
            logger.error(
                f"Invalid seed creation data for collection ID {collection_id}: {e}"
            )
            raise

        # Convert to dict for API request
        payload: dict = seed_create.model_dump(
            exclude_none=True, by_alias=True, mode="python"
        )

        logger.debug(f"Seed creation payload: {payload}")

        # Add any additional params
        if other_params:
            payload.update(other_params)

        response = self.httpx_client.post(
            "seed",
            data=payload,
        )
        seed_data = response.json()
        logger.info(f"Successfully created seed in collection ID: {collection_id}")

        # If metadata is provided, update it after seed creation
        if metadata:
            seed_id = seed_data.get("id")
            if seed_id:
                logger.info(f"Updating metadata for newly created seed ID: {seed_id}")
                self.update_seed_metadata(seed_id=seed_id, metadata=metadata)
                # Refresh seed_data to include updated metadata
                seed_data["metadata"] = metadata
            else:
                logger.warning(
                    "Seed created but no ID returned, cannot update metadata"
                )

        return ModelValidator.validate(
            SeedKeys, seed_data, f"created seed in collection {collection_id}"
        ).model_dump()

    def delete_seed(
        self,
        seed_id: str | int,
    ) -> dict:
        """Delete a seed by its ID.

        Args:
            seed_id (str | int): The ID of the seed to delete.

        Returns:
            dict: The validated seed data from the API after deletion. The 'deleted' flag should be True.

        Raises:
            ValidationError: If the API returns invalid seed data.

        """
        logger.info(f"Deleting seed ID: {seed_id}")

        response = self.httpx_client.patch(
            f"seed/{seed_id}",
            data={"deleted": True},
        )  # The API uses PATCH 'deleted' flag to delete seeds

        logger.info(f"Successfully deleted seed ID: {seed_id}")

        seed_data = response.json()

        # Validate and return the response
        return ModelValidator.validate(
            SeedKeys, seed_data, f"deleted seed {seed_id}"
        ).model_dump()
