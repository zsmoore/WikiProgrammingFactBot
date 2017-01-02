#Parser for target input file for the purpose of relating subjects
import json
import pprint
class Parser:

    def __init__(self):

        self.subject_to_base = {}
        self.parse_file()

    #Parses input file
    def parse_file(self):
        
        with open('input.json') as data_file:
            data = json.load(data_file)

        print(type(data))


Parser()
