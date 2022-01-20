# https://github.com/bimdata/docker-images/blob/main/Dockerfile.poetry
FROM docker-registry.bimdata.io/bimdata/python-poetry:3.9 as builder-base


# https://github.com/bimdata/docker-images/blob/main/Dockerfile.django
FROM docker-registry.bimdata.io/bimdata/python-django:3.9

# $PYSETUP_PATH contains all packages installed by poetry
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

ENV COMPILE_MESSAGES=1
