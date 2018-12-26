import json
import nltk
import pandas
import numpy
import math
import random
import os

nltk.data.path.append(os.getcwd())


def clean_token_list(token_list):
    cleaned_list = []
    filter_terms = ["http", "&amp;", "-", "&gt;"]

    for token in token_list:
        add = True
        for filter_term in filter_terms:
            if filter_term in token:
                add = False
                break

        if add:
            trimmed_token = token.replace("\"", "")
            cleaned_list.append(trimmed_token)

    return cleaned_list


def generate_model(cfd_obj, start_word, num=100):
    joined_string = ""
    prec_word = ""
    common_prec_words = ["and", "a", "A", "am", "have", "very", "big", "as", "favorite"]

    for i in range(num):
        joined_string = joined_string + " " + start_word

        if i > 50:
            current_pos = nltk.pos_tag([start_word])
            pos = ""
            try:
                pos = current_pos[0][1]
            except:
                pass

            excluded_pos_list = ["PRP", "CC", "IN"]
            excluded_end_word_list = ["a", "your", "the", "my", "who", "to", "very"]

            if pos not in excluded_pos_list and start_word not in excluded_end_word_list:
                joined_string = joined_string + "."
                break

        start_word_freq_dict = cfd_obj[start_word]

        freq_dist_aslist = []
        for key, value in start_word_freq_dict.items():
            freq = [key, value]
            freq_dist_aslist.append(freq)

        df_wordlist = pandas.DataFrame(freq_dist_aslist, columns=['Word', 'Freq'])
        df_wordlist = df_wordlist.sort_values(by="Freq", ascending=False)
        df_as_list = df_wordlist.values.tolist()

        max_sample_range = math.ceil(len(df_as_list) / 2)

        if len(df_as_list) == 1:
            sample_index = 0
        elif start_word in common_prec_words:
            sample_index = math.ceil(numpy.random.gamma(3, 3, 1))
        else:
            sample_type_randomizer = random.random()

            # 10% probability to sample deeper into bi-grams occurrence to increase randomness,
            # 90% probability to sample more coherent text
            if sample_type_randomizer < 0.2:
                sample_index = math.ceil(numpy.random.gamma(3, 3, 1))
            else:
                sample_index = math.ceil(numpy.random.gamma(1, 2, 1) * 0.6)

            if sample_index > max_sample_range:
                sample_index = max_sample_range

        start_word = df_as_list[sample_index][0]

    return joined_string


def build_tweet(subject):
    with open("tweets.json", encoding="utf-8") as file:
        data = json.load(file)

    tweet_bodies = [x["text"] for x in data if x["is_retweet"] == False]

    corpus = (' '.join(filter(None, tweet_bodies)))
    token_list = corpus.split(" ")
    token_list_cleaned = clean_token_list(token_list)

    bigrams = nltk.bigrams(token_list_cleaned)
    cfd = nltk.ConditionalFreqDist(bigrams)

    tweet = generate_model(cfd, subject)
    tweet = tweet\
        .replace("  ", " ")\
        .replace("\"", "")\
        .replace(" i ", " I ")
    tweet = tweet.lstrip(" ")
    tweet = "\"" + tweet + "\""

    return tweet
