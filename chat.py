import pandas as pd
import re
import numpy as np
import sys

mail = pd.read_html('Gmail.html' )
data = mail[-1]
data.columns =  data.iloc[0]
data = data[1:] 
data.set_index('Product Id')

def query(income_string, data_reduction):
    candidates = []
    for word in income_string.split():
        for column in data_reduction.columns.values:
            candidates.append(data_reduction[column].str.contains(word, flags = re.IGNORECASE))
    matches = np.sum(np.array(candidates), axis = 0)
    print(matches)
    return matches
    
def decision(matches):
    print(np.where(matches == matches.max())[0])
    if len(np.where(matches == matches.max())[0]) == 1:
        return np.argmax(matches)
    else:
        ask__another_question()
        
def ask__another_question():
    sys.stdout.write("Sorry, you didn't provide enough information to proceed. What else can you say about the device you are looking for?")
    
    
    
matches = query('Iphone fuck 32GB', data)
answer = decision(matches)
print(data.iloc[answer])