import re
import spacy
import nltk
from nltk.corpus import stopwords

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']


def pre_process(paragraph):
    paragraph = re.sub('[^A-Za-z .-]+', ' ', paragraph)
    paragraph = ' '.join(paragraph.split())

    stopWords = stopwords.words('english')
    filtered = ' '.join([w for w in paragraph.split() if w not in stopWords])

    return filtered


def word_freq(paragraph):
    words = nltk.tokenize.word_tokenize(paragraph)
    dist = nltk.FreqDist(words)
    return dist


def get_noun(paragraph):

    dist = word_freq(paragraph)

    most_freq = [w for w,c in dist.most_common(10)
                 if nltk.pos_tag([w])[0][1] in NOUNS]

    filter_sent = nltk.sent_tokenize(paragraph)


    sentences = [nltk.word_tokenize(s) for s in filter_sent]
    sentences = [nltk.pos_tag(s) for s in sentences]
    return sentences


def split_sentences(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    sentences = [nltk.word_tokenize(w) for w in sentences]
    return sentences


def get_categories(paragraph):
    categories = []
    sentences = split_sentences(paragraph)
    sentences = [nltk.pos_tag(s) for s in sentences]

    for tagged_s in sentences:
        for chunks in nltk.ne_chunk(tagged_s):
            print(type(chunks))
            if type(chunks) == nltk.tree.Tree:
              categories.append(' '.join([c[0] for c in chunks]).lower())

    return categories



if __name__ == '__main__':
    text = 'I love swimming. This week has been crazy. Attached is my report on IBM. ' \
           'Can you give it a quick read and provide some feedback. ' \
           'Also, make sure you reach out to Claire (claire@xyz.com).You’re the best soccer. Cheers, George W. 212–555–1234'

    nlp = spacy.load("en_core_web_sm")
    sent = "Harry potter is my favorite character"
    doc = nlp(sent)
    for tok in doc:
        print(tok.dep_)

    sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj")]

    print(sub_toks)



