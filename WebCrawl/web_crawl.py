from bs4 import BeautifulSoup
import requests
import pprint
from relation import Relation
import json
from collections import deque


'''

        NEED TO FIX DISAMBIGUATIONS
        NEED TO MULTIPROCESS AS WELL 
        Terms with colon mess up wikipedia possible split and search on both
        ex: GNU:_Compiler_for_java switch to search for GNU and Compiler_for_java

'''

#Based on KeyWords start building web graph of programming terms
def create_graph(relation_obj):

    #Graph set up and graph for json dump
    graph = {}
    visited = set()
    queue = deque()
    dist = {}

    #Base url
    base = 'https://en.wikipedia.org/wiki/'
    #1258
    #HARD CODED TO STOP FOR THIS EXAMPLE CHANGE THIS
    #For each key term
    count = 0
    for word in relation_obj.get_base_words():
        if count < 1256:
            count += 1
            continue

        print(word)
        #Build new urls and get html request
        full = base + word
        req = requests.get(full)
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
       
        #NEED SEPERATE FUNCTION FOR INCLUSION
        include = True
        div = soup.find('div', {'id':'mw-content-text'})
        #Filter out any disambiguations
        for test in div.find_all('p'):
            test = str(test)
            if 'may refer to:' in test or 'could refer to:' in test or 'Other reasons this message may be displayed:' in test:
                include = False
            
        #Only recurse on good links
        if include == True:
            visited.add('/wiki/' + word)
            #HERE IS WHERE DISTANCE IS DECIDED
            dist['/wiki/' + word] = 1
            queue.append('/wiki/' + word)
    
    #BFS
    while len(queue) > 0:
        node = queue.pop()

        print(dist[node], node)

        #Initialize term in graph to a set
        if node not in graph:
            graph[node] = set()
        

        #Base url for requests
        base = 'https://en.wikipedia.org'
            
        #Get request
        full = base + node
        req = requests.get(full) 
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
    
        #THIS IS BAD MAKE IT A SEPARATE FUNCTION FOR INCLUDING
        include = True
        div = soup.find('div',{'id':'mw-content-text'})
        #Filter out disambiguations
        for test in div.find_all('p'):
            test = str(test)
            if 'may refer to:' in test or 'could refer to:' in test or 'Other reasons this message may be displayed:' in test:
                include = False
                
        if include == True:
            #Get all connections
            for link in div.find_all('a'):
                inner_link = link.get('href')
                        
                #Check for Nones
                if not isinstance(inner_link, str):
                    continue
                #Filter links to only allow other wiki links
                elif inner_link.startswith('/wiki/') and inner_link not in visited:
       
                    #Add edge to graph
                    graph[node].add(inner_link)
                    
                    #Only continue if we haven't reached our max depth yet
                    if dist[node] > 0:
                        #Add node to visited
                        visited.add(inner_link)
 
                        #Add to queue
                        queue.append(inner_link)
        
                        #Decrement distance
                        dist[inner_link] = dist[node] - 1

    #Change sets to lists so it is json compatible
    for key in graph:
        graph[key] = list(graph[key])

    #Dump subject's graph to json
    with open(str(relation_obj) + '.json', 'w') as fp:
        json.dump(graph, fp)
                        

'''
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

'''

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
