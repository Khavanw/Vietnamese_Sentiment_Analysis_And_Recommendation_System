#  [PhoBERT Fine-tuning & Recommendation] Vietnamese_Sentiment_Analysis_And_Recommendation_System

## Overview
This system combines advanced natural language processing techniques for sentiment analysis on Vietnamese text. Additionally, it integrates a content-based recommendation system to enhance user experience.

### PhoBERT Fine-tuning:
- Uses PhoBERT, fine-tuned specifically for Vietnamese sentiment analysis tasks.
- Optimized for real-world Vietnamese datasets.

### Recommendation:
- Content-based Filtering recommendation engine.
- Context-aware filtering logic prioritizing factors like sentiment, user ratings, and technical specifications.

### Workflow:

![WorkFlow](assets/workflow.png)

## Method

### 1. PhoBERT Fine-tuning
We use the best model from the AIViVN's competition by [Khoi Nguyen](https://github.com/suicao). The model scored 0.90849 on the public leaderboard

#### Model architecture
Here we created a custom classification head on top of the BERT backbone. We concatenated the last 4 hidden representations of the ```[CLS]``` token, which is actually ```<s>``` in this case, and fed it to a simple MLP.

![](https://i.imgur.com/1bYD5dq.png)

### 2. Recommendation System
The recommendation system uses content-based filtering with:
- Weighted features: sentiment (25%), user ratings (15%), and technical specifications (35%).
- Tools: TensorFlow, Hugging Face.

![](assets/Recommendation.png)
## Dataset
### Data Collection
Data is scraped from the website: Thế Giới Di Động using automation tools:
- **Framework**: selenium, BeautifulSoup
- Scripts:
  - ```scrape\crawl_links.py```
  - ```scrape\crawl_reviews_rating.py```


## Setup model traning

### Data preprocessing
Using dataset preprcessing:
```function\Data_preprocessing.py```

### Installing VnCoreNLP

Install the python bindings:

```$pip install  vncorenlp```

Clone the VNCoreNLP repo: https://github.com/vncorenlp/VnCoreNLP

### Downloading PhoBERT 

Follow the instructions in the original repo:

PhoBERT-base:

```
$wget https://public.vinai.io/PhoBERT_base_transformers.tar.gz
$tar -xzvf PhoBERT_base_transformers.tar.gz
```
## Experiments Results
### 1. Model Performance
PhoBERT Fine-tuning achieved excellent results in fold 4 after 20 epochs:
- **AUC**: A score close to 1 indicates strong discrimination between classes.
- **F1 Score**: A score of 0.8 reflects a good balance between precision and recall.

## Result Classification report and confussion matrix
- PhoBERT Fine-tuning:

<p align="center">
  <img src="assets/Evaluate.png"><br/>
</p>

## DEMO


  

