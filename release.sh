#!/usr/bin/bash

# example usage:
# version=1.4.2 message="biggest release till now!" ./release.sh
# optionally you could clean with: ./release.sh clean 

if [ "$1" = "clean" ]; then
    rm -r dist
    rm -r *.egg-info
    exit
fi

if [ -z ${version+x} ]; then
    echo "no version set"
    exit
fi

if [ -z ${message+x} ]; then
    echo "no message set"
    exit
fi
exit

git tag $version -m "$message"
git tag

python setup.py register -r pypitest
python setup.py sdist upload -r pypitest

python setup.py register -r pypi
python setup.py sdist upload -r pypi
