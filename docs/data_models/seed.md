# Seed

The `Seed` model represents the complete seed object returned by the Archive-It API. It includes all fields that the API provides, including read-only fields like `id`, `created_date`, and `last_updated_date`.

---

::: pyarchiveit.models.Seed
    options:
      show_root_heading: false
      show_docstring_description: false
      show_source: false
      show_bases: false
      members_order: source
      members: false
      heading_level: 3



### Protected Fields

The following fields are **read-only** and cannot be set via user input:

- `id`
- `created_by`
- `created_date`
- `last_updated_by`
- `last_updated_date`
- `canonical_url`
- `http_response_code`
- `last_checked_http_response_code`
- `valid`
- `seed_type`
- `canonical_url`

These fields are automatically populated by the Archive-It API.