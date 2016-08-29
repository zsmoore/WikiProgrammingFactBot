from bs4 import BeautifulSoup
import requests

def crawl(file_name):
    
    start_url = 'https://en.wikipedia.org/wiki/Computer'
    start_page = requests.get(start_url)
    write_to = open(file_name, 'a')
    
    soup = BeautifulSoup(start_page.content)
    for link in soup.find_all('a'):
        inner_link = link.get('href')
        try:
            if type(inner_link) is None or inner_link is 'None':
                print('hit')
                continue
            elif inner_link.startswith('/wiki') and inner_link.find('.') == -1 and inner_link.find(':') == -1:
                write_to.write(start_url + '\t' +  'https://en.wikipedia.org/' + str(inner_link) + '\n')
                recurse(inner_link, file_name)
        except:
            print('hit')
            pass

        
def recurse(came_from, file_name):
    
    pre_cursor = 'https://en.wikipedia.org'
    write_to = open(file_name, 'a')
    
    try:
        req = requests.get(pre_cursor + came_from)
        soup = BeautifulSoup(req.content)
    except:
        print(came_from)
        return

    for link in soup.find_all('a'):
        inner_link = link.get('href')
        if(type(inner_link) == None):
            continue
        elif inner_link.startswith('/wiki') and inner_link.find('.') == -1 and inner_link.find(':') == -1:
            write_to.write(pre_cursor + came_from + '\t' + pre_cursor + str(inner_link) + '\n')
            recurse(inner_link, file_name)


def main():
    
    graph_file_name = 'web_graph.txt'
    open(graph_file_name, 'w')
    crawl(graph_file_name)

main()
