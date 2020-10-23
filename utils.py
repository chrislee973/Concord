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
        Takes in a query and returns list of sentences that contain the specified keyword or keywords
        '''
        query = query.lower().strip()
        #query_set = set([key.lower().strip() for key in query.split(',')])
        query_sents = []
        # Iterate through the sentences and return those that contain the keyword
        for sent in self.sents:
            # Word-tokenize each sentence and check if the set of keyword(s) is contained in the set of tokens for that sentence
            if query in set(nltk.word_tokenize(sent.lower())):
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
      Takes in query and returns list of sentences that contain the specified keyword or keywords
      '''
      query = query.lower().strip()
      #query_set = set([key.lower().strip() for key in query.split(',')])
      query_sents = []
      #Iterate through the sentences and return those that contain the keyword
      for sent in self.sents:
        #Word-tokenize each sentence and check if the set of keyword(s) is contained in the set of tokens for that sentence
        if query in set(nltk.word_tokenize(sent.lower())):
          query_sents.append(sent)
      return query_sents


def load_word2vec():
    return api.load("word2vec-google-news-300")


def retrieve(files, query, pdf_obj, txt_obj):
    '''

    Input: files - List of file names
           query - query to search against the files
           pdf_obj - dictionary of processed pdf objects chosen by user
           txt_obj - dictionary of processed text files chosen by user

    Output: output_sents_zipped - a zipped list which will contain all output sentences
                                along with corresponding index telling which file they belong in

            num_sents_found- the total number of sentences retrieved
    '''

    # Initialize output_sents_zipped
    output_sents_zipped = []

    # Initialize num_sents_found and output_sents
    num_sents_found = 0
    output_sents = []


    for i, file in enumerate(files):
        if file.endswith('.pdf'):
            pdf = pdf_obj[file]
            output_sents = pdf.get_sents(query)
            num_sents_found += len(output_sents)

            output_sents_zipped += list(zip([i] * num_sents_found, output_sents))

        elif file.endswith('.txt'):
            txt = txt_obj[file]
            output_sents = txt.get_sents(query)
            num_sents_found += len(output_sents)

            output_sents_zipped += list(zip([i] * num_sents_found, output_sents))

    return output_sents_zipped, num_sents_found


def print_output_sents(output_sents_zipped, files, background_colors = None, cprint = None):
    '''
    Prints color-coded results to output box

    Input: output_sents_zipped - a zipped list of sentences with their document index
           files - list of all files chosen by usercolor
           background-colors - list of colors with which to color-code each sentence
    '''

    for i, sent in output_sents_zipped:
        #If only 1 file chosen, no need to color-code
        if len(files) == 1:
            cprint(sent, end='\n\n')
        else:
            #If multiple files chosen, color-code them
            cprint(sent, background_color=background_colors[i], end='\n\n')
