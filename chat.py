import pandas as pd
import numpy as np
import sys
import random

data = pd.read_csv('data.csv', index_col = 'Product Id')

def read_message():
    '''Reads customer's input. If the input is empty asks again'''
    income_string = input()
    while income_string.isspace() or income_string == '':
        sys.stdout.write("Your message is empty. Please try again. ")
        income_string = input()
#    trim
    income_words = np.unique(np.array(income_string.split(' ')))
    return income_words  

def ask_first_question():
    '''Starts the conversation. Asks to enter some info about the item'''
    sys.stdout.write('Hello! What kind of device are you interested in?\n') 
    sys.stdout.write('Tip: you can type "abort" any time to abort the session. ')
               
def ask_to_choose(column_uniques, column_name):
    '''Asks to enter a number from numbers to choose'''
    if column_name == 'Category':
        sys.stdout.write('We found products correponding to your query in '
          +str(column_uniques.shape[0])+ ' categories:\n')
    if column_name == 'Brand':
        sys.stdout.write('We found products correponding to your query from '
          +str(column_uniques.shape[0])+ ' brands:\n')
    if column_name == 'Product Name':
        sys.stdout.write('We found '+str(column_uniques.shape[0])+ 
                                         ' products correponding to your query:\n')
    
    sys.stdout.write("\n".join([str(i)+': ' + column_uniques[i] 
                                for i in range(column_uniques.shape[0])]))
    sys.stdout.write('\nPlease enter the corresponding number: ')
     
def ask_to_choose_again():
    '''Asks to enter a number from numbers to choose, after a customer entered a wrong number'''
    sys.stdout.write("The number you entered is out of the range. Please try again. ")

def suggest(data_reduction):
    '''Suggests single left item to a customer'''
    sys.stdout.write('You chose ' + data_reduction.iloc[0]['Product Name']+'. Subscription price is '
                    + str(data_reduction.iloc[0]['Subscription Plan'])) 
    
def suggest_random(data_reduction):
    '''Suggests random item from data'''
    sys.stdout.write("Sorry! We didn't find any device corresponding to your query.\n")
    #Suggest random device. Just an option what to do, when we can't figure out what to suggest
    random_idx = random.randint(0, data_reduction.shape[0]-1)
    sys.stdout.write('Try ' + data_reduction.iloc[random_idx]['Product Name']+
                             '. Subscription price is ' + str(data_reduction.iloc[random_idx]['Subscription Plan']))
    
def check_index(input_words, column_uniques):
    '''Cheks for correct input when choosing'''
    return input_words.shape[0] == 1 and (input_words[0] in [str(idx) for idx in range(column_uniques.shape[0])])
    
def check_reset(income_words):
    '''Checks if a customer entered reset code word'''
    return income_words[0] =='abort'
    
def reset():
    '''Runs a new session'''
    sys.stdout.write("You aborted the session. Let's try again.\n")
    new_main()
         
def new_query(data_reduction, words, column_name, remaining_words=1):
    #initialize remaining_words matrix if the beginning of conversation
    if type(remaining_words) ==int:
        remaining_words = np.ones((data_reduction.shape[0], words.shape[0]))
    matches = np.zeros(data_reduction.shape[0])
    #chec what words are in the column and where; exclude from remaining words the ones that are met
    for row in range(data_reduction.shape[0]):
        for i in range(words.shape[0]):
            if remaining_words[row,i]:
                if words[i].lower() in data_reduction.iloc[row][column_name].lower().split():
                    matches[row]+=1
                    remaining_words[row, i] = 0
    #find most relevant rows
    candidate_rows = np.where(matches == matches.max())[0]
    data_reduction = data_reduction.iloc[candidate_rows]
    remaining_words = remaining_words[candidate_rows,:]
    return data_reduction, remaining_words
    
def choosing(data_reduction, column_name):
    '''Asks to choose from unique values in column_name. Narrows data according to the answer'''
    column_uniques = data_reduction[column_name].unique()
    ask_to_choose(column_uniques, column_name)
    income_words = read_message()
    #check for correct input
    while not check_index(income_words, column_uniques):
        reset_var = check_reset(income_words)
        if reset_var:            
            return reset_var, data_reduction 
        ask_to_choose_again()
        income_words = read_message()
    index = int(income_words[0])
    data_reduction=data_reduction.loc[data_reduction[column_name]==column_uniques[index]]
    return False, data_reduction
    
   
    
def new_main():
    data_reduction = data
    remaining_words=1
    ask_first_question()
    income_words = read_message()
    #check for session reset
    if check_reset(income_words):
        reset()
        return
    #check for words in Tags, afterwards Product Name, afterwards Brand; each time only most relevant rows remain
    for column_name in ['Tags', 'Product Name', 'Brand']:
        if data_reduction.shape[0]>1:
            data_reduction, remaining_words = new_query(data_reduction,income_words, column_name, remaining_words)
    #If words were not found, start from the beginnig
    if data_reduction.shape[0] == data.shape[0]:
        suggest_random(data_reduction)
        return
    #if the decision is not made, ask a customer to choose
    if data_reduction.shape[0] != 1:
        #first a customer chooses a category (if it's ambiguous)
        for column_name in ['Category', 'Brand','Product Name']:
            if data_reduction[column_name].unique().shape[0]>1:
               reset_var, data_reduction = choosing(data_reduction, column_name)
               if reset_var:
                   reset()
                   return
    #When only 1 item left, show a customer it's subscription price
    suggest(data_reduction)

new_main()
        
        