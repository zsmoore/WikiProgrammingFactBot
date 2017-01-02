from bs4 import BeautifulSoup
import requests
import pprint
import nltk
from nltk.corpus import stopwords
from nltk.stem.api import StemmerI

#Class with methods for relating keywords and finding common ground for subjects
class Relation:

    def __init__(self, relation_subject, base_url_for_terms):

        self.subject = relation_subject
        self.base_url = base_url_for_terms
        self.base_words = set()
        self.base_words_def_count = {}
        self.stemmed = {}

    #Add new Key word into class
    def add_key(self, word):
        
        if word not in self.base_words:
            self.base_words.add(word)
        
        if word not in self.base_words_def_count:
            self.base_words_def_count[word] = 1

    #Remove Key word from class
    def remove_key(self, word):
        
        #Exception handling needed
        if word not in self.base_words_def_count:
            print('word not in class')

        else:
            self.base_words.remove(word)
            del self.base_words_def_count[word]

    '''
        CURRENTLY HARDCODED - THIS IS BAD
    '''
    #Initializes class to have key words
    def initialize_keywords(self):

        req = requests.get(self.base_url)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')

        #For each term on website
        for key in soup.find_all('b'):
            
            #Format string
            key = str(key).split('>')[1].split('<')[0].strip().strip('-')
            key = key.replace(' ', '_')
                
            #Break if at end of key term list
            if key == 'Bold.':
                break
            else:
                if key == '' or key == ' ':
                    continue
                self.add_key(key)
    
    #Algo to relate key words
    def relate_keys(self):
        
        self.grab_defs()
        self.remove_outliers()
        self.stem_relate()
        pprint.pprint(self.stemmed)
        print(len(self.stemmed.keys()))
        #pprint.pprint(self.base_words_def_count)
        #print(len(self.base_words_def_count.keys()))

    #MAYBE BUILDING TRIE IS BETTER?
    def build_trie(self):

        trie = {}
        for word in self.base_words_def_count.keys():
            for i in range(len(word)):
                pass
                


    #Get stems of words and sum them
    def stem_relate(self):
        
        x = nltk.stem.SnowballStemmer('english')
        for word in self.base_words_def_count.keys():
            stem = x.stem(word)
            if stem not in self.stemmed:
                self.stemmed[stem] = self.base_words_def_count[word]
            else:
                self.stemmed[stem] += self.base_words_def_count[word]


    #Remove outliers from word count in order to remove common language
    def remove_outliers(self):
        
        #Get keys that arent common word
        s = set(stopwords.words('english'))
        filtered = filter(lambda w: not w in s, list(self.base_words_def_count.keys()))
        filtered = set(filtered)
        
        #Make dict = difference of dict and filtered
        for word in set(self.base_words_def_count.keys()) - filtered:
            del self.base_words_def_count[word]

    #Grabs definitions for key words 
    def grab_defs(self):
        
        req = requests.get(self.base_url)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')

        #For each key-definition
        for entry in soup.find_all('li'):
            #Remove the key word to keep the definition
            if entry.find('b'):
                remove = entry.find('b')
                remove.extract()
                
                #Get rid of html tags
                entry = str(entry).split('>')[1].split('<')[0].strip().strip('-')
                
                #For each word in definition
                for word in entry.split():
                    
                    #Strip away commas, periods, quotes
                    word = word.strip().strip(',').strip('.').strip('\'').strip('\"').strip('(').strip(')').strip('_')
                    
                    #Get rid of parenthesis
                    if word.startswith('('):
                        word = word.split('(')[1].split(')')[0]
                    
                    #Make lower case
                    word = word.lower()

                    '''

                        Weird formatting stuff needs to be cleaned up 
                    
                    '''
                    #If dash in word add full word and split
                    if len(word.split('-')) > 1:
                        
                        #If not in dict initialize and add if in dict add
                        temp_split = word.split('-')
                        for sub_word in temp_split:
                            if sub_word not in self.base_words_def_count:
                                self.base_words_def_count[sub_word] = 1
                            else:
                                self.base_words_def_count[sub_word] += 1

                        if word not in self.base_words_def_count:
                            self.base_words_def_count[word] = 1
                        else:
                            self.base_words_def_count[word] += 1

                    #If underscore in word add full word and split
                    if len(word.split('_')) > 1:
                        
                        #If not in dict initialize and add if in dict add
                        temp_split = word.split('_')
                        for sub_word in temp_split:
                            if sub_word not in self.base_words_def_count:
                                self.base_words_def_count[sub_word] = 1
                            else:
                                self.base_words_def_count[sub_word] += 1

                        if word not in self.base_words_def_count:
                            self.base_words_def_count[word] = 1
                        else:
                            self.base_words_def_count[word] += 1
 
                    #If parenthesis in word add full word and split
                    if len(word.split('(')) > 1:
                        
                        #If not in dict initialize and add if in dict add
                        temp_split = word.split('(')
                        for sub_word in temp_split:
                            if sub_word not in self.base_words_def_count:
                                self.base_words_def_count[sub_word] = 1
                            else:
                                self.base_words_def_count[sub_word] += 1

                        if word not in self.base_words_def_count:
                            self.base_words_def_count[word] = 1
                        else:
                            self.base_words_def_count[word] += 1
 

                    #If split not needed
                    else:
                        #Add to dict
                        if word not in self.base_words_def_count:
                            self.base_words_def_count[word] = 1
                        else:
                            self.base_words_def_count[word] += 1


    #Return base words
    def get_base_words(self):
        return self.base_words

    #Return definition word count dict
    def get_base_word_def_count(self):
        return self.base_words_def_count

    #Return stemmed summed words dict
    def get_stemmed(self):
        return self.stemmed
    #To String will print out what this object is relating
    def __str__(self):
        return self.subject
