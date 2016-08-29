from bs4 import BeautifulSoup
import requests
import sys

sys.setrecursionlimit(1000000)
visited = set()

def crawl(file_name):
    
    start_url = 'https://en.wikipedia.org/wiki/Computer'
    global visited
    visited.add('/wiki/Computer')
    start_page = requests.get(start_url)
    write_to = open(file_name, 'a')
    
    soup = BeautifulSoup(start_page.content)

    for link in soup.find_all('a'):
        inner_link = str(link.get('href'))
        try:
            if type(inner_link) is None or inner_link is 'None':
                print('hit')
                continue
            elif str(inner_link).startswith('/wiki') and str(inner_link).find('.') == -1 and str(inner_link).find(':') == -1:
                if(str(inner_link) not in visited):
                    visited.add(str(inner_link))
                    write_to.write(start_url + '\t' +  'https://en.wikipedia.org/' + str(inner_link) + '\n')
                    write_to.flush()
                    recurse(str(inner_link), file_name)
        except Exception as e:
            print(e)
            print(inner_link)
            pass
    write_to.close()

        
def recurse(came_from, file_name):
    
    pre_cursor = 'https://en.wikipedia.org'
    write_to = open(file_name, 'a')
    global visited
    try:
        req = requests.get(pre_cursor + came_from)
        soup = BeautifulSoup(req.content)
    except:
        return
    for link in soup.find_all('a'):
        inner_link = str(link.get('href'))
        if(type(inner_link) == None):
            continue
        elif str(inner_link).startswith('/wiki') and inner_link.find('.') == -1 and inner_link.find(':') == -1:
            if(str(inner_link) not in visited):
                visited.add(str(inner_link))
                write_to.write(pre_cursor + came_from + '\t' + pre_cursor + str(inner_link) + '\n')
                write_to.flush()
                recurse(inner_link, file_name)
    write_to.close()


def main():
    
    graph_file_name = 'web_graph.txt'
    open(graph_file_name, 'w')
    crawl(graph_file_name)

main()
