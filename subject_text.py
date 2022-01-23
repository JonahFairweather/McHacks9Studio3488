import re
import spacy
import nltk
from nltk.corpus import stopwords
from collections import Counter
import pickle
import reddit_scrape

f = open('lexicon.pkl','rb')
LEXICON = pickle.load(f)
f.close()

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
ELIMINATE_VERBS = ['have', 'be', 'go', 'look', 'see', 'hear', 'smell', 'touch', 'gone', 'like', 'love', 'begin',
                   'think', 'say', 'make', 'mean', 'do']
ELIMINATE_LABELS = ['CARDINAL','ORDINAL','QUANTITY','MONEY', 'PERCENT', 'TIME','DATE', 'PERSON', 'NORP']


def pre_process(paragraph):
    paragraph = re.sub('[^A-Za-z .-]+', ' ', paragraph)
    paragraph = ' '.join(paragraph.split())

    stopWords = stopwords.words('english')
    filtered = ' '.join([w for w in paragraph.split() if (w not in stopWords and 'thing' not in w and len(w) > 2)])

    return filtered


def word_freq(words):

    return Counter(words).most_common(1)


def split_sentences(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    sentences = [nltk.word_tokenize(w) for w in sentences]
    return sentences


def get_nouns(paragraph):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)

    sub_toks = [tok.lemma_.lower() for tok in doc
                if ((tok.dep_ == "nsubj" or tok.dep_ == "dobj" or tok.dep_ == "ROOT" or tok.dep_ == "pobj"
                     or tok.dep_ == "attr" or tok.dep_ == "xcomp")
                    and (tok.pos_ == 'NOUN'))]

    nouns_lexicon = []
    nouns_not_lexicon = []

    for noun in sub_toks:
        if noun in LEXICON:
            nouns_lexicon.append(noun)
        else:
            nouns_not_lexicon.append(noun)
    all_nouns = []

    all_nouns.append(nouns_lexicon)
    all_nouns.append(nouns_not_lexicon)
    return all_nouns


def get_verbs(paragraph):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)

    sub_toks = [tok for tok in doc
                if (tok.pos_ == 'VERB')]
    good_verbs = []
    # removing verbs with no real meaning about the text
    for index,verbs in enumerate(sub_toks):
        if verbs.pos_ == 'VERB':
            indirect_object = False
            direct_object = False
        for obj in verbs.children:
            if obj.dep_ == "iobj" or obj.dep_ == "pobj":
                indirect_object = True
            if obj.dep_ == "dobj" or obj.dep_ == "dative":
                direct_object = True
        # We do not want ditransitive verbs
        if not(indirect_object and direct_object):
                good_verbs.append(verbs.lemma_)

    for verb in good_verbs:
        if verb in ELIMINATE_VERBS:
            good_verbs.remove(verb)

    sub_toks = []

    for verb in good_verbs:
       if verb in LEXICON:
            sub_toks.append(verb)


    return sub_toks


def get_entities(paragraph):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)

    k = doc.ents
    ents = [e.text.lower() for e in doc.ents if e.label_ not in ELIMINATE_LABELS]

    return ents


def get_relevant_words(paragraph):
    tags = []
    #tags.append(get_verbs(paragraph))
    paragraph = pre_process(paragraph)
    nouns = get_nouns(paragraph)
    tags.append(nouns[0])
    tags.append(nouns[1])
    tags.append(get_entities(paragraph))

    return tags

def get_popular(paragraph):
    top = []
    tags = get_relevant_words(paragraph)
    for types in tags:
        top.extend(Counter(types).most_common(3))
    return top

def get_web_tags(paragraph):
    tags = []
    popular = get_popular(paragraph)
    for tuple in popular:
        tags.append(tuple[0])
    return tags

if __name__ == '__main__':

    lol = reddit_scrape.extract_comments()

    print(get_web_tags(lol))











