from bs4 import BeautifulSoup
import requests


#Class with methods for relating keywords and finding common ground for subjects
class Relation:

    def __init__(self, relation_subject, base_url_for_terms):

        self.subject = relation_subject
        self.base_url = base_url_for_terms
        self.base_words = set()
        self.base_words_def_count = {}

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
            self.base_words.remove(word):
            del self.base_words_def_count[word]

    '''
        CURRENTLY HARDCODED - THIS IS BAD
    '''
    #Initializes class to have key words
    def initialize_keywords(self):

        req = requests.get(self.base_url)
        html = req.html
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
                keywords.append(key)
                      
        #Return start of terms to end of list
        return keywords[4:]


    #To String will print out what this object is relating
    def __str__(self):
        return self.subject
           
    
       
        
