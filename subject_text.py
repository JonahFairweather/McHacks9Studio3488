import re
import spacy
import nltk
from nltk.corpus import stopwords
from collections import Counter

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
ELIMINATE_VERBS = ['have', 'be', 'go', 'look', 'see', 'hear', 'smell', 'touch', 'gone', 'like', 'love', 'begin', 'think']

def pre_process(paragraph):
    paragraph = re.sub('[^A-Za-z .-]+', ' ', paragraph)
    paragraph = ' '.join(paragraph.split())

    stopWords = stopwords.words('english')
    filtered = ' '.join([w for w in paragraph.split() if w not in stopWords])

    return filtered


def word_freq(words):

    return Counter(words).most_common(1)


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


def get_entities(paragraph):
    categories = []
    sentences = split_sentences(paragraph)
    sentences = [nltk.pos_tag(s) for s in sentences]

    for tagged_s in sentences:
        for chunks in nltk.ne_chunk(tagged_s):
            print(type(chunks))
            if type(chunks) == nltk.tree.Tree:
              categories.append(' '.join([c[0] for c in chunks]).lower())

    return categories


def get_nouns(paragraph):

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)

    sub_toks = [tok.lemma_ for tok in doc
                if ((tok.dep_ == "nsubj" or tok.dep_ == "dobj" or tok.dep_ == "ROOT" or tok.dep_ == "pobj")
                    and (tok.pos_ == 'NOUN'))]

    return sub_toks


def get_actions(paragraph):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)

    sub_toks = [tok.lemma_ for tok in doc
                if (tok.dep_ == "attr" or tok.dep_ == "xcomp" or tok.dep_ == "ROOT" or tok.pos_ == 'VERB')]
    return sub_toks


def get_entities(paragraph):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)

    ents = [e.text for e in doc.ents]

    return ents


def get_tags(paragraph):

    paragraph = pre_process(paragraph)
    tags = get_nouns(paragraph)
    tags.append(get_actions(paragraph))
    tags.append(get_entities(paragraph))
    return tags


if __name__ == '__main__':
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Harry Potter is straight shit")

    text = "What do you mean? We outmatch you in firepower 10,000 to 1!" \
           "mhm, valid point, but you only need one ten-thousandth of your power to destroy yourself anyways..."\
           "What are you talking about?"\
           "See, earth, the only reason we survived so long was because of this little concept we knew as 'Mutually assured destruction.' Essentially meaning, if one fires, so too does the other."\
           "You would never be able to defend!"\
           "That's not the point, the point is if we both have the ability to kill each other, then it doesn't matter if you can't defend so long as you can react, and retaliate before their attack hits you. And believe me, we can react in time." \
            "The Ilerian paused. Thinking about what the pathetic human had said. he knew humans had nuclear armaments, and that they could destroy his species, but he had always thought that it didn't matter so long as they were more powerful."\
           "Our weapons should chill you to the bone, why do you act so confident in the face of death?" \
           "Because we've stared death in the face many times before. Humans are deadly, we've commit genocide on our own people multiple times. We've faced extinction, and planetary obliteration before, and never once did we back down. All this is is just another doomsday scenario that we will stare down until it either hits us, or back off."\
           "The Ilerian was taken aback by these words. He had heard that humans were vicious, but never expected them to be so cunning in the face of war."\
           "I... you can't possibly be serious. No species would drive themselves to the brink of extinction!"\
           "Kind of ironic, seeing as you're doing it right now, testing us. Who says we wont make the first move?"\
           "y-you wouldn't! We outgun you tenth-"\
           "so long as we can destroy your entire civilization, firepower hardly matters. Essentially, that makes us equal. So as your equal peer, i suggest you disarm those planet breakers, and we discuss peace."\
           "The Ilerian had ever heard someone speak of themselves as an equal to the Ilerian empire. They had outposts all over the quadrant, and this pathetic morsel thinks they can oppose him? But what if he wasn't bluffing? What if they did retaliate. They have the means and know-how to deploy untraceable warheads to every base they had. If the ilerians attacked first, would the humans be able to react in time?"\
           "uh... well then human... i- uhh, I guess we are in stalemate. I declare we never interact aga-"\
           "Oh no no, that's not how this works anymore. You just lost your chance to drop it and say that we never met, cause now I'm the one calling the shots. So here's my proposal. begin disarmament, and once you reach weapon equivalent to us, we too shall begin disarmament procedures. You will drop all of your trade barriers, and open your colonies to cultural exchange. If you don't I can assure you that neither of us will live to see the next galactic annum. Do we have a deal?"
    print(get_tags(text))









