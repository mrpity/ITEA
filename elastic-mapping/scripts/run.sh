#!/usr/bin/env sh

set -euo pipefail

pip install --upgrade pip
pip install -U --no-cache-dir -r /workdir/requirements.txt

echo "RUN: python3 elastic_utils.py -a create -m webpages posts -elastic $ELASTICSEARCH_URL"
sleep 3600
#exec python3 /workdir/elastic_utils.py -a create -m webpages posts -elastic $ELASTICSEARCH_URL
