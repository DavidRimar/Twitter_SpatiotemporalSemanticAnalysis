import spacy
from Tensor2attr import *
from TweetCrawler import *
from config import *
from models.ModelMarch import *
from nltk.tokenize import TweetTokenizer

### QUERY TWEETS
tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)
query_df = tweetCrawler.crawl_data_with_session(March_Tweets, filtering='% march %')

print(len(query_df))

### MODEL INIT
# Load a Transformer-based language model; assing to variable 'nlp'
nlp_trf = spacy.load('en_core_web_trf')

# Load a large language model and assign it to the variable 'nlp_lg'
nlp_lg = spacy.load('en_core_web_lg')

# Add the component named 'tensor2attr', which we registered using the
# @Language decorator and its 'factory' method to the pipeline.
nlp_trf.add_pipe('tensor2attr')

# Call the 'pipeline' attribute to examine the pipeline
# print(nlp_trf.pipeline)

# process the syntetised example sentences with the transformer-based model and the large laanguage model
doc_march_movement_1_trf = nlp_trf('Some protesters march through the city as tensions escalate unexpectedly')
doc_march_movement_2_trf = nlp_trf('As police invaded the crowd, people decided to march towards the square.')
doc_march_movement_3_trf = nlp_trf('Activitist organized a coordinated march to make their voices heard against the bill')

doc_march_month_1_trf = nlp_trf('The are protests on Saturday 26th March 2021 against the kill the bill movement')
doc_march_month_2_trf = nlp_trf('Cant believe it is March already, wanna wear my new hoodies xD.')
doc_march_month_3_trf = nlp_trf('The government announced new plans for green investments, effective as of March 2022')

doc_march_movement_lg = nlp_lg('The protesters march through the city as tensions escalate unexpectedly')
doc_march_month_lg = nlp_lg('The are protests on Saturday 26th March 2021 against the kill the bill movement')

#print(doc_march_month_lg)

# Retrieve vectors for the two Tokens corresponding to "march";
# assign to variables 'march_movement' and 'march_month'.
march_movement_1_trf = doc_march_movement_1_trf[2]
march_movement_2_trf = doc_march_movement_2_trf[9]
march_movement_3_trf = doc_march_movement_3_trf[4]

march_month_1_trf = doc_march_month_1_trf[6]
march_month_2_trf = doc_march_month_2_trf[5]
march_month_3_trf = doc_march_month_3_trf[12]

print("march movement 1: ", march_movement_1_trf)
print("march movement 2: ", march_movement_2_trf)
print("march movement 3: ", march_movement_3_trf)

print("march month 1: ", march_month_1_trf)
print("march month 2: ", march_month_2_trf)
print("march month 3: ", march_month_3_trf)

march_movement_lg = doc_march_movement_lg[2]
march_month_lg = doc_march_month_lg[6]

# Compare the similarity of the two meanings of 'march'
print("Similarity of march (diff sense) with the transformer model", march_movement_1_trf.similarity(march_month_1_trf))
print("Similarity of march (same sense) with the transformer model", march_movement_1_trf.similarity(march_movement_2_trf))

print("Similarity of march with the large language model ", march_movement_lg.similarity(march_month_lg))

def classify_march(df):

    new_df = df

    new_df['classified_march'] = None

    for index, row, in df.iterrows():

        text = row['text']
        tweet_tokenizer = TweetTokenizer()
        tokenized_tweet = tweet_tokenizer.tokenize(text)

        doc_text_trf = nlp_trf(text)

        # FIND THE INDEX POSITION OF THE MARCH INDEX
        march_index = 9999

        for i in range(1, len(tokenized_tweet)):

            #print(type(tokenized_tweet[i]))

            if tokenized_tweet[i].lower() == 'march':

                print("sdgsdgsd")

                march_index = i

        # COMPARE SIMILARITY OF text 'march' with example 'march'

        # if the word 'march' appears
        if march_index < 9999:

            # get vector representation of 'march' using the march_index
            march_vr_trf = doc_text_trf[march_index]

            # march_movement_count
            march_movement_count = 0

            # march_month_count
            march_month_count = 0

            # use similarity threshold of 0.5 to decide if
            # this is march in the movement sense (using 3 proxies)
            # or this is march in the month sense (using 3 proxies)
            # add to respective counts
            if march_movement_1_trf.similarity(march_vr_trf) > 0.5:

                march_movement_count += 1
            
            if march_movement_2_trf.similarity(march_vr_trf) > 0.5:

                march_movement_count += 1

            if march_movement_3_trf.similarity(march_vr_trf) > 0.5:

                march_movement_count += 1
            
            if march_month_1_trf.similarity(march_vr_trf) > 0.5:
    
                march_month_count += 1
            
            if march_month_2_trf.similarity(march_vr_trf) > 0.5:

                march_month_count += 1

            if march_month_3_trf.similarity(march_vr_trf) > 0.5:

                march_month_count += 1


            # use above counts to decide how 'march' is used
            if march_month_count < march_movement_count:

                new_df.at[index, 'classified_march'] = 'Movement'

            elif march_month_count > march_movement_count:
                
                new_df.at[index, 'classified_march'] = 'Month'

            elif  march_month_count == march_movement_count:

                new_df.at[index, 'classified_march'] = 'Undecided'

    return new_df

classed_march_df = classify_march(query_df[:10])
print(classed_march_df.head(12))