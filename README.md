## Twitter Semantics and STDBSCAN

This project uses Twitter data to detect spatiotemporal and semantic patterns of a specified target event. It implements the following methododologies:

    1. TF-IDF significant word discovery on spatiotemporal partitions of tweets
    2. Text Classification with spaCy with labelled tweets targeting the "2021 Bristol riots"
    3. Spatiotemporal clustering of classified tweets with STDBSCAN
    4. Polysemous word disambiguation with contextual embeddings

# Main References

- TF-IDF and MAUP:
  `W. Mackaness and O. Chaudry, “Assessing the Veracity of Methods for Extracting Place Semantics from Flickr Tags”, University of Edinburgh, Public Health England, Transactions in GIS, 2013, vol. 17, Issue 4`
- Text Classification with spaCy: https://www.machinelearningplus.com/nlp/custom-text-classification-spacy/
- ST-DBSCAN: https://github.com/eubr-bigsea/py-st-dbscan
- Contextual embeddings: https://applied-language-technology.readthedocs.io/en/latest/notebooks/part_iii/04_embeddings_continued.html
