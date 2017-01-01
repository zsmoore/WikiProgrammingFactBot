from bs4 import BeautifulSoup
import requests
import pprint
import ./relation.py

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



#Main
def main():
    
    #Grab arguments
    subject = sys.argv[1]
    base_url = sys.argv[2]

    base_obj = Relation(subject, base_url)
    keys = get_keywords(base_obj)
    create_graph(keys)


#Main will run if nothing else specified
if __name__ == "__main__":
    main()


