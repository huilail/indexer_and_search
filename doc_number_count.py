import os


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
            

if __name__ == "__main__":
    
    count = 0
    for sub_dir in iter_dir("C:\\Users\\Franc\\eclipse-workspace\\indexer\\WEBPAGES_RAW"):
        count += len(sub_dir)
    print "doc_num = ", count
    
    count = 0
    f = open("merged_index.txt",'r')
    for line in f:
        count += 1
    print "token_num = ", count
        