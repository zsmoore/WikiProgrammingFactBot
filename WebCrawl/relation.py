from bs4 import BeautifulSoup
import requests
import pprint

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
        pprint.pprint(self.base_words_def_count)

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
                    word = word.strip().strip(',').strip('.').strip('\'').strip('\"')
                    
                    #Get rid of parenthesis
                    if word.startswith('('):
                        word = word.split('(')[1].split(')')[0]
                    
                    #Make lower case
                    word = word.lower()

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

    #To String will print out what this object is relating
    def __str__(self):
        return self.subject
           
    
       
        
