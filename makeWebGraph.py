from bs4 import BeautifulSoup
import requests

def crawl(file_name):
    
    start_url = 'https://en.wikipedia.org/wiki/Computer'
    start_page = requests.get(start_url)
    write_to = open(file_name, 'a')
    
    soup = BeautifulSoup(start_page.content)
    for link in soup.find_all('a'):
        inner_link = link.get('href')
        if(type(inner_link) == None):
            continue
        write_to.write(start_url + '\t' +  str(inner_link) + '\n')
        recurse(inner_link, file_name)

        
def recurse(came_from, file_name):
    
    write_to = open(file_name, 'a')
    
    try:
        req = requests.get(came_from)
        soup = BeautifulSoup(req.content)
    except:
        print(came_from)
        return

    for link in soup.find_all('a'):
        inner_link = link.get('href')
        if(type(inner_link) == None):
            continue
        write_to.write(came_from + '\t' + str(inner_link) + '\n')
        recurse(inner_link, file_name)


def main():
    
    graph_file_name = 'web_graph.txt'
    open(graph_file_name, 'w')
    crawl(graph_file_name)

main()
