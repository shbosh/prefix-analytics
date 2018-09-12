#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The simplest TF-IDF library imaginable.
Add your documents as two-element lists
`[docname, [list_of_words_in_the_document]]` with
`addDocument(docname, list_of_words)`. Get a list of all the
`[docname, similarity_score]` pairs relative to a document by calling
`similarities([list_of_words])`.
See the README for a usage example.
"""
import math



class tfidf:
  documents = []


  def add_document(self, doc_name, list_of_words):
    """ Adds a new document to a collection of documents """

    # Build dictionary like 'word : frequency'
    doc_dict = {}
    for word in list_of_words:
      doc_dict[word] = doc_dict.get(word, 1.)

    # Add the normalized document to the other documents
    self.documents.append([doc_name, doc_dict])


  def _tf(self, word, doc_dict):
    """ To calculate tf (term frequency) """

    # All words in the document
    words = doc_dict.keys()

    if len(words) == 0:
        return 0.0

    return words.count(word) / float(len(words))


  def _idf(self, word):
    """ To calculate idf (inverse document frequency) """

    D = float(len(self.documents))
    Q = sum(1 for doc in self.documents if word in doc[1])
    if Q != 0:
        return math.log10(D / Q)
    return 0.0


  def similarities(self, list_of_words):
    """
    Get the score for a list of words
    the importance of a set of documents
    """

    # Returns a list in the form of '[['foo', 0.13], ['bar', 0.0]]'
    similarities = []

    for document in self.documents:
      doc_name, doc_dict = document

      tf_idf = 0.0

      # Calculate the tf-idf for all words in the current document
      for word in list_of_words:
        tf_idf += self._tf(word, doc_dict) * self._idf(word)

      similarities.append([doc_name, tf_idf])

    # Return the list of words in the documents of evaluation
    return similarities
