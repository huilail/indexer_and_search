import os

def print_dict(d):
    sorted_list = d.keys()
    sorted_list.sort()
        
    for k in sorted_list:        
        output = k + ";"
        for element in d[k]:
            output += element + ','
        print output.rstrip(',')
     

if __name__ == "__main__":
    dir_path = "C:\\Users\\Franc\\eclipse-workspace\\indexer\\raw_index"
    file_list = os.listdir(dir_path)
    
    d = dict()
    for file_name in file_list:
        #print_dict(d)
        print "start merging ", file_name
        f = open(dir_path + "\\" + file_name,'r')
        for line in f:
            #print line
            temp = line.split(';')
            
            if (not d.has_key(temp[0])):
                d[temp[0]] = temp[1].strip()
            else:
                d[temp[0]] += ',' + temp[1].strip()
        f.close()
        
    file_name = "merged_index.txt"
    f = open(file_name,"w")
        
    sorted_list = d.keys()
    sorted_list.sort()
        
    for k in sorted_list:        
        output = k + ";" + d[k]
        f.write(output+'\n')
            
            
    f.close()