import spacy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from TweetCrawler import *
from config import *
from models.ModelBristol import *
from SpacyTextClassifier import *

#### GET DATA ####
tweetCrawler = TweetCrawler(DATABASE_URI_RDS_TWEETS)
bristol_tweets_df = tweetCrawler.crawl_data_with_session(
    BristolSEM)

#### TRAIN AND TEST DATA ####
# instantiate spacyTextClassifier instance
spacyTextClassifier = SpacyTextClassifier()

# prepare_training_data()
train_data = spacyTextClassifier.prepare_training_data(bristol_tweets_df)

# train_and_evaluate()
spacyTextClassifier.train_model_and_evaluate(train_data, 2)

#### APPLY MODEL ON UNSEEN TWEETS ####
test_text_1 = "The police is struggling to contain the protest as people continue to march."
test_text_2 = "This is the biggest headache of the police in March"
text_list = [test_text_1, test_text_2]

spacyTextClassifier.test_model(text_list)
