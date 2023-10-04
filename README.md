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

This will put the Wikipedia files under `wikipedia/cleaned/` and the corresponding DBpedia files under `dbpedia/cleaned/`.

# Evaluation metrics

Usage for the eval metric is:

`python scripts/eval.py --reference dbpedia/cleaned/<some_reference_kb>.txt --prediction <your_predicted_kb>`

The predicted KB should contain one triple per line, in the format `<subject> <relation> <object>`. Look at reference DBpedia files (under `dbpedia/cleaned/`) if in doubt about the format. The output of the eval script is precision, recall and F1 score, for two settings:

- Exact match. Here, a predicted triple is counted as correct if it exactly matches a triple in the reference KB. This is a very strict metric.

- Soft match. This computes a similarity score for each pair of (predicted\_triple, reference\_triple). On that basis,

  - precision is the sum of the highest similarity (to a reference triple) for each predicted triple, divided by the number of predicted triples.

  - recall is the sum of the highest similarity (to a predicted triple) for each reference triple, divided by the number of reference triples.

The similarity score of two triples is a number between 0 and 1, and is based on the edit distance between their subjects, relations and objects. The closer the string representations, the higher the similarity score. The soft match metric will give partial credit to triples that are almost right. For reference, here are a few similarity scores:

\<Ada\_Lovelace\> \<child\> \<Anne\_Blunt,\_15th\_Baroness\_Wentworth\> --- \<Lovelace\> \<child\> \<Anne\_Blunt,\_15th\_Baroness\_Wentworth\> --- 0.8992886260452183

\<Ada\_Lovelace\> \<child\> \<Ralph\_King-Milbanke,\_2nd\_Earl\_of\_Lovelace\> --- \<Lady\_Lovelace\> \<child\> \<Ralph\_King-Milbanke\> --- 0.7469007910928608

\<Ada\_Lovelace\> \<spouse\> \<William\_King-Noel,\_1st\_Earl\_of\_Lovelace\> --- \<Ada\_Lovelace\> \<married\> \<William\_King-Noel,\_1st\_Earl\_of\_Lovelace\> --- 0.5227579585747103


Additional arguments to the `script/eval.py`:

- `alignment`: whether to print the alignment used for the soft match scores.

- `significant`: the number of digits after the comma for metric scores.

If in doubt, run `python scripts/eval.py -h`.

# IE tools to try out

- spacy.io

- NLTK https://www.nltk.org/

- Regular expressions https://regex101.com/

- Stanford CoreNLP https://corenlp.run/

- OpenIE (in Stanford CoreNLP)

- FrameNet https://framenet.icsi.berkeley.edu/

Run them, use the eval script, look at the errors, try to tweak the method to increase the scores.
