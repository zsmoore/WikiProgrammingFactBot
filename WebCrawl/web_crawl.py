from bs4 import BeautifulSoup
import requests
import pprint
from relation import Relation
import json

#Based on KeyWords start building web graph of programming terms
def create_graph(relation_obj):

    #Base graph to be json dumped
    graph = {}
    visited = set()

    #Base url
    base = 'https://en.wikipedia.org/wiki/'
    
    #For each key term
    for word in relation_obj.get_base_words():
       
        #Build new urls and get html request
        full = base + word
        req = requests.get(full)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')
        
        include = True
        #Should be a single div so no long looping
        for div in soup.find_all('div', {'id':'bodyContent'}):
            #Filter out any disambiguations
            for test in div.find_all('p'):
                test = str(test)
                if 'may refer to:' in test:
                    #print(test)
                    include = False
            
            #Only recurse on good links
            if include == True:
                print(word)
                visited.add('/wiki/' + word)
                dig_deeper(3, '/wiki/' + word, graph, visited)

    #Dump subject's graph to json
    with open(str(relation_obj) + '.json', 'w') as fp:
        json.dump(graph, fp)
                        

#Branch out deeper on wikipedia to a certain depth
def dig_deeper(remaining_levels, term, graph, visited):
    
    #No more recurses
    if remaining_levels == 0:
        return
    else:
        
        print(remaining_levels, term)
        #initialize term in graph to a set    
        if term not in graph:
            graph[term] = set()

        #Base url for requests
        base = 'https://en.wikipedia.org/'
        
        #Get request
        full = base + term
        req = requests.get(full)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')

        #Should be a single div not a long loop
        for div in soup.find_all('div', {'id':'bodyContent'}):
            #If at disambiguation consider end node and exit recursion
            for test in div.find_all('p'):
                test = str(test)
                if 'may refer to:' in test:
                    return

            #Get all connections
            for link in div.find_all('a'):
                inner_link = link.get('href')
                
                #Check for Nones
                if not isinstance(inner_link, str):
                    pass
                #Filter links to only allow other wiki links
                elif inner_link.startswith('/wiki/') and inner_link not in visited:
                    #Add node to visited
                    visited.add(inner_link)

                    #Add edge to graph
                    graph[term].add(inner_link)
    
                    #recurse deeper
                    dig_deeper(remaining_levels - 1, inner_link, graph, visited)



#Main
def main():
    
    #Get Data from input json and initialize
    relation_obj_list = []
    data = json.load(open('input.json','r'))
    
    #initialize all objects for inputs
    for key in data:
        relation_obj_list.append(Relation(key, data[key]))
    
    #initialize keyword lists may not be necessary, design choice here
    for obj in relation_obj_list:
        obj.initialize_keywords()
    
    #initialize each graph
    for obj in relation_obj_list:
        create_graph(obj)


#Main will run if nothing else specified
if __name__ == "__main__":
    main()


