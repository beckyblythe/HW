import pandas as pd
import re
import numpy as np
import sys
import random

data = pd.read_csv('data.csv', index_col = 'Product Id')

def query(income_string, data_reduction):
    '''Chooses items from narrawed data for which last input given by a customer is most relevant'''
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
    return income_string  
        
def ask_another_question():
    '''Asks for info about the item if previous answers didn't give ebeough info'''
    sys.stdout.write("Sorry, we need more information to proceed. What else can you say about the device you are looking for? ")
        
def ask_first_question():
    '''Starts the conversation. Asks to enter some info about the item'''
    sys.stdout.write('Hello! What kind of device are you interested in? ') 

def ask_to_choose(data_reduction):
    '''Asks to enter a number corresponding to 1 of the items in narrowed data'''
    sys.stdout.write('We believe you are looking for one of these: \n')
    sys.stdout.write("\n".join([str(i)+': ' + data_reduction.iloc[i]['Product Name'] for i in range(data_reduction.shape[0])]))
    sys.stdout.write('\nPlease enter the number of the desired device: ')
     
def ask_to_choose_again():
    '''Asks to enter a number corresponding to 1 of the items in narrowed data, after a customer entered a wrong number'''
    sys.stdout.write("The number you entered doesn't correspond to any device. Please try again.")
    
def suggest_random(data_reduction):
    '''Suggests random item from narrowed data'''
    sys.stdout.write("Sorry! We are not sure what you are looking for.\n")
    #Suggest random device. Just one option for a policy, when we can't figure out what to suggest
    random_idx = random.randint(0, data_reduction.shape[0]-1)
    sys.stdout.write('Try ' + data_reduction.iloc[random_idx]['Product Name']+
                             '. The subscription price is ' + str(data_reduction.iloc[random_idx]['Subscription Plan']))
    
def suggest(data_reduction, device_idx=-1):
    '''Suggests either chosen or single left item to a customer'''
    if  device_idx != -1:
        sys.stdout.write('You chose ' + data_reduction.iloc[device_idx]['Product Name']+'. The subscription price is '
                        + str(data_reduction.iloc[device_idx]['Subscription Plan'])) 
    else:
       sys.stdout.write('We believe you are looking for ' + data_reduction.iloc[0]['Product Name']+
                         '. The subscription price is ' + str(data_reduction.iloc[0]['Subscription Plan']))
        
    
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
            while (device_idx not in range(data_reduction.shape[0])) and (choice_number<3):
                if choice_number == 0:
                    ask_to_choose(data_reduction)
                else:
                    ask_to_choose_again()
                device_idx = int(read_message())
                choice_number +=1
            #if a customer entered a proper index, suggest the corresponding item
            if choice_number<3:            
                suggest(data_reduction, device_idx)
            else:
                suggest_random(data_reduction)          
    else:
       suggest_random(data_reduction)
        
        
    
main()