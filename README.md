`pylibs` is a collection of python packages for use in other projects.

## Pull Docker image

    sudo docker pull andyceo/pylibs

## Build Docker image with your project with `andyceo/pylibs` dependency

    FROM andyceo/pylibs
    #...

## Building Docker image

    sudo docker build -t andyceo/pylibs:rev_<LAST_REVISION_ID_OR_TAG_OR_DATE>
