wikipedia_text := wikipedia/cleaned
wikipedia_raw := wikipedia/raw
dbpedia_raw := dbpedia/raw
dbpedia_cleaned := dbpedia/cleaned

all: wikipedia-txt dbpedia-txt $(dbpedia_raw)/Albert_Einstein.json

clean:
	rm $(wikipedia_text)/*
	rm wikipedia-txt
	rm $(dbpedia_raw)/*
	rm $(dbpedia_cleaned)/*

wikipedia-txt: $(wikipedia_text)/Ada_Lovelace.txt $(wikipedia_text)/Alan_Turing.txt $(wikipedia_text)/Albert_Einstein.txt $(wikipedia_text)/Alonzo_Church.txt $(wikipedia_text)/Charles_Babbage.txt $(wikipedia_text)/David_Hilbert.txt $(wikipedia_text)/Emmy_Noether.txt $(wikipedia_text)/Frédéric_Joliot-Curie.txt $(wikipedia_text)/Irène_Joliot-Curie.txt $(wikipedia_text)/Marie_Curie.txt
	touch $@

dbpedia-txt: $(dbpedia_cleaned)/Ada_Lovelace.txt $(dbpedia_cleaned)/Alan_Turing.txt $(dbpedia_cleaned)/Albert_Einstein.txt $(dbpedia_cleaned)/Alonzo_Church.txt $(dbpedia_cleaned)/Charles_Babbage.txt $(dbpedia_cleaned)/David_Hilbert.txt $(dbpedia_cleaned)/Emmy_Noether.txt $(dbpedia_cleaned)/Frédéric_Joliot-Curie.txt $(dbpedia_cleaned)/Irène_Joliot-Curie.txt $(dbpedia_cleaned)/Marie_Curie.txt
	touch $@

$(wikipedia_text)/%.txt: scripts/clean-html.py $(wikipedia_raw)/%
	mkdir -p $(wikipedia_text)
	python3 $^ $@

$(wikipedia_raw)/%: scripts/download-wikipedia.sh
	mkdir -p $(wikipedia_raw)
	bash $^ $(notdir $@) $@

$(dbpedia_cleaned)/%.txt: scripts/clean-dbpedia.py $(dbpedia_raw)/%.json
	mkdir -p $(dbpedia_cleaned)
	python3 $^ $@

$(dbpedia_raw)/%.json: scripts/download-dbpedia.py $(wikipedia_text)/%.txt
	mkdir -p $(dbpedia_raw)
	python3 $^ $@
