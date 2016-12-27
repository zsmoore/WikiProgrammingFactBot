from bs4 import BeautifulSoup
import requests
import pprint

#Pull from website that has key comp sci terms
def get_keywords():

    #Set up site scrape
    keywords = []
    keyword_url = 'http://www.labautopedia.org/mw/List_of_programming_and_computer_science_terms'
    keyword_page = requests.get(keyword_url)
    html = keyword_page.content
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

#Based on KeyWords start building web graph of programming terms
def create_graph(keywords):

    #Base url
    base = 'https://en.wikipedia.org/wiki/'
    
    #For each key term
    for word in keywords:
        
        #Build new urls and get html request
        full = base + word
        req = requests.get(full)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')
        
        #Filter out any disambiguations
        for test in soup.find_all('p'):
            test = str(test)
            if 'may refer to:' in test:
                print(test)

def main():

    keys = get_keywords()
    create_graph(keys)
    


main()
