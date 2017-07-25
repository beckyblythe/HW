import pandas as pd
import numpy as np
import sys
import random

data = pd.read_csv('data.csv', index_col = 'Product Id')

def query(income_string, data_reduction):
    '''Chooses items from narrowed data for which last input given by a customer is most relevant'''
    candidates = []
    #for more data faster method needed
    #Find rows in data/narrowed data in which words from customer's input participate most often
    for word in income_string.split(' '):
        for column in data_reduction.drop(['Subscription Plan'], axis = 1).columns.values:
            #think of some nicer way to do it
            candidates.append([word.lower() in string.lower().split(' ') for string in data_reduction[column].tolist()])
    matches = np.sum(np.array(candidates), axis = 0)
    return data_reduction.iloc[np.where(matches == matches.max())[0]]       
       
def read_message():
    '''Reads customer's input. If the input is empty asks again'''
    income_string = input()
    while income_string.isspace() or income_string == '':
        sys.stdout.write("Your message is empty. Please try again. ")
        income_string = input()
    income_words = np.unique(np.array(income_string.split(' ')))
    return income_words  

def ask_first_question():
    '''Starts the conversation. Asks to enter some info about the item'''
    sys.stdout.write('Hello! What kind of device are you interested in?\n') 
    sys.stdout.write('Tip: you can type "abort" any time to abort the session. ')
        
def ask_another_question():
    '''Asks for info about the item if previous answers didn't give enough info'''
    sys.stdout.write("Sorry, we need more information to proceed. What else can you say about the device you are looking for? ")
        
def ask_to_choose(column_uniques):
    '''Asks to enter a number corresponding to one of the items in the narrowed data'''
    sys.stdout.write("\n".join([str(i)+': ' + column_uniques[i] 
                                for i in range(column_uniques.shape[0])]))
    sys.stdout.write('\nPlease enter the corresponding number: ')
     
def ask_to_choose_again():
    '''Asks to enter a number corresponding to one of the items in narrowed data, after a customer entered a wrong number'''
    sys.stdout.write("The number you entered doesn't correspond to any device. Please try again. ")
    
def suggest_random(data_reduction):
    '''Suggests random item from narrowed data'''
    sys.stdout.write("Sorry! We are not sure what you are looking for.\n")
    #Suggest random device. Just an option what to do, when we can't figure out what to suggest
    random_idx = random.randint(0, data_reduction.shape[0]-1)
    sys.stdout.write('Try ' + data_reduction.iloc[random_idx]['Product Name']+
                             '. Subscription price is ' + str(data_reduction.iloc[random_idx]['Subscription Plan'])+' €.')
    
def suggest(data_reduction, device_idx=-1):
    '''Suggests either chosen or single left item to a customer'''
#    if  device_idx != -1:
    sys.stdout.write('You chose ' + data_reduction.iloc[device_idx]['Product Name']+'. Subscription price is '
                    + str(data_reduction.iloc[device_idx]['Subscription Plan'])+' €.') 
#    else:
#       sys.stdout.write('We believe you are looking for ' + data_reduction.iloc[0]['Product Name']+
#                         '. Subscription price is ' + str(data_reduction.iloc[0]['Subscription Plan'])+' €.')
#       
def check_reset(income_words):
    '''Checks if a customer enterd reset code word'''
    return income_words[0] =='abort'
    
def reset():
    '''Runs a new session'''
    sys.stdout.write("You aborted the session. Let's try again.\n")
    main()
        

def new_query(data_reduction, words, column_name, remaining_words=1):
    if type(remaining_words) ==int:
        remaining_words = np.ones((data_reduction.shape[0], words.shape[0]))
    matches = np.zeros(data_reduction.shape[0])
    for row in range(data_reduction.shape[0]):
        for i in range(words.shape[0]):
            if remaining_words[row,i]:
                if words[i].lower() in data_reduction.iloc[row][column_name].lower().split():
                    matches[row]+=1
                    remaining_words[row, i] = 0
    
    candidate_rows = np.where(matches == matches.max())[0]
    data_reduction = data_reduction.iloc[candidate_rows]
    remaining_words = remaining_words[candidate_rows,:]
    return data_reduction, remaining_words
    
    
def new_main():
    data_reduction = data
    ask_first_question()
    income_words = read_message()
    #check for session reset
    if check_reset(income_words):
        reset()
        return
    data_reduction, remaining_words = new_query(data_reduction,income_words, 'Tags')
    if data_reduction.shape[0]>1:
        data_reduction, remaining_words = new_query(data_reduction,income_words, 'Product Name', remaining_words)
        if data_reduction.shape[0]>1:
            data_reduction, remaining_words = new_query(data_reduction,income_words, 'Brand', remaining_words)
    if data_reduction.shape[0]==1:
        suggest(data_reduction)
        return()
    else:
        #loooooooop???
        if data_reduction['Category'].unique().shape[0]>1:
            categories = data_reduction['Category'].unique()
            print('We found products correponding to your query in '
                  +str(data_reduction['Category'].unique().shape[0])+ ' categories')
            ask_to_choose(categories)
            income_words = read_message()
            #check for session reset
            if check_reset(income_words):
                reset()
                return
            #implement a check here
            index = int(income_words[0])
            data_reduction=data_reduction.loc[data_reduction['Category']==categories[index]]
                
        if data_reduction['Brand'].unique().shape[0]>1:
            brands = data_reduction['Brand'].unique()
            print('We found products correponding to your query from '
                  +str(data_reduction['Brand'].unique().shape[0])+ ' brands')
            ask_to_choose(brands)
            income_words = read_message()
            #check for session reset
            if check_reset(income_words):
                reset()
                return
            #implement a check here
            index = int(income_words[0])
            data_reduction=data_reduction.loc[data_reduction['Brand']==brands[index]]
            
        if data_reduction['Product Name'].unique().shape[0]>1:
            names = data_reduction['Product Name'].unique()
            print('We found '+str(names.shape[0])+'products correponding to your query')
            ask_to_choose(names)
            income_words = read_message()
            #check for session reset
            if check_reset(income_words):
                reset()
                return
            #implement a check here
            index = int(income_words[0])
            data_reduction=data_reduction.loc[data_reduction['Product Name']==names[index]]
    suggest(data_reduction)
new_main()
        
        

def main():
    #initialize
    question_number = 0
    data_reduction = data
    #ask at most 3 questions, narrow number of items to at most 3
    while (data_reduction.shape[0]>3) and (question_number<3):
        if question_number == 0:
            ask_first_question()
        else:
            ask_another_question()
        income_string = read_message()
        #check for session reset
        if check_reset(income_string):
            reset()
            return
        data_reduction = query(income_string, data_reduction)
        question_number += 1
    #if we narrrowed number of items enough, make a decision which item to suggest
    if data_reduction.shape[0]<=3:
        #if only a single item left, suggest it to a customer
        if data_reduction.shape[0] == 1:
            suggest(data_reduction)
        #if more than 1 item left, ask customer to choose the item they are interested in
        else:
            #ask at most 3 times to choose an item from the reduced list, till they give a proper index
            device_idx = -1
            choice_number = 0
            while device_idx not in range(data_reduction.shape[0]):
                if choice_number == 0:
                    ask_to_choose(data_reduction)
                else:
                    ask_to_choose_again()
                income_string = read_message()
                #check for session reset
                if check_reset(income_string):
                    reset()
                    return
                device_idx = int(income_string)
                choice_number +=1
            #when a customer entered a proper index, suggest the corresponding item
            suggest(data_reduction, device_idx)
    else:
       suggest_random(data_reduction)
        
        
    
#main()