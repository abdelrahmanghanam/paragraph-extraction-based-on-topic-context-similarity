# PDF paragraphs extraction based on a specified topic and headline generation for extracted topics.

This repo is divided into two sections, the GUI scripts and the notebook. The GUI scripts contain the GUI PyQt5 code and the code from notebook organized in scripts.



## Installation

To install the GUI version write the following command after activating your Python environment.

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md  
```

then to run navigate to "GUI" folder and type

```bash
python main.py
```

for the notebook just open and run all cells !
## Idea and usage
this code is for text analysis. basically, it takes a pdf file extracts paragraphs, after that the paragraphs are extracted based on its similarity to a specified topic, finally each paragraph is given a headline based on most important sentence in the extracted paragraph.

### 1. paragraph extraction 
in the beggining we need to take a pdf file, analyze it and extract paragraphs. the challenge here is that regular paragraphs has a '\n' as delimeter, but it is not the case in pdf files as it each line ends with '\n' so to overcome this issue I split all lines of the pdf file and used empty lines as an end to a praragraph.

### 2. similarity measure

Now it is time for paragraph extraction based on similarity to a specified topic context-based.
In this stage I had three approaches (simple, lazy, model-based)

#### a) simple: key word matching 
It is the most simple way by checking if that the topic sentence can be found inside the paragraph.
This is a simple way that has some drawbacks: - 
(it is not context based similarity 
it depends on the presence of the words inside a paragraph )
for example the research I am using is a study for sentiment analysis, so It is logical that data analysis topic is being discussed at most of the paragraphs, but It extracts 1 paragraph only.
#### b) lazy: using NLP library like Spacy 

In this approach I am using a NLP library spacy that has ready methods for comparing similaries between two texts depending on some factors, for example, searching for the same topic (data analysis), now it extracts 7 paragraphs (depending on the threshold I am providing that can be changed to add more or less paragraph),
but again it has some drawbacks like : (no customization available, no control on similarity measurement way)
#### c) cosine similarity:  using pre-built model for feature extraction 

This is the typical ML engineer approach is to build a model for feature extraction to get the context in considerstion and then using similarity measurement to measure similarity of topic features and paragraph features, here I used cosine similarity as a measurement tool for similarity, here I couldn't find a dataset to build a model for feature extraction, that is why I used pre-built model which is BERT model. from my point of view it is the best approach as (model can be costumised, context is considered, can control measurement tool).

### 3. Headline generation

### a) using the sentence that has most frequence words inside the paragraph

In this approach I need to do some preprocessing first as we depend on word occurence so I first need to remove numbers and special characters to avoid errors.

### b) using cosine similarity 
this approach is similar to the one I used at the beggining of that notebook, but here I am splitting paragraph sentneces, and compare similarity of each sentence to the whole paragraph, and then I use the most similar sentence as the headline.