import spacy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from TweetCrawler import *
from config import *
from models.ModelBristol import *
from SpacyTextClassifier import *
from DataLoader import *

#### GET DATA ####
tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)
bristol_tweets_df = tweetCrawler.crawl_data_with_session(
    Bristol_Set2_TextClassifier)

#### TRAIN AND TEST DATA ####
# instantiate spacyTextClassifier instance
spacyTextClassifier = SpacyTextClassifier()

# prepare_training_data()
train_data = spacyTextClassifier.prepare_training_data(bristol_tweets_df)

# train_and_evaluate()
spacyTextClassifier.train_model_and_evaluate(train_data, 10)

#### APPLY MODEL ON UNSEEN TWEETS ####
"""
test_text_1 = "The police is struggling to contain the protest as people continue to march."
test_text_2 = "This is the biggest headache of the police in March"
test_text_3 = "The #KilltheBill rally marches through #Manchester, thankfully with very little Police presence so far, just at the back. Hoping @gmpolice have observed from Bristol exactly what not to do."
text_text_4 = "Evidence of Journalist at the receiving end of police violence in Bristol. Such indiscriminate violence against protestors creates an inter group dynamic. This is NOT one sided"
text_text_5 = "I just wanna say thanks to @metpoliceuk Kingston today for not resorting to violence like @ASPolice have done recently. It’s nice to know you’re capable of the bare minimum restraint. #KillTheBill also make sure your officers are wearing PPE properly when talking to public."
text_list = [test_text_1, test_text_2, test_text_3, text_text_4, text_text_5]

spacyTextClassifier.test_model(text_list)
"""

classified_tweets_df = spacyTextClassifier.classify_unseen_tweets(
    bristol_tweets_df)

### LOAD RESULTS TO DB ###
dataLoader = DataLoader(DATABASE_URI_RDS_TWEETS)

dataLoader.update_all(classified_tweets_df, Bristol_Set2_TextClassifier)
