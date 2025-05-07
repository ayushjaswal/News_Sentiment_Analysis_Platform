import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import warnings
from News_Sentiment_Analysis.logging.logger import logging
import os


warnings.filterwarnings("ignore", category=UserWarning)

exclude = string.punctuation
stop_words = set(stopwords.words("english"))


class PredictionPipeline:
    def __init__(self):
        self.biases = {
            "pol_model": {
                "model_lstm": keras.models.load_model(
                    "./model/political_bias/model_pol_model_lstm_6.keras"
                ),
                "model_gru": keras.models.load_model(
                    "./model/political_bias/model_pol_model_gru_6.keras"
                ),
                "model_hybrid": keras.models.load_model(
                    "./model/political_bias/model_pol_model_hybrid_6.keras"
                ),
            },
            "sens_and_opin": {
                "model_lstm": keras.models.load_model(
                    "./model/sens_and_opinion/model_model_lstm.keras"
                )
            },
            "frame_model": {
                "model_lstm": keras.models.load_model(
                    "./model/framing_bias/model_model_lstm.keras"
                ),
                "model_gru": keras.models.load_model(
                    "./model/framing_bias/model_model_gru.keras"
                ),
                "model_hybrid": keras.models.load_model(
                    "./model/framing_bias/model_model_hybrid.keras"
                ),
            }
        }
        
        with open("./model/political_bias/tokenizer_pol_6.pkl", "rb") as file:
            political_tokenizer = pickle.load(file)
        with open("./model/framing_bias/tokenizer.pkl", "rb") as file:
            frame_tokenizer = pickle.load(file)
        with open("./model/sens_and_opinion/tokenizer.pkl", "rb") as file:
            sno_tokenizer = pickle.load(file)

        self.tokenizer = {
            "pol_model": political_tokenizer,
            "sens_and_opin": sno_tokenizer,
            "frame_model": frame_tokenizer
        }

        self.predictions  = {}

        self.max_lens = {"pol_model": 400, "sens_and_opin": 350, 'frame_model': 200}

        self.padding = {"pol_model": "pre", "sens_and_opin": "post", "frame_model": "post"}

        self.labels = {
            'pol_model': ['center', 'left', 'right'],
            'sens_and_opin': ['high', 'low'],
            'frame_model': ['negative', 'neutral', 'positive'],
        }

    def predict(self, text):
        for bias_name, bias_models in self.biases.items():
            predictions = []
            text_input = self.preprocess_text(bias_name, text)
            for model in bias_models.values():
                prediction = model.predict(text_input,verbose=0)
                predictions.append(prediction)
            predictions = np.array(predictions)
            soft_voted_predictions = np.mean(predictions, axis=0)
            predictions = np.argmax(soft_voted_predictions, axis=1)

            print(predictions)
            self.predictions[bias_name] = self.labels[bias_name][predictions[0]]
        return self.predictions

    def preprocess_text(self, model_name, text):
        tokenizer = self.tokenizer[model_name]

        # get cleaned text
        cleaned_text = self.clean_text(text.lower())

        # stem them to the root words
        stemmer = PorterStemmer()
        stemmed_text = " ".join([stemmer.stem(word) for word in cleaned_text.split()])

        # convert it to sequence using tokenizer and add padding
        sequence = tokenizer.texts_to_sequences([stemmed_text])
        # sequence = [idx for idx in sequence if tokenizer.num_words is None or idx < tokenizer.num_words]
        padded_sequence = pad_sequences(
            sequence, padding=self.padding[model_name], maxlen=self.max_lens[model_name]
        )
        return padded_sequence

    def clean_text(self, text):
        # removes urls
        text = re.sub(r"http\S+|www.\S+", "", text)

        # removes numbers
        text = re.sub(r"\d+", "", text)

        # removes punctuations
        text = text.translate(str.maketrans("", "", exclude))

        # remove stopwords
        text = self.remove_stopwords(text)

        return text

    def remove_stopwords(self, text):
        new_text = []
        for word in text.split():
            if word not in stop_words:
                new_text.append(word)
        return " ".join(new_text)


if __name__ == "__main__":
    pipeline = PredictionPipeline()
    text = "This past week, travellers in Rome may have spotted cardinals frequenting their favourite restaurants. Just before the last papal election in 2013, Italian media reported that many of these men were making the time to visit a particular neighbourhood favourite, Al Passetto di Borgo, a family-run eatery located 200m from Saint Peter's Basilica, where Cardinal Donald William Wuerl is known to order the lasagna and Francesco Coccopalmerio (allegedly the most-voted Italian cardinal in 2013) likes the grilled squid.Cardinals may feel some urgency to get in a good meal or two because, during the conclave beginning on 7 May, in which 135 cardinals will hold a secret election for a new pope in the Vatican's Sistine Chapel, they'll be entirely secluded from the rest of the world for an indefinite period of time. Voting, sleeping and eating all take place in tightly controlled sequestration."
    print(pipeline.predict(text))