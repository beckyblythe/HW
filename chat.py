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
    #for more data faster method needed
    for word in income_string.split(' '):
        for column in data_reduction.columns.values:
            #to change here!!!!
            candidates.append(word in data_reduction[column].str.split())
    matches = np.sum(np.array(candidates), axis = 0)
    return data.iloc[np.where(matches == matches.max())[0]]       
       
def read_message():
    income_string = input()
    while income_string.isspace() or income_string == '':
        sys.stdout.write("Your message is empty. Please try again. ")
        income_string = input()
    return income_string  
        
def ask_another_question():
    sys.stdout.write("Sorry, you didn't provide enough information to proceed. What else can you say about the device you are looking for? ")
    income_string = read_message()    
    return income_string
    
def ask_first_question():
    sys.stdout.write('Hello! What kind of device are you interested in? ') 
    income_string = read_message()    
    return income_string
     
def main():
    question_number = 0
    income_string = ask_first_question()
    data_reduction = query(income_string, data)
    while data_reduction.shape[0]>3 and question_number<2:
        income_string = ask_another_question()
        data_reduction = query(income_string, data_reduction)
        question_number += 1
    if data_reduction.shape[0]<=3 and data_reduction.shape[0]>1 :
        device_idx = -1
        trial_number = 0
        while device_idx not in range(data_reduction.shape[0]) and trial_number<3:
            if trial_number == 0:
                sys.stdout.write('We believe you are looking for one of these: \n')
                sys.stdout.write("\n".join([str(i)+': ' + data_reduction.iloc[i]['Product Name'] for i in range(data_reduction.shape[0])]))
                sys.stdout.write('Please enter the number of the desired device: ')
            else:
                sys.stdout.write("The number given doesn't correspond to any device.")
            device_idx = int(read_message())
            trial_number +=1
        if trial_number<4:            
            sys.stdout.write('You chose ' + data_reduction.iloc[device_idx]['Product Name']+'. The subscription price is '
                             + data_reduction.iloc[device_idx]['Subscription Plan']  )
        else:
            sys.stdout.write("Sorry! We can't figure out what device you're looking for. Please, try again from the beginning.")    
            
    else:
        if data_reduction.shape[0] == 1:
            sys.stdout.write('We believe you are looking for ' + data_reduction.iloc[0]['Product Name']+
                             '. The subscription price is ' + data_reduction.iloc[0]['Subscription Plan']  )
        else:
            #instead suggest something, also in the other case
            sys.stdout.write("Sorry! We can't figure out what device you're looking for. Please, try again from the beginning.")
        
    
main()