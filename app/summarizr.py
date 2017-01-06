import string
import nltk
import re
from nltk.tokenize import WhitespaceTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from collections import OrderedDict


def summarize(paragraph):
    paragraphs = re.split(r'\.(?=[a-zA-Z][^\.])', paragraph)
    summarized_paragraphs = []
    for para in paragraphs:
        tokenized_sentences = sentence_tokenize(para)
        para_length = len(tokenized_sentences)
        summarized_length = min(para_length, int(round(para_length / 3.0)))

        tokenized_words = tokenize_paragraph(tokenized_sentences)
        sent_freq_dists = get_freq_dist(tokenized_words)
        sent_scores = get_sent_scores(sent_freq_dists)

        summarized_sentences = []
        for i in xrange(0, summarized_length):
            summarized_sentences.append(sent_scores.popitem()[0])
        tokenized_sentences = [i for i in tokenized_sentences if i in summarized_sentences]
        summarized_paragraph = " ".join(tokenized_sentences)
        summarized_paragraphs.append(summarized_paragraph)
    return summarized_paragraphs


def sentence_tokenize(paragraph):
    extra_abbreviations = ['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e', 'm.a', 'b.a', 'ph.d']
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentence_tokenizer._params.abbrev_types.update(extra_abbreviations)

    sentences = sentence_tokenizer.tokenize(paragraph)
    return sentences


def tokenize_paragraph(sentences):
    stops = set(stopwords.words('english'))
    stops = [s.encode('ascii') for s in stops]

    tokenized_sentences = {sent: [w.lower().translate(None, string.punctuation)
                                  for w in WhitespaceTokenizer().tokenize(sent) if w.lower() not in stops]
                           for sent in sentences}
    return tokenized_sentences


def get_freq_dist(tokenized_sentences):
    return {sent: FreqDist(tokenized_sentences.get(sent)) for sent in tokenized_sentences.keys()}


def get_sent_scores(sent_freq_dists):
    sent_scores = {}
    for sent in sent_freq_dists.keys():
        score = 0
        for compare in sent_freq_dists.keys():
            if compare is not sent:
                score += get_intersection(sent_freq_dists.get(sent), sent_freq_dists.get(compare))
        sent_scores[sent] = score
    ordered_scores = OrderedDict(sorted(sent_scores.items(), key=lambda t: t[1], reverse=True))
    return ordered_scores


def get_intersection(freq1, freq2):
    score = 0
    normalized_length = (len(freq1) + len(freq2)) / 2
    intersection = freq1.viewkeys() & freq2.viewkeys()

    for val in intersection:
        score += (freq1.get(val) + freq2.get(val))
    return score / float(normalized_length)
