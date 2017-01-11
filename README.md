# wikiSummarizr
A small [Flask](http://flask.pocoo.org/) web app that uses the Wikipedia Python [API](https://wikipedia.readthedocs.io/en/latest/) to naively summarize articles. Check it out [here](http://www.wikisummarizr.info).

## How it works
1. The content of the Wikipedia article is split into an ordered dictionary deliminated by the subheadings within the article
2. The [Natural Language Toolkit](http://www.nltk.org/) package is used to tokenize the sentences and then word tokenize each sentence
3. All forms of stopwords and abbreviations are cleansed from the text
3. `nltk.probabilty.freqDist` is used to calculate the frequency distribution of words in each sentence of the paragraph
4. The frequency distributions are used to calculate the number of intersections a sentence has with all other sentences in the paragraph. An intersection occurs when a word appears at least once in both sentences. This cumulative intersection score is normalized by the average length of both sentences: `score =  score / (float((len(freq1) + len(freq2) / 2))`
5. This is repeated for each sentence in the paragraph, creating a dictionary of sentences to scores
6. This dictionary of sentences to scores helps determine which sentences are more redundant. i.e. The higher the score, the more redundant the sentence, as it has the greater number of intersections with other sentences
7. A subset with length based on the size of the original paragraph of the lowest scoring sentences is created. This subset is concatenated to form the final summarized paragraph
8. Lather rinse and repeat for all other paragraphs and sections in the article

## Running locally
* After downloading the repo to your local machine, install the requirements by running `pip install -r requirements.txt` (I recommend creating a virtual environment using venv)
* Change line 11 in `app/summarizr.py` to the location of actual location of the corpora and tokenizers directory on your machine (current is defaulted to Heroku environment)
* Run the application with `python run.py` the app should now be running on `127.0.0.1:5000`

## To-Do
* Add support for special symbols (such as mathematic, Greek letters)
* Add corpora path as a variable in config.py
* Support for stemming and lemmatization
