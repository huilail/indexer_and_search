# indexer_and_search
organizing raw html data and searching according to keywords

Indexer
It processes and organize raw html data returned by web-crawler.
The processed data is stored locally in a text file using a searching friendly format.
(The local file can also be stored in database to ensure the security and backup)



Search
It search the inputed keywords in the processed data and return the url of web page.
The searching algorithm considers:
  frequency of occurance of the keyword in the whole data
  frequency of occurance of the keyword in the given web page file
  occurance in metatage, title, bolded text, description 
The result urls are sorted in descending order according to webpage score.
