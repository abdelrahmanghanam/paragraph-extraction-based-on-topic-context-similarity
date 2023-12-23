import spacy
from transformers import BertTokenizer, BertModel
import torch


class Paragraphs_Filter:
    def extract_paragraphs_based_on_keywords(self,topic,paragraphs):
        #simple keyword matching
        relevant_paragraphs_keyword_matching = []
        for paragraph in paragraphs:
            if topic.lower() in paragraph.lower():
                relevant_paragraphs_keyword_matching.append(paragraph)
        return relevant_paragraphs_keyword_matching

    def extract_paragraphs_using_NLP(self,topic, paragraphs):
        #using NLP to mesaure similarity
        nlp = spacy.load("en_core_web_md")
        topic = nlp(topic)
        relevant_paragraphs_spacy = []
        for paragraph in paragraphs:
            paragraph_tokenized = nlp(paragraph)
            if paragraph_tokenized.similarity(topic) > 0.6:
                relevant_paragraphs_spacy.append(paragraph)
        return relevant_paragraphs_spacy

    def extract_paragraphs_features_cosine_similarity(self,topic, paragraphs):
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
        topic_embeddings = get_bert_embeddings(topic)
        relevant_paragraphs = []
        for paragraph in paragraphs:
            paragraph_embeddings = get_bert_embeddings(paragraph)
            similarity_matrix = compute_cosine_similarity(topic_embeddings, paragraph_embeddings)
            if similarity_matrix > 0.4:
                relevant_paragraphs.append(paragraph)
        return relevant_paragraphs


