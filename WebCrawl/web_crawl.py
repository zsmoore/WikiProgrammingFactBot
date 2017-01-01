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
        
        include = True
        #Filter out any disambiguations
        for test in soup.find_all('p'):
            test = str(test)
            if 'may refer to:' in test:
                #print(test)
                include = False
        
        #Only recurse on good links
        if include == True:
            dig_deeper(3, term)
                        

#Branch out deeper on wikipedia to a certain depth
def dig_deeper(remaining_levels, term):
    
    #No more recurses
    if remaining_levels == 0:
        return
    else:
        #do stuff
        dig_deeper(remaining_levels - 1, #next term)



def main():

    keys = get_keywords()
    create_graph(keys)
    


main()
