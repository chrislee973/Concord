import nltk
import re
import pdfplumber
import gensim.downloader as api

class text_file:
    def __init__(self, fpath):
        with open(fpath) as f:
            text = f.read()

        self.fname = fpath.split('/')[-1]
        self.text = re.sub('[\n]', ' ', text)
        self.sents = nltk.sent_tokenize(self.text)

    def get_sents(self, query=None):
        '''
        Takes in list of query(s) taken from Text widget and returns list of sentences that contain the specified keyword or keywords
        '''
        query = query
        query_set = set([key.lower().strip() for key in query.split(',')])
        query_sents = []
        # Iterate through the sentences and return those that contain the keyword
        for sent in self.sents:
            # Word-tokenize each sentence and check if the set of keyword(s) is contained in the set of tokens for that sentence
            if query_set <= set(nltk.word_tokenize(sent.lower())):
                query_sents.append(sent)
        return query_sents


class Pdf:
  def __init__(self, filepath):
    with pdfplumber.open(filepath) as pdf:
      num_pages = len(pdf.pages)
      valid_pages = [pdf.pages[i] for i in range(num_pages) if pdf.pages[i].extract_text() is not None]

    self.name = filepath.split('/')[-1]
    self.num_pages = num_pages
    self.valid_pages = valid_pages
    self.text=''
    for page in self.valid_pages:
      self.text += page.extract_text()

    self.text = re.sub('[\n]', '', self.text)
    self.sents = nltk.sent_tokenize(self.text)


  def get_sents(self, query = None):
      '''
      Takes in list of query(s) taken from Text widget and returns list of sentences that contain the specified keyword or keywords
      '''
      query = query
      query_set = set([key.lower().strip() for key in query.split(',')])
      query_sents = []
      #Iterate through the sentences and return those that contain the keyword
      for sent in self.sents:
        #Word-tokenize each sentence and check if the set of keyword(s) is contained in the set of tokens for that sentence
        if query_set <= set(nltk.word_tokenize(sent.lower())):
          query_sents.append(sent)
      return query_sents

class word2vec:
    def __init__(self):
        self.wv = api.load('word2vec-google-news-300')

    def topn_sims(self, query = None, n = None):
        '''
        Returns the top n similar words as the query
        '''

        return self.wv.most_similar(positive = query, topn = n)


