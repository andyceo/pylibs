Python Libraries
================

`pylibs` is a collection of open-source (see [LICENSE](LICENSE)) Python packages and libraries to use in other projects.


## Testing

    python3 -m unittest test.test_config


## Pull Docker image

    sudo docker pull andyceo/pylibs


## Build Docker image with your project with `andyceo/pylibs` dependency

    FROM andyceo/pylibs
    #...


## Building Docker image

    sudo docker build -t andyceo/pylibs:rev_<LAST_REVISION_ID_OR_TAG_OR_DATE>

You also can use `build.sh` script to build and push image to custom repository with custom tag. To customize image repostory and tag, provide environment variables `$REPO` and `$TAG` respectively.


## Updating your PYTHONPATH for easy import

Create a `.pth` file inside your site directory or change `.bashrc`. See more on [Permanently add a directory to PYTHONPATH](https://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath)


## Packages interdependencies

This list represent the packages interdependencies. Requirements are listed in package's `requirements.txt` file.

- `aiml`: none
- `singleton`: none
- `timefuncs`: none
- `webserver`: none
- `bitfinex`: timeframeds
- `timeframeds`: timefuncs
- `dblogging`: peeweext


## Curated list of awesome third-party Python packages and libraries

This list is not restricted by libraries used only in this repository.

- `bitfinex-api-py`: library for interacting with Bitfinex API (wriiten by Bitfinex itself)
    - Github: https://github.com/bitfinexcom/bitfinex-api-py
    - PyPi: https://pypi.org/project/bitfinex-api-py/
    - Installation: `pip install bitfinex-api-py`
- `ciso8601`: fast `C` library for parsing ISO 8601 date strings (really fast!)
    - Github: https://github.com/closeio/ciso8601
    - PyPi: https://pypi.org/project/ciso8601/
    - Installation: `pip install ciso8601`
- `requests`: work with HTTP/HTTPS requests, fetching data from url, etc.
    - Github: https://github.com/psf/requests
    - Documentation: https://requests.readthedocs.io/en/master/
    - PyPi: https://pypi.org/project/requests/
    - Installation: `pip install requests`

For russian-speaking users: also take a look at my [Python docpage (ru)](https://github.com/andyceo/documentation/wiki/Python)
