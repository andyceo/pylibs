`pylibs` is a collection of python packages for use in other projects.

## Pull Docker image

    sudo docker pull andyceo/pylibs

## Build Docker image with your project with `andyceo/pylibs` dependency

    FROM andyceo/pylibs
    #...

## Building Docker image

    sudo docker build -t andyceo/pylibs:rev_<LAST_REVISION_ID_OR_TAG_OR_DATE>

You also can use `build.sh` script to build and push image to custom repository with custom tag. To customize image repostory and tag, provide environment variables `$REPO` and `$TAG` respectively.
