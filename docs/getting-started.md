# Getting Started

## Installation

Install pyarchiveit using pip or uv:

=== "pip"

    ```bash
    pip install pyarchiveit
    ```

=== "uv"

    ```bash
    uv add pyarchiveit
    ```

## Initialization

You will need to initialize the `ArchiveItAPI` class with your account credentials.

=== "Using environment variables (recommended)"

    It is a better practice to set your credentials as environment variables (.env) and read them in your code instead of hardcoding them. You may use the `python-dotenv` package to help with this.

    === "pip"

        ```bash
        pip install python-dotenv
        ```

    === "uv"

        ```bash
        uv add python-dotenv
        ```

    Then, create a `.env` file in your project directory with the following content:
    ```
    ARCHIVE_IT_ACCOUNT_NAME=your_username
    ARCHIVE_IT_ACCOUNT_PASSWORD=your_password
    ```

    Now, read the environment variables in your code and initialize the `ArchiveItAPI` client:
    ```python
    import os
    from dotenv import load_dotenv
    load_dotenv()
    from pyarchiveit import ArchiveItAPI

    archive_it_client = ArchiveItAPI(
        account_name=os.getenv('ARCHIVE_IT_ACCOUNT_NAME'),
        account_password=os.getenv('ARCHIVE_IT_ACCOUNT_PASSWORD')
    )
    ```

=== "Direct initialization"

    ```python
    from pyarchiveit import ArchiveItAPI

    # Initialize the Archive-it API client with your credentials
    archive_it_client = ArchiveItAPI(
        account_name='your_username',
        account_password='your_password'
    )
    ```

## Next Steps

Now that you have initialized the client, you can start using the Archive-it API. Check out the [API Reference](api/ArchiveItAPI.md) for available methods and their documentation.
