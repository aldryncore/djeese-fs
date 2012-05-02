#!/bin/sh

python setup.py sdist
filename="dist/`ls dist/ | tail -n1`"
scp $filename pkg@pkg.djeese.com:data/
