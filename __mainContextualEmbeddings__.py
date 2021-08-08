import spacy
from Tensor2attr import *
from TweetCrawler import *
from config import *
from models.ModelMarch import *
from nltk.tokenize import TweetTokenizer
from DataLoader import *

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

doc_march_month_1_trf = nlp_trf('The are protests on Saturday 26th March 2021 against the bill')
doc_march_month_2_trf = nlp_trf('Cant believe it is March already, wanna wear my new hoodies xD.')
doc_march_month_3_trf = nlp_trf('The government announced new plans for green investments, effective as of 29th March 2022')

doc_march_movement_lg = nlp_lg('The protesters march through the city as tensions escalate unexpectedly')
doc_march_month_lg = nlp_lg('The are protests on Saturday 26th March 2021 against the bill')

#print(doc_march_month_lg)

# Retrieve vectors for the two Tokens corresponding to "march";
# assign to variables 'march_movement' and 'march_month'.
march_movement_1_trf = doc_march_movement_1_trf[2]
march_movement_2_trf = doc_march_movement_2_trf[9]
march_movement_3_trf = doc_march_movement_3_trf[4]

march_month_1_trf = doc_march_month_1_trf[6]
march_month_2_trf = doc_march_month_2_trf[5]
march_month_3_trf = doc_march_month_3_trf[13]


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

        # FIND THE MARCH TOKEN
        march_vr_trf = None

        for i in range(1, len(doc_text_trf)):

            if doc_text_trf[i].text.lower() == 'march':

                # save the march vector representation
                march_vr_trf = doc_text_trf[i]

                break

        # COMPARE SIMILARITY OF text 'march' with example 'march'

        # if the march vector representation exists
        if march_vr_trf is not None:

            # march_movement_count
            march_movement_count = 0

            # march_month_count
            march_month_count = 0

            # use similarity threshold of 0.5 to decide if
            # this is march in the movement sense (using 3 proxies)
            # or this is march in the month sense (using 3 proxies)
            # add to respective counts

            march_movement_count += march_movement_1_trf.similarity(march_vr_trf)
            march_movement_count += march_movement_2_trf.similarity(march_vr_trf)
            march_movement_count += march_movement_3_trf.similarity(march_vr_trf)

            march_month_count += march_month_1_trf.similarity(march_vr_trf)
            march_month_count += march_month_2_trf.similarity(march_vr_trf)
            march_month_count += march_month_3_trf.similarity(march_vr_trf)

            """
            if march_movement_1_trf.similarity(march_vr_trf) > 0.05:

                march_movement_count += march_movement_1_trf.similarity(march_vr_trf)
            
            if march_movement_2_trf.similarity(march_vr_trf) > 0.05:

                march_movement_count += march_movement_2_trf.similarity(march_vr_trf)

            if march_movement_3_trf.similarity(march_vr_trf) > 0.05:

                march_movement_count += march_movement_3_trf.similarity(march_vr_trf)
            
            if march_month_1_trf.similarity(march_vr_trf) > 0.05:
    
                march_month_count += march_month_1_trf.similarity(march_vr_trf)
            
            if march_month_2_trf.similarity(march_vr_trf) > 0.05:

                march_month_count += march_month_2_trf.similarity(march_vr_trf)

            if march_month_3_trf.similarity(march_vr_trf) > 0.05:

                march_month_count += march_month_3_trf.similarity(march_vr_trf)
            """

            # use above counts to decide how 'march' is used
            if march_month_count < march_movement_count:

                print(text)
                print("march month: ", march_month_count)
                print("march move: ", march_movement_count)

                new_df.at[index, 'classified_march'] = 'Movement'

            elif march_month_count > march_movement_count:
                
                new_df.at[index, 'classified_march'] = 'Month'

            elif march_month_count == march_movement_count:

                print(text)
                print("march month: ", march_month_count)
                print("march move: ", march_movement_count)

                new_df.at[index, 'classified_march'] = 'Undecided'

    return new_df

classed_march_df = classify_march(query_df)
#print(classed_march_df.head(12))

# DATA LOAD
data_loader = DataLoader(DATABASE_URI_RDS_TWEETS)

data_loader.update_all(classed_march_df, March_Tweets)