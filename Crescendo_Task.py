#!/usr/bin/env python
# coding: utf-8

# # Loading Dataset

# In[2]:


import json

with open('E:\\All Aplication\\Interview-Task\\Crescendo-Task\\MLB2016\\MLB2016.json') as f:
    data = json.load(f)

print(data)


# In[9]:


print(len(data))


# # Anser to the Question no - 3

# In[109]:


def moneyline_prob_converter(num):
    if num > 0:
        return 100 / (num + 100)
    else:
        return (-1 * (num)) / ((-1 * num) + 100)

def is_win(score1, score2):
    if score1 > score2:
        return 1
    else:
        return 0
firstMoneyUS2_Count = 0
lastMoneyUS2_Count = 0

data_dict = {}
count = 0
for index in range(total):
    gameID = data['GameID'][index]
    #print(gameID)
    #print(data['HomeTeam'][index])
    myDataLines = data['Lines'][index]
    #print(myDataLines)
    for x in myDataLines['MoneyUS2']:
        firstMoneyUS2 = x
        if firstMoneyUS2 != "NA":
            break
    
    for x in reversed(myDataLines['MoneyUS2']):
        lastMoneyUS2 = x
        if lastMoneyUS2 != "NA":
            break
    
    #print(moneyline_prob_converter(firstMoneyUS2))
    #print(moneyline_prob_converter(lastMoneyUS2))
    win_or_lose = is_win(data['FinalScoreHome'][index], data['FinalScoreAway'][index])
    firstMoneyUS2_probability = moneyline_prob_converter(firstMoneyUS2)
    lastMoneyUS2_probability = moneyline_prob_converter(lastMoneyUS2)
    
    data_dict[gameID] = (firstMoneyUS2_probability, lastMoneyUS2_probability, win_or_lose)
    
    if win_or_lose > 0:
        if firstMoneyUS2_probability > lastMoneyUS2_probability:
            firstMoneyUS2_Count = firstMoneyUS2_Count + 1
        else:
            lastMoneyUS2_Count = lastMoneyUS2_Count + 1
    else:
        if firstMoneyUS2_probability < lastMoneyUS2_probability:
            firstMoneyUS2_Count = firstMoneyUS2_Count + 1
        else:
            lastMoneyUS2_Count = lastMoneyUS2_Count + 1
    
    print(gameID, data_dict[gameID])
        
print(firstMoneyUS2_Count)
print(lastMoneyUS2_Count)


# # Answer to the Question no -3.a

# ### From the above output information, we can see that "lastMoneyUS2" better predictor for the final outcome. I've counted both predictor value. I found value for the First_MoneyUS2= 1106 and lastMoneyUS2= 1356.  

# # Answer to the Question no -1

# # Json Data convert to Dataframe

# In[587]:


import pandas as pd
data_df = pd.read_json('E:\\All Aplication\\Interview-Task\\Crescendo-Task\\MLB2016\\MLB2016.json')
data_df.head()


# In[588]:


data_df.shape


# In[606]:


data_df.to_csv('Desktop\\data1.csv')


# In[387]:


print(list(data_df.columns))


# In[388]:


data_df.head(20)


# In[389]:


# Get all NL Central Team Records for 2016
year = 2018
#data_df.HomeTeam['Chicago Cubs']

data_df.HomeTeam.value_counts()


# In[391]:


cub = pd.concat([cubs1, cubs2],axis=0)
cub


# # create a dataframe for season home wins

# In[392]:


home_wins = (cubs1[cubs1['FinalScoreHome'] > cubs1['FinalScoreAway']]['HomeTeam'].value_counts())
print(home_wins)
#home_wins.value_counts()
#home_wins.set_axis(['home_wins'],axis='columns',inplace=True)
#home_wins.index.name = 'team'


# # create a dataframe for  season losses

# In[393]:


away_wins = (cubs2[cubs2['FinalScoreHome'] > cubs2['FinalScoreAway']]['AwayTeam'].value_counts()) 
print(home_losses)
#home_losses.set_axis(['losses'],axis='columns',inplace=True)
#home_losses.index.name = 'away_team'


# # Chicago Cubs Win Percentage

# In[394]:


home_play = (cubs1['HomeTeam'].value_counts())
#home_play
away_play = (cubs2['AwayTeam'].value_counts())
away_play


# # Final Win Percentage of the Chicago Cubs at the end of 2016

# In[395]:


Chicago_Cubs_win_percentage = (home_wins + away_wins)/(home_play + away_play)*100
Chicago_Cubs_win_percentage = Chicago_Cubs_win_percentage.round(2)
print(Chicago_Cubs_win_percentage)


# # Answer to the Question no - 1.a
# ## Plot the winning percentage of the Chicago Cubs as a function of time in 2016.

# In[396]:


import matplotlib.pyplot as plt
import seaborn as sns


# In[603]:


from datetime import datetime

    
import operator
data_dict = {}   #{player: (num_games, num_wins)}

def is_win(score1, score2):
        if score1 > score2:
            return True
        else:
            return False

for index, row in cub.iterrows():
    eventDate = datetime.utcfromtimestamp(row['EventDateTimeUTC']).strftime('%Y-%m-%d')
    eventDateMonth = datetime.strptime(eventDate, '%Y-%m-%d')
    eventMonth = eventDateMonth.strftime('%B')
    #print(eventMonth, row['AwayTeam'], row['HomeTeam'], row['FinalScoreAway'], row['FinalScoreHome'])
    
    if eventMonth not in data_dict:
        if row['AwayTeam'] == 'Chicago Cubs':
            if (is_win(row['FinalScoreAway'], row['FinalScoreHome'])):
                data_dict[eventMonth] = (1, 1)
            else:
                data_dict[eventMonth] = (1, 0)
        else:
            if (is_win(row['FinalScoreHome'], row['FinalScoreAway'])):
                data_dict[eventMonth] = (1, 1)
            else:
                data_dict[eventMonth] = (1, 0)
            #print(data_dict)
    else:
        num_games, num_wins = data_dict[eventMonth]
        if row['AwayTeam'] == 'Chicago Cubs':
            if (is_win(row['FinalScoreAway'], row['FinalScoreHome'])):
                data_dict[eventMonth] = (num_games+1, num_wins+1)
            else:
                data_dict[eventMonth] = (num_games+1, num_wins)
        else:
            if (is_win(row['FinalScoreHome'], row['FinalScoreAway'])):
                data_dict[eventMonth] = (num_games+1, num_wins+1)
            else:
                data_dict[eventMonth] = (num_games+1, num_wins)
                
#print(data_dict)


data_dict_rank = {} 
for data in data_dict:
    num_games, num_wins = data_dict[data]
    data_dict_rank[data] = ((num_wins/num_games)*100) 
#print(data_dict_rank)
listofTuples = sorted(data_dict_rank.items() , reverse=True, key=lambda x: x[1])
for elem in listofTuples :
    #print(elem[0] , " ::" , elem[1] ) 
    print(elem)
    
#{'April': 89.55, 'May': 67, 'June': (29, 16), 'July': (25, 11), 'August': (28, 22), 'September': (29, 18), 'October': (17, 10), 'November': (2, 2)}

import matplotlib.pylab as plt

lists = sorted(data_dict_rank.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.title('Monthly Percentage Of the Chicago Cubs')
plt.xlabel('Month')
plt.ylabel('Percentage')
plt.plot(x, y)
plt.show()


# # Answer to the Question no- 2
# ## Create an object that counts the number of games each pitcher started and the number of wins

# In[460]:


data_df.head(50)


# # Number of Games each Pitcher Started and the number of Wins

# In[477]:


import operator
data_dict = {}   #{player: (num_games, num_wins)}

def is_win(score1, score2):
    if score1 > score2:
        return True
    else:
        return False
    

for index, row in data_df.iterrows():
    if row[5] not in data_dict:
        if (is_win(row[7], row[8])):
            data_dict[row[5]] = (1, 1)
        else:
            data_dict[row[5]] = (1, 0)
    else:
        num_games, num_wins = data_dict[row[5]]
        if (is_win(row[7], row[8])):
            num_wins = num_wins + 1        
        data_dict[row[5]] = (num_games+1, num_wins)
            
    if row[6] not in data_dict:
        if (is_win(row[8], row[7])):
            data_dict[row[6]] = (1, 1)
        else:
            data_dict[row[6]] = (1, 0)
    else:
        num_games, num_wins = data_dict[row[6]]
        if (is_win(row[8], row[7])):
            num_wins = num_wins + 1        
        data_dict[row[6]] = (num_games+1, num_wins)
#print(data_dict)
print("Pitcher :"           "Games:"              "Wins:")
for key, value in data_dict.items():
    print(key, ' : ', value)


# # Answer to the Question no- 2.a
# ## Rank the Pitchers from Best to Worst using the Information Form the Table Above

# In[500]:


data_dict_rank = {} 
for data in data_dict:
    num_games, num_wins = data_dict[data]
    data_dict_rank[data] = ((num_wins/num_games)*100, num_games, num_wins) 

listofTuples = sorted(data_dict_rank.items() , reverse=True, key=lambda x: x[1])
for elem in listofTuples :
    print(elem[0] , " ::" , elem[1] ) 


# ## I ranked the pitchers from best to worst based on number of Games each Pitcher and the number of Wins. 
# ##  I've based on Pitcher, Games and Wins. If we see the above output of the Pitcher "S LUGO", it's 100 ranked. 
# ##  Beacuse, it plays 7 games and it wins 7 games. 
# 

# In[ ]:




