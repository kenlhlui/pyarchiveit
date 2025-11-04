# ArchiveItAPI Reference

The main client class for interacting with the Archive-it API.

You will first need to initialize the `ArchiveItAPI` class with your account credentials:

```python
from pyarchiveit import ArchiveItAPI
archive_it_client = ArchiveItAPI(
    account_name='your_username',
    account_password='your_password'
)
```

::: pyarchiveit.api.ArchiveItAPI
    options:
      show_root_heading: false
      show_source: false
      members_order: source
      heading_level: 2
      show_docstring_description: false
