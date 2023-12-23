# extractive summary by word count in each sentence
import spacy
import re
import torch
from transformers import BertTokenizer, BertModel
from nltk.tokenize import sent_tokenize
class Headline_Generator:

    def generate_headlines_using_word_occurence(self, paragraphs):
        nlp = spacy.load("en_core_web_md")
        relevant_paragraphs_with_occurence = []
        for paragraph in paragraphs:
            # preprocess
            # match all digits in the string and replace them with an empty string
            processed_feature = re.sub(r'[0-9]+', '', paragraph)
            # remove all the special characters
            processed_feature = re.sub(r'\W', ' ', processed_feature)
            doc = nlp(processed_feature)
            word_dict = {}
            # loop through every sentence and give it a weight
            for word in doc:
                word = word.text.lower()
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1
            # list of tuple (sentence text, score, index)
            sents = []
            sent_score = 0
            for index, sent in enumerate(doc.sents):
                for word in sent:
                    word = word.text.lower()
                    sent_score += word_dict[word]
                sents.append((sent.text.replace("\n", " "), sent_score / len(sent), index))
            # sort sentence by word occurrences
            sents = sorted(sents, key=lambda x: -x[1])
            # summarize in 3 sentences
            sents = sorted(sents[:3], key=lambda x: x[2])

            # compile them into text
            headline = sents[0][0]
            relevant_paragraphs_with_occurence.append({"headline": headline, "paragraph": paragraph})
        return relevant_paragraphs_with_occurence

    def generate_headlines_using_cosine_similarity(self, paragraphs):

        # using bert model
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')
        def get_bert_embeddings(text):
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=50,
                               add_special_tokens=True)
            outputs = model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)  # using mean pooling for sentence embeddings
            return embeddings
        # this is for vector cosine similarity
        def compute_cosine_similarity(embeddings1, embeddings2):
            similarity = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)
            return similarity.item()


        relevant_paragraphs_with_topics_similarity = []
        for paragraph in paragraphs:
            sentences = sent_tokenize(paragraph)
            headline = ""
            headline_similarity = 0
            for sentence in sentences:
                # match all digits in the string and replace them with an empty string
                sentence = re.sub(r'[0-9]+', '', sentence)
                # remove all the special characters
                sentence = re.sub(r'\W', ' ', sentence)
                headline_embeddings = get_bert_embeddings(sentence)
                text_embeddings = get_bert_embeddings(paragraph)
                similarity = compute_cosine_similarity(headline_embeddings, text_embeddings)
                if similarity > headline_similarity:
                    # most similar sentence
                    headline_similarity = similarity
                    headline = sentence
            relevant_paragraphs_with_topics_similarity.append({"headline": headline, "paragraph": paragraph})
        return relevant_paragraphs_with_topics_similarity
