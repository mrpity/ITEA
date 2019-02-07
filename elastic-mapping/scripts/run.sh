#!/usr/bin/env sh

set -euo pipefail

pip install --upgrade pip
pip install -U --no-cache-dir -r /workdir/requirements.txt

echo "RUN: python3 /workdir/elastic_utils.py -a $MAPPING_ACTION -m $MAPPING_LIST -e $ELASTICSEARCH_URL"
exec python3 /workdir/elastic_utils.py -a $MAPPING_ACTION -m $MAPPING_LIST -e $ELASTICSEARCH_URL
