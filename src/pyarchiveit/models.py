"""Models for endpoints in Archive-it API."""

from pydantic import BaseModel, Field


class MetadataValue(BaseModel):
    """A single metadata value item."""

    value: str | int | float = Field(..., description="The metadata value")
    id: str | None = Field(None, description="ID for the metadata value")
    model_config = {
        "extra": "forbid",
        "strict": True,  # Prevent type coercion (e.g., bool to int)
    }


class SeedKeys(BaseModel):
    """Model representing the keys for a Seed object from Archive-it API.

    This model accepts data from the Archive-it API and validates the structure.
    Extra fields are allowed since the API may return additional fields.
    """

    id: int = Field(..., description="Unique identifier for the seed")
    created_by: str | None = Field(..., description="User who created the seed")
    created_date: str | None = Field(..., description="Date when the seed was created")
    last_updated_by: str | None = Field(
        ..., description="User who last updated the seed"
    )
    publicly_visible: bool | None = Field(
        ..., description="Indicates if the seed is publicly visible"
    )
    http_response_code: int | None = Field(..., description="HTTP response code")
    last_checked_http_response_code: int | None = Field(
        None, description="Last checked HTTP response code"
    )
    active: bool = Field(..., description="Indicates if the seed is active")
    collection: int = Field(..., description="Collection ID the seed belongs to")
    valid: bool | None = Field(..., description="Indicates if the seed is valid")
    seed_type: str | None = Field(..., description="Type of the seed")
    deleted: bool = Field(..., description="Indicates if the seed is deleted")
    last_updated_date: str = Field(
        ..., description="Date when the seed was last updated"
    )
    url: str = Field(..., description="URL of the seed")
    crawl_definition: int = Field(
        ..., description="Crawl definition ID the seed belongs to"
    )
    canonical_url: str = Field(..., description="Canonical URL of the seed")
    login_username: str | None = Field(..., description="Login username for the seed")
    login_password: str | None = Field(..., description="Login password for the seed")
    metadata: dict | None = Field(..., description="Metadata for the seed")
    seed_groups: list | None = Field(
        ..., description="List of seed groups the seed belongs to"
    )

    model_config = {
        "extra": "allow",  # Allow extra fields from API responses
    }


class SeedCreate(BaseModel):
    """Model for creating a new seed (user input).

    This model forbids extra fields to prevent users from submitting invalid data.
    """

    url: str = Field(..., description="URL of the seed to create")
    collection: str | int = Field(..., description="Collection ID to add the seed to")
    crawl_definition: str | int = Field(
        ..., description="Crawl definition ID for the seed"
    )

    # Fields that users SHOULD NOT set (will be rejected)
    # By not including them and using extra="forbid", they're automatically forbidden

    model_config = {
        "extra": "forbid",  # Forbid any fields not explicitly defined
    }


class SeedUpdate(BaseModel):
    """Model for updating a seed (user input).

    Only allows specific fields that users are permitted to update.
    """

    metadata: dict[str, list[MetadataValue]] | None = Field(
        default=None, description="Metadata to update"
    )
    deleted: bool | None = Field(default=None, description="Mark seed as deleted")

    # # Define forbidden fields explicitly for better error messages
    # FORBIDDEN_FIELDS: set[str] = {
    #     "id",
    #     "created_by",
    #     "create_date",
    #     "collection",
    #     "url",
    #     "crawl_definition",
    #     "active",
    #     "valid",
    # }

    model_config = {
        "extra": "forbid",  # Forbid any extra fields
    }
