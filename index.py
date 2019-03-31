from chardet.latin1prober import FREQ_CAT_NUM
class doc_info:
    
    def __init__(self):
        self.freq = 0
        self.tags = set()
        
    def add(self):
        self.freq += 1
            
    def add_tag(self, tag):
        self.tags.add(tag)



class index:
    
    def __init__(self):
        self.token_dict = dict()
        
        
    def add(self, element, doc_no):
        if (element != ""):
            
            if (not self.token_dict.has_key(element)):
                """
                If the given token is not a key in self.token_dict
                Add the token into it
                """
                self.token_dict[element] = dict()
                
            if (not self.token_dict[element].has_key(doc_no)):
                """
                If the given [doc] is not a [key] in the dict associate with the [token]
                Add the [doc] into the token dict
                """
                self.token_dict[element][doc_no] = doc_info()
                
            self.token_dict[element][doc_no].add()
        
    def add_tag(self, element, doc_no, tagname):
        """
        if (not self.token_dict.has_key(element)):
            self.add(element, doc_no)
        if (not self.token_dict[element].has_key(doc_no)):
            self.token_dict[element][doc_no] = doc_info()
            self.token_dict[element][doc_no].add()
        """
        if (self.token_dict.has_key(element) and self.token_dict[element].has_key(doc_no)):
            self.token_dict[element][doc_no].add_tag(tagname)
        
        
    def read_token(self, token):
        """
        Return a string
        first part is token string be separated with other parts by ;
        second part is a list of doc info 
        containing doc_no token_freq tags
        each element is separated by ,
        
        tag list contains all tags the doc has
        tags are separated by - 
        """
        if (not self.token_dict.has_key(token)):
            return None
        
        else:
            if (type(token) != str):
                print type(token)
                print token
                pause = raw_input("Stop here")
            result = token + ";"
            
            for doc in self.token_dict[token]:
                #print self.token_dict[token][doc]
                result += (doc + " " + str(self.token_dict[token][doc].freq) + " ")
                temp = ""
                if (self.token_dict[token][doc].tags == set()):
                    temp = "NONE"
                else:
                    for tag in self.token_dict[token][doc].tags:
                        temp += (tag + "-")     
                result += (temp.rstrip("-") + "," )
            return result
        
        