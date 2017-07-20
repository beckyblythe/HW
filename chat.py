import pandas as pd

mail = pd.read_html('Gmail.html' )
data = mail[-1]
data.columns =  data.iloc[0]
data = data[1:] 
data.set_index('Product Id')

def query(income_string):
    candidates = []
    for word in income_string:
        for column in data.columns.values:
            candidates.append(data[column].str.contains(word))
    print(candidates)
    
query('32GB')
        