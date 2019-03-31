from my_tokenizer import my_tokenizer
from index import index
import os
from lxml import etree
#from lxml import html
import re

def iter_dir(given_path):
    """
    Take a string represents a path
    Iterate over the given directory path
    Return a list containing all files inside given path
    and files in its subdirectories
    """
    for element in os.listdir(given_path):
        result = list()
        target = given_path + "\\" + element
        if(os.path.isdir(target)):
            for file_name in os.listdir(target):
                doc_no = element + "\\" + file_name
                doc_path = target + "\\" + file_name
                result.append((doc_no,doc_path))
            yield result

def my_parser(root):
    for element in root.iter():
        if (element.text != None and element.text != ""):
            result = element.text.encode('utf-8')
            yield result.strip()

"""
def my_parser(f):
    parser = etree.HTMLParser()
    root = etree.parse(f,parser)
    for value in root.iter():
        if (value.text != None):
            result = value.text.encode('utf-8')
            yield result.strip()
"""
                
def tag_list(root, tag_name):
    try:
        return root.xpath(tag_name)
    except:
        return []


def get_token_list(string):
    if string != "":
        return my_tokenizer(string)
    else:
        return []
    
            
if __name__ == "__main__":
    file_list_generator = iter_dir("C:\\Users\\Franc\\eclipse-workspace\\indexer\\WEBPAGES_RAW")
     
    count = 0
    for wl in file_list_generator:
        my_index = index()
        for f in wl:
            html_file = open(f[1],"r")
            
            parser = etree.HTMLParser()
            root = etree.parse(html_file, parser)
            html_file.close() 
            
            for line in my_parser(root):
                for token in get_token_list(line):
                    my_index.add(token,f[0])
                    
            try:
                taglist = tag_list(root,'//title')
                for element in taglist:
                    if (element.text != None):
                        for token in get_token_list(element.text.encode('utf-8')):
                            my_index.add_tag(token, f[0],element.tag.encode('utf-8'))
                   
                meta_description_element = root.xpath("//meta[@name='description']")#[@property='description']
                if (meta_description_element != []):
                    for meta in meta_description_element:
                        temp = (etree.tostring(meta, pretty_print = True)).encode('utf-8')
                        L = re.split("name=\"description\"", temp.lstrip("<meta").strip().rstrip('/>'))
                        for string in L:
                            if string != None and string != '':
                                for token in get_token_list(string):
                                    my_index.add_tag(token, f[0], 'meta')
                
            except:
                print f[0], " fail to load root"  
            
        print "directory ", count, " reading complete"
        
        file_name = "raw_index\\index_" + str(count)+".txt"
        f = open(file_name,"w")
        
        sorted_list = my_index.token_dict.keys()
        sorted_list.sort()
        for k in sorted_list:
            output = my_index.read_token(k).rstrip(',') + "\n"
            
            f.write(output)
            
            
        f.close()
        print "directory ", count, " writing complete"
        count += 1