#!/bin/bash

# have job exit if any command returns with non-zero exit status (aka failure)
# set -e

# uninstall
if [ -e /mnt/onboard/.AMR/uninstall.* ]
then
    rm -rf /mnt/onboard/.AMR
    sed -r -e '/^127\.0\.0\.42\s.*/d' -i /etc/hosts
    exit
fi

# vhosts
if [ -e /mnt/onboard/.AMR/vhosts.conf ]
then
    cp /etc/hosts /tmp/mangaportal_hosts
    sed -r -e '/^127\.0\.0\.42\s.*/d' -i /tmp/mangaportal_hosts
    echo 127.0.0.42 $(sed -e 's@#.*@@' /mnt/onboard/.AMR/vhosts.conf | sort) >> /tmp/mangaportal_hosts
    cmp /etc/hosts /tmp/mangaportal_hosts || cp /tmp/mangaportal_hosts /etc/hosts
fi

# prepare network
ifconfig lo 127.0.0.1
ip addr replace 127.0.0.42 dev lo

# export paths and run Python script or app
cd /mnt/onboard/.AMR/
export LD_LIBRARY_PATH=/mnt/onboard/.AMR/amrpyenv/lib:$LD_LIBRARY_PATH
export PYTHONHOME=/mnt/onboard/.AMR/amrpyenv
export FLASK_APP=AMRmain
export FLASK_DEBUG=1
/mnt/onboard/.AMR/amrpyenv/bin/python3 -m flask run --host=127.0.0.42 --port=1234 --no-reload
