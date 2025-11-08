# 📦 Pyarchiveit

[Pyarchiveit](https://pypi.org/project/pyarchiveit/) is a Python library designed to interact with the Internet Archive's Archive-it API. It provides a simple interface to manage the seeds and collections within Archive-it accounts.

!!! warning
    🚨This library is under active development. Use at your own risk. 🚨

## ✨ Features
- Create and update seeds with metadata validation
- Retrieve seed lists with their metadata for single or multiple collections
- Export seed data to CSV and XLSX formats

## 📥 Installation
You can install the library using pip:
``` bash
pip install pyarchiveit
```
Or use [uv](https://github.com/astral-sh/uv) if you have it installed:
``` bash
uv add pyarchiveit
```

!!! tip
    As a best practice (and since the project is under active development), you should pin the version of `pyarchiveit` when installing it, e.g. `pip install pyarchiveit==0.1.0` or `uv add pyarchiveit==0.1.0`, to avoid unexpected issues from future updates.

## 💡 Quick Start

See the [Getting Started](getting-started.md) guide for detailed installation and initialization instructions.

### Create a new seed with metadata

``` Python
metadata = { # (1)!
    'title':[{"value": "Example Metadata 1"}],
    'another_field':[
        {"value": "Example Metadata 2"},
        {"value": "Additional Metadata"}
        ]
}

new_seed = archive_it_client.create_seed(
    collection_id=123456,
    url="http://example.com",
    crawl_definition_id=41125648146,
    other_params=None,
    metadata=metadata,
)

```

1.  To specify metadata fields, the `metadata` parameter should be a dictionary where each key is the metadata field name, and the value is a list of dictionaries. Each dictionary in the list should contain a "value" key with the corresponding metadata value. The structure MUST be followed or the API will reject the request.

### Update an existing seed's metadata

``` Python
metadata = {
    'title':[{"value": "Example Metadata 1"}],
    'another_field':[
        {"value": "Example Metadata 2"},
        {"value": "Additional Metadata"}
        ]
}
updated_seed = archive_it_client.update_seed_metadata(
    seed_id=123456,
    metadata=updated_metadata
)
```

### Retrieve seed lists

``` Python
# Get seed list of a collection
seeds = archive_it_client.get_seeds(collection_ids=123456)

# Or get seeds from multiple collections
seeds = archive_it_client.get_seeds(collection_ids=[123456, 789012])
```

!!! tip
    See the [ArchiveItAPI Reference](api/ArchiveItAPI.md) for full method documentation.

## ⚫ Support

For questions or support, please open an issue on the [GitHub repository](https://github.com/kenlhlui/pyarchiveit/issues).

## 🖊️ Author

[Ken Lui](https://github.com/kenlhlui) - Data Curation Specialist at [Map & Data Library, University of Toronto](https://mdl.library.utoronto.ca/)

## 📄 License

This project is licensed under the GNU GPLv3 - see the [LICENSE](https://github.com/kenlhlui/pyarchiveit/blob/main/LICENSE) file for details.

