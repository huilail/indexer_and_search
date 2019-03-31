import math
from my_tokenizer import my_tokenizer
import json

class query_vector:
    
    def __init__(self,tokens):
        self.tf = dict()
        self.df = dict()
        self.initialize(tokens)
        self.length = 0.00
        #self.weight()
    
    def initialize(self,tokens):
        for t in tokens:
            if not self.tf.has_key(t):
                self.tf[t]= 0.00
            self.tf[t] += 1.00
            self.df[t] = 0.00
            
    def normalize(self):
        for token in self.tf:
            self.tf[token] = float(self.tf[token])/float(self.length)
        self.tf[token] = -1*abs(self.tf[token]) + 1
    
    def weight(self,N):
        for token in self.tf:
            tf = float(self.tf[token])
            #self.tf[token] = (1.00 + math.log(tf,10)) * math.log(N/(self.df[token]),10)
            self.tf[token] = (1.00 + math.log(tf,10)) * math.log(N/(self.df[token]),10)
            self.length += (float(self.tf[token]) * float(self.tf[token]))
        self.length = math.sqrt(self.length)
        self.normalize()


class doc_vector:
    
    def __init__(self):
        self.d = dict()
        self.score = 0.00
        self.length = 0.00
        self.title = 0.00
        self.meta  = 0.00
    
    def add_token(self,token,freq):
        self.d[token] = float(freq)
    
    def normalize(self):
        for token in self.d:
            self.d[token] = float(self.d[token])/float(self.length)
    
    def weight_d(self, query_v, N):
        for token in self.d:
            tf = 0.00 + float(self.d[token])
            self.d[token] = (1 + math.log(tf,10)) * math.log(N/float(query_v.df[token]),10)
            self.length += (float(self.d[token]) * float(self.d[token]))
        self.length = math.sqrt(self.length)
        
        self.normalize()
        
        for token in self.d:
            self.score += (float(self.d[token]) * float(query_v.tf[token]))
        
        unique_token = float(len(query_v.tf))
        self.score += (self.title/unique_token) * 0.5
        self.score += (self.meta/unique_token) * 0.5 


def search(query_tokens, N, num=15):
    vq = query_vector(query_tokens)
    
    v_dict = dict()
    f = open("merged_index.txt",'r')
    for line in f:
        temp = line.split(';')
        
        if (temp[0] in query_tokens):
            #print temp[0]
            
            count = 0
            docs = temp[1].split(',')
            #for doc in docs:
                #print doc
            for doc in docs:
                count += 1
                element = doc.split()
                # doc_no = element[0]
                # freq   = element[1]
                # tags   = element[2]
                if not v_dict.has_key(element[0]):
                    v_dict[element[0]] = doc_vector()
                v_dict[element[0]].add_token(temp[0],element[1])
                tags = element[2].split('-')
                if not tags[0] == "NONE":
                    for t in tags:
                        if t == 'title':
                            v_dict[element[0]].title += 1.00
                        elif t == 'meta':
                            v_dict[element[0]].meta  += 1.00
                            
            vq.df[temp[0]] = count
    f.close()
    vq.weight(N)
    for k in v_dict:
        v_dict[k].weight_d(vq,N)
    
    result = sorted([(doc,v_dict[doc].score) for doc in v_dict], key = lambda v: v[1], reverse = True)
    #return result
    if len(result) <= num :
        return result
    else:
        return [result[i] for i in range(num)]

def print_result(L):
    print "Start Printing Results"
    count = 1
    for url in L:
        print str(count)," Link: ", url
        count += 1
    
if __name__ == "__main__":
    user_input = ""
    f = open("WEBPAGES_RAW\\bookkeeping.json","r")
    json_obj = json.load(f)
    f.close()
    webpage_number = len(json_obj)
    print "number of document = ", webpage_number
    while (True):
        user_input = raw_input("Enter search query or (q) to quit: ").lower().strip()
        number_of_result = raw_input("Enter the number of results you want (default 15): ")
        try:
            number_of_result = int(number_of_result)
        except:
            number_of_result = ""
        
        if user_input == 'q':
            break
        
        if (user_input != ""):
            query_tokens = my_tokenizer(user_input)
            try:
                if number_of_result == "":
                    result = search(query_tokens, webpage_number)
                else:
                    result = search(query_tokens, webpage_number, num = number_of_result)
                count = 1
                print "Results of: ", user_input
                for element in result:
                    temp = element[0].split('\\')
                    key = temp[0] + '/' + temp[1]
                    print "Link ", count, ": ", json_obj[key], "\ndoc_number: ", element[0], "\nScore: ", element[1], "\n"
                    count += 1
                #print_result(result)
            except ZeroDivisionError:
                print "No Result Found"
        else:
            print "Search query cannot be empty"
    