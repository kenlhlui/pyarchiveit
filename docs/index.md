# 📦 Pyarchiveit

Pyarchiveit is a Python library designed to interact with the Internet Archive's Archive-it API. It provides a simple interface to manage the seeds and collections within Archive-it accounts.

!!! warning
    This library is under active development. Use at your own risk.

## ✨ Features
- Create and update seeds with metadata validation
- Retrieve seed lists with their metadata for single or multiple collections

## 📥 Installation
You can install the library using pip:
```bash
pip install pyarchiveit
```
Or use [uv](https://github.com/astral-sh/uv) if you have it installed:
```bash
uv add pyarchiveit
```

## 💡 Quick Start

See the [Getting Started](getting-started.md) guide for detailed installation and initialization instructions.

### Create a new seed with metadata

```python
metadata = [
    {"value": "Example Metadata 1"},
    {"value": "Example Metadata 2"}
]
new_seed = archive_it_client.create_seed(
    collection_id=123456,
    url='http://example.com',
    crawl_definition_id=789012,
    other_params=None,
    metadata=metadata
)
```

### Update an existing seed's metadata

```python
updated_metadata = [
    {"value": "Updated Metadata 1"},
    {"value": "Updated Metadata 2"}
]
updated_seed = archive_it_client.update_seed_metadata(
    seed_id=123456,
    metadata=updated_metadata
)
```

See the [ArchiveItAPI](api/ArchiveItAPI.md) page for full method documentation.

### Retrieve seed lists

```python
# Get seed list of a collection
seeds = archive_it_client.get_seeds(collection_ids=123456)

# Or get seeds from multiple collections
seeds = archive_it_client.get_seeds(collection_ids=[123456, 789012])
```

## ⚫ Support

For questions or support, please open an issue on the [GitHub repository](https://github.com/kenlhlui/pyarchiveit/issues).

## 🖊️ Author

[Ken Lui](https://github.com/kenlhlui) - Data Curation Specialist at [Map & Data Library, University of Toronto](https://mdl.library.utoronto.ca/)

## 📄 License

This project is licensed under the GNU GPLv3.

