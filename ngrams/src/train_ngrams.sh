#!/bin/bash
shopt -s expand_aliases
source ~/.zshrc

set -e

ngram-count -text /Users/yanshengjia/GitHub/automated-essay-scoring/data/language-model/ngrams/corpus.txt -order 3 -lm /Users/yanshengjia/GitHub/automated-essay-scoring/data/language-model/ngrams/corpus.lm -interpolate -kndiscount
wait
echo "Ngrams Count Done!"

cd /Users/yanshengjia/GitHub/automated-essay-scoring/data/language-model/ngrams
python3 arpa_parser.py
wait
echo "ARPA Parsing Done!"