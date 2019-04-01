import re


def generate_ngrams(review, n):
    """
    Generate n-grams from a review
    :param review: one single review
    :param n: the size of n gram
    :return: generated list of n-grams
    """
    sentences = review.split(".")
    n_grams = []
    for sentence in sentences:
        sections = sentence.split(",")
        for section in sections:
            parts = section.split(";")
            for part in parts:
                words = part.split()
                
                n_grams_temp = []    # the return list
                for i in range(len(words)):
                    temp = words[i]
                    for j in range(1, n):
                        if (i + j) < len(words):
                            temp = temp + ' ' + words[i + j]
                            n_grams.append(temp)
    return n_grams
