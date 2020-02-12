import textwrap
from datetime import datetime

import spacy
# from spacy.matcher import Matcher
from spacy.matcher.phrasematcher import PhraseMatcher
from spacy.tokens import Span
import json

_first_story_date = "2020-01-09"
_last_story_date = "2020-02-09"

nlp = spacy.load("en_core_web_sm")


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def read_guardian_articles():
    art = {}
    with open("guardianArticles.json", "r") as read_file:
        data = json.load(read_file)
    for k in data:
        spt = k.split('|')
        spt[0] = spt[0].strip()
        spt[1] = spt[1].strip()
        art[(spt[0], spt[1])] = data[k]
        # TODO convert spt[0] to date time
    return art


def get_article_as_text(ky, art_dict):
    first_art = art_dict[ky]['bodyHtml']
    first_art = "".join(first_art)
    first_art = remove_html_tags(first_art)
    return first_art


def on_match(matcher, doc, id, matches):
    print('Matched!', matches)


def match_doc_with_sentences(doc, matcher):
    """
    Runs a matcher against a doc and returns a new doc just for the matched sentences
    :param doc:
    :return:
    """
    debug = False
    matched_sentences = []
    matched_sents_keys = {}

    # Add the pattern to the matcher and apply the matcher to the doc
    # matcher.add("ADJ_NOUN_PATTERN", None, pattern)
    matches = matcher(doc)
    if debug:
        print("Total matches found:", len(matches))

    # Iterate over the matches and print the span text
    for match_id, start, end in matches:
        span = doc[start:end]  # Matched span
        sent = span.sent
        if sent in matched_sents_keys:
            continue
        matched_sents_keys[sent] = True
        matched_sentences.append(sent.text)
        if debug:
            print("Match found:", span.text)
            wrapper = textwrap.TextWrapper(width=100)
            word_list = wrapper.wrap(text=sent.text)
            for element in word_list:
                print(element)

    if len(matched_sentences) > 0:
        new_doc = nlp(" ".join(matched_sentences))
        return new_doc
    else:
        return None


def create_matcher(syns, label):
    disease_patterns = list(nlp.pipe(syns))
    # print("disease_patterns:", disease_patterns)
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add(label, None, *disease_patterns)
    return matcher


def get_sentences_from_doc(doc):
    if not doc:
        return []
    sents = []
    for s in doc.sents:
        sents.append(s.text)
    return sents


def search_article(article):
    # print(first_art)

    doc = nlp(article)

    disease_syns = ["coronavirus", "virus", "disease", ]
    disease_matcher = create_matcher(disease_syns, "DISEASE")

    death_syns = ['deaths', 'died', 'fatalities', 'deceased', 'killing']
    death_matcher = create_matcher(death_syns, "DEATHS")

    # Write a pattern for adjective plus one or two nouns
    # pattern = [{"POS": "ADJ"}, {"POS": "NOUN"}, {"POS": "NOUN", "OP": "?"}]

    docs_match_disease = match_doc_with_sentences(doc, disease_matcher)
    docs_match_disease_and_death = match_doc_with_sentences(docs_match_disease, death_matcher)

    if False and docs_match_disease:
        print(f"Sentences only matching the disease")
        sents = get_sentences_from_doc(docs_match_disease)
        for s in sents:
            print(f"\t{s}")

    if docs_match_disease_and_death:
        print(f"Sentences matching the disease & death")
        sents = get_sentences_from_doc(docs_match_disease_and_death)
        for s in sents:
            print(f"\t{s}")


art_dict = read_guardian_articles()

curr_dt = datetime.strptime(_first_story_date, '%Y-%m-%d')

for date, id in art_dict:
    # if date != curr_dt:
    #   continue
    print(f"{date} {id}")

first_art = get_article_as_text(
    ('2020-01-09 00:00:00', 'world/2020/jan/09/chinas-sars-like-illness-worries-health-experts'),
    art_dict)

c = 0
arts_to_search = 20
for k in art_dict:
    print(f"Searching: {k}")
    if c >= arts_to_search:
        break
    art_text = get_article_as_text(k, art_dict)
    search_article(art_text)
    c += 1
