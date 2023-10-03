# Lab session SD201
This repository contains files for the lab session of SD201.

# Contents
- Makefile: this ties together all the data download and preparation scripts
- download-wikipedia.sh: download relevant Wikipedia pages
- clean-html.py: strip pages of anything except the bare text
- download-dbpedia.py: download corresponding DBpedia pages, to be used as reference
- clean-dbpedia.py: remove some of the triples from DBpedia
- eval.py: compute evaluation metrics, to check quality of extracted knowledge base

# Installation
You need python 3. Feel free to create a virtual environment before running pip.

`pip install -r requirements.txt`

`git clone https://github.com/SgfdDttt/sd201.git`

`cd sd201`

`make`
