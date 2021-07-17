import numpy as np
import spacy
from spacy.util import minibatch, compounding
# from spacy.training import Example
# from spacy.pipeline.textcat import DEFAULT_SINGLE_TEXTCAT_MODEL
import random

"""
The TweetCrawler class is responsible for query the DB.
"""


class SpacyTextClassifier():

    ### CONSTRUCTOR ###
    def __init__(self):

        ### INSTANCE VARIABLES ###
        # self.config = {
        #    "threshold": 0.5,
        #    "model": DEFAULT_SINGLE_TEXTCAT_MODEL,
        # }
        # config validation error...
        self.config = {"exclusive_classes": True, "architecture": "simple_cnn"}

        # init spacy NLP instance
        self.nlp = spacy.load("en_core_web_sm")

        # textcat
        self.textcat = None

        # add the text classifier to the pipeline if it doesn't exist
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if 'textcat' not in self.nlp.pipe_names:
            self.textcat = self.nlp.create_pipe('textcat', config=self.config)
            self.nlp.add_pipe(self.textcat, last=True)
        # otherwise, get it, so we can add labels to it
        else:
            self.textcat = self.nlp.get_pipe('textcat')

        # Adding the labels to textcat
        self.textcat.add_label("POSITIVE")
        self.textcat.add_label("NEGATIVE")

        # variables for evaluation
        self.dev_texts = None
        self.dev_cats = None

    # ########## METHODS

    def load_data(self, train_tuples, split=0.8):
        """
        Splits the training data to train and test samples.

        """
        train_data = train_tuples  # raw_train needs to be a list of tuples
        # Shuffle the data
        random.shuffle(train_data)
        texts, labels = zip(*train_data)
        # get the categories
        cats = [{"POSITIVE": bool(y), "NEGATIVE": not bool(y)} for y in labels]
        # split training and test data
        split = int(len(train_data) * split)
        return (texts[: split], cats[: split]), (texts[split:], cats[split:])

    def prepare_training_data(self, raw_dataset_df):
        """
        Prepares training data.

        Uses load_data()
        """

        raw_dataset_df["label"] = None

        # tweets with score 4, 5 are POSITIVE ~ 1
        # tweets with score 0, 1 are NEGATIVE ~ 0
        # the rest are unknown and not used for training
        raw_dataset_df.label[raw_dataset_df.tweet_score <= 1] = 0
        raw_dataset_df.label[raw_dataset_df.tweet_score >= 4] = 1

        # get a sample of 2000 tweets each for pos and neg
        train_pos_df = raw_dataset_df[raw_dataset_df.label == 1][:1000]
        train_neg_df = raw_dataset_df[raw_dataset_df.label == 0][:1000]
        training_data = train_pos_df.append(train_neg_df)
        print("shape of training data: ", training_data.shape)

        print(training_data.head(10))
        print(training_data.tail(10))

        # spacy accepts list of tuples (text, label)
        training_data['tuples'] = training_data.apply(
            lambda row: (row['text'], row['label']), axis=1)  # adds a tuples column to training_data

        # convert the tuples column to a list
        train_tuples = training_data['tuples'].tolist()

        # usage of load_data
        (train_texts, train_cats), (dev_texts,
                                    dev_cats) = self.load_data(train_tuples)

        # set instance variables so these are accessible by other methods
        self.dev_texts = dev_texts
        self.dev_cats = dev_cats

        # after calling the above
        # Processing the final format of training data
        train_data = list(
            zip(train_texts, [{'cats': cats} for cats in train_cats]))
        # print("inspect final format of training data", train_data[:10])

        return train_data

    def evaluate(self, tokenizer, textcat, texts, cats):
        """
        Evaluates the model.
        """
        docs = (tokenizer(text) for text in texts)
        tp = 1e-8  # True positives
        fp = 1e-8  # False positives
        fn = 1e-8  # False negatives
        tn = 1e-8  # True negatives
        for i, doc in enumerate(textcat.pipe(docs)):
            gold = cats[i]
            for label, score in doc.cats.items():
                if label not in gold:
                    continue
                if score >= 0.5 and gold[label] >= 0.5:
                    tp += 1.
                elif score >= 0.5 and gold[label] < 0.5:
                    fp += 1.
                elif score < 0.5 and gold[label] < 0.5:
                    tn += 1
                elif score < 0.5 and gold[label] >= 0.5:
                    fn += 1
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f_score = 2 * (precision * recall) / (precision + recall)
        return {'textcat_p': precision, 'textcat_r': recall, 'textcat_f': f_score}

    def train_model_and_evaluate(self, train_data, n_iter):
        """
        The nlp instance gets updated for each training iterations, so
        the trained model is self.nlp > one needs to use this for live data.
        """
        # get names of other pipes to disable them during training

        other_pipes = [
            pipe for pipe in self.nlp.pipe_names if pipe != 'textcat']

        with self.nlp.disable_pipes(*other_pipes):  # only train textcat

            # with self.nlp.select_pipes(enable="textcat"):

            # create_optimizer() # resume_training()
            optimizer = self.nlp.begin_training()
            print("Training the model...")
            print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))

            # TRAINING ITERATIONS
            for i in range(n_iter):

                # TRAIN IN BATCHES
                losses = {}
                # batch up the examples using spaCy's minibatch

                batches = minibatch(
                    train_data, size=compounding(4., 32., 1.001))

                i = 0
                for batch in batches:

                    print("batch: ", i)

                    texts, annotations = zip(*batch)
                    # nlp instance gets updated
                    self.nlp.update(texts, annotations, sgd=optimizer, drop=0.2,
                                    losses=losses)

                    i += 1

                """ VERSION 3.0.0 and above
                for batch in minibatch(train_data, size=compounding(4., 32., 1.001)):

                    for text, annotations in batch:
                        # create Example object
                        doc = self.nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        # Update the model
                        # losses=losses, drop=0.3
                        self.nlp.update([example], sgd=optimizer)
                """

            # EVALUATE
            with self.textcat.model.use_params(optimizer.averages):
                # evaluate on the dev data split off in load_data()
                scores = self.evaluate(self.nlp.tokenizer, self.textcat,
                                       self.dev_texts, self.dev_cats)
            print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'  # print a simple table
                  .format(losses['textcat'], scores['textcat_p'],
                          scores['textcat_r'], scores['textcat_f']))

    def test_model(self, text_list):
        """
        Predict each text in the list.
        """
        for text in text_list:

            doc = self.nlp(text)
            print(doc.cats)
