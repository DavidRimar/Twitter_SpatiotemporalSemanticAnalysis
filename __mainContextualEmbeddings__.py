import spacy
from Tensor2attr import *

### MODEL INIT
# Load a Transformer-based language model; assing to variable 'nlp'
nlp_trf = spacy.load('en_core_web_trf')

# Load a large language model and assign it to the variable 'nlp_lg'
#nlp_lg = spacy.load('en_core_web_lg')

# Add the component named 'tensor2attr', which we registered using the
# @Language decorator and its 'factory' method to the pipeline.
nlp_trf.add_pipe('tensor2attr')

# Call the 'pipeline' attribute to examine the pipeline
# print(nlp_trf.pipeline)

# process the syntetised example sentences with the transformer-based model and the large laanguage model
doc_march_movement_trf = nlp_trf('The protesters march through the city as tensions escalate unexpectedly')
doc_march_month_trf = nlp_trf('The are protests on Saturday 26th March 2021 against the kill the bill movement')
doc_march_movement_2_trf = nlp_trf('An organized march is expected on Friday in the city of Luton')

#doc_march_movement_lg = nlp_lg('The protesters march through the city as tensions escalate unexpectedly')
#doc_march_month_lg = nlp_lg('The are protests on Saturday 26th March 2021 against the kill the bill movement')

#print(doc_march_month_lg)

# Retrieve vectors for the two Tokens corresponding to "march";
# assign to variables 'march_movement' and 'march_month'.
march_movement_trf = doc_march_movement_trf[3]
money_month_trf = doc_march_month_trf[7]
money_movement_2_trf = doc_march_month_trf[3]

#march_movement_lg = doc_march_movement_lg[3]
#money_month_lg = doc_march_month_lg[7]

# Compare the similarity of the two meanings of 'capital'
print("Similarity of march with the transformer model", march_movement_trf.similarity(money_month_trf))
print("Similarity of march with the transformer model", march_movement_trf.similarity(money_movement_2_trf))

#print("Similarity of march with the large language model ", march_movement_lg.similarity(money_month_lg))

def classify_march(df):

    for index, row, in df.iterrows():

        text = row['text']

        print(text)