import re
import spacy
import nltk
from nltk.corpus import stopwords
from collections import Counter

NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
ELIMINATE_VERBS = ['have', 'be', 'go', 'look', 'see', 'hear', 'smell', 'touch', 'gone', 'like', 'love', 'begin',
                   'think', 'say', 'make', 'mean']

def pre_process(paragraph):
    paragraph = re.sub('[^A-Za-z .-]+', ' ', paragraph)
    paragraph = ' '.join(paragraph.split())

    stopWords = stopwords.words('english')
    filtered = ' '.join([w for w in paragraph.split() if w not in stopWords])

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

    return sub_toks


def get_verbs(paragraph):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)

    sub_toks = [tok for tok in doc
                if (tok.pos_ == 'VERB')]

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
        if indirect_object and direct_object:
            sub_toks.remove(verbs)
        else:
            sub_toks[index] = verbs.lemma_

    for verb in sub_toks:
        if verb in ELIMINATE_VERBS:
            sub_toks.remove(verb)
    return sub_toks


def get_entities(paragraph):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(paragraph)
    ents = [e.text.lower() for e in doc.ents]

    return ents


def get_tags(paragraph):
    tags = []
    tags.append(get_verbs(paragraph))
    paragraph = pre_process(paragraph)
    tags.append(get_nouns(paragraph))
    tags.append(get_entities(paragraph))
    return tags

def get_popular(paragraph):
    top3 = []
    tags = get_tags(paragraph)
    for types in tags:
        top3.append(Counter(types).most_common(3))
    return top3



if __name__ == '__main__':
    text = 'The majority of galactic species evolved as hive mind,' \
           ' the professor\'s voice rung throughout the metallic lecture hall, though only a few hundred of the thousands of students were physically present, the rest would be catching the beam. As a pie chart appeared on the vision boards the professor continued, "another sizeable portion evolved from pack dynamics apex predators. It is estimated that as few as half a percent of galactic civilizations developed interstellar technology from a tribal civilization." The professor raised a finger, and the smallest slice of the pie possible became highlighted, "even among that particular subset, only one emerged from a tribal civilization where the dominant tribe wasn\'t fully determined before the initial attempts at spacefaring were made.'\
    'The vision boards changed, but the professor lowered his hand and they went momentarily dark, "before we continue, consider that point. For every civilization other than humanity, there is a singular, inescapable, gap - their warfighting capability, tactics, and motives, go utterly dormant and unchanged from at least the advent of spacefaring to their arrival on the interstellar stage, for most far longer than that. The hive minds can\'t imagine dealing with an equal being, the apex predators have never been hunted, even the very few tribal species haven\'t dealt with others on equal footing since times barely preserved as legend. Is it any wonder their solutions to conflict have been rudimentary, and swift? None had needed anything resembling either war or diplomacy in most of their evolutionary history.'\
           'The boards lit up again, images famous in the human diaspora. The first battle of the twin stars, when the Canim fleet had come to eradicate humanities expansion into their sector. A ring of gleaming warships, whose FTL technology was primitive in comparison, but loaded with weapons the dogs had never imagined. Weapons honed from centuries of intersystem war, "There were three hundred and forty two nations on earth when the Admiral Parry entered FTL bound for Alpha Centauri. There are three hundred and thirty six today. Humanity never stopped learning how to fight. With the pieces we pulled out of the wreckage of the first Canim battle fleet our FTL reached parity fairly quickly."'\
           'Another image, ships of similar design, but sleeker, newer, lighting fusion candles as they pulled away from the shining blue marble of earth in the distance, "the Admiral Perry may have been named similar to its predecessor, but it served a different purpose. An attempt was made to close the galaxy to us. Those ships went forth to kick it open."'\
           'final image, the standard of Earth, a blue marble on a field of black originally marking a single system growing to take a sizeable chunk of the local arm of the milky may. A war to end all wars, a war of dominance. Humans had learned a few things about diplomacy in its history, yes - but it had also learned how to deal with predators below it on the food chain. Humans were an odd sort of apex predator, but they were not any less of one.'

    print(get_popular(text))










