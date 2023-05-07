from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import turtle
import DataVisualizationTurtle

# Open file and initialize input and output lists
# mvp_data was manually compiled using voting data from 1979-1980 to 2018-2019
mvp_data = open('mvpvotes.csv', encoding='latin1') # use encoding to ignore special characters like %
mvp_data2020 = open('mvpvotes2020.csv', encoding='latin1')

header2020 = mvp_data2020.readline()
subheader2020 = mvp_data2020.readline()
header = mvp_data.readline()
sub_header = mvp_data.readline()

x = []
y = []

for line in mvp_data:
  datalist = line.strip().split(',')
  if datalist[4] != 'G':
  # Output is quantity of votes
    y += [float(datalist[6])]
  # input is statistics achieved throughout the year by a player
    x += [[float(datalist[12]),float(datalist[13]),float(datalist[14]),float(datalist[15]),float(datalist[21]),float(datalist[22]),float(datalist[23]),float(datalist[24])]]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)

predictor = LinearRegression(n_jobs=-1)
predictor.fit(X=x_train,y=y_train)
testdict = {}
for i in range(len(x_test)):
  X_test = [x_test[i]]
  # print(X_test)
  outcome = predictor.predict(X_test)
  coefficients = predictor.coef_  
  #print(y_test)
  testdict[y_test[i]] = float(outcome)
# print((testdict))

# Initialize dictionary to store percenterror percentages
percent_storage = {"0-10":0,"10-20":0,"20-30":0,"30-40":0,"40-50":0,"50-60":0,\
"60-70":0,"70-80":0,"80-90":0,"90-100":0,">100":0}
percenterror = 0

# Loop through testdict to find percenterror and store to percent_storage
for key in testdict:
  if key != 0:
    percenterror = (abs(key - testdict[key])/key)
    if percenterror > 1.00:
      percent_storage[">100"] += 1
    elif 0<percenterror<=0.10:
      percent_storage["0-10"] += 1
    elif 0.10<percenterror<=0.20:
      percent_storage["10-20"] += 1
    elif 0.20<percenterror<=0.30:
      percent_storage["20-30"] += 1
    elif 0.30<percenterror<=0.40:
      percent_storage["30-40"] += 1
    elif 0.40<percenterror<=0.50:
      percent_storage["40-50"] += 1
    elif 0.50<percenterror<=0.60:
      percent_storage["50-60"] += 1
    elif 0.60<percenterror<=0.70:
      percent_storage["60-70"] += 1
    elif 0.70<percenterror<=0.80:
      percent_storage["70-80"] += 1    
    elif 0.80<percenterror<=0.90:
      percent_storage["80-90"] += 1
    elif 0.90<percenterror<=1.00:
      percent_storage["90-100"] += 1
# print(percent_storage)

# Using data from 2019-2020, predict how many points each player will receive
player_votes = {}
for line in mvp_data2020:
  datalist = line.strip().split(',')
  if datalist[4] != 'G':
    # print([float(datalist[12]),float(datalist[13]),float(datalist[14]),float(datalist[15]),float(datalist[21]),float(datalist[22]),float(datalist[23]),float(datalist[24])])
    real_outcome = predictor.predict([[float(datalist[12]),float(datalist[13]),float(datalist[14]),float(datalist[15]),float(datalist[21]),float(datalist[22]),float(datalist[23]),float(datalist[24])]])
    # print(datalist[1])
    player_votes[datalist[1]] = float(real_outcome)

top_score = 0
for key, value in player_votes.items():
  if value > top_score:
    top_score = value
    top_player = key

# Retrieve name from column 1 of csv
split = top_player.split('\\')
top_player_name = split[0]
# print(top_player_name,top_score,"votes")

print('Type 0 to exit')
print('Type 1 to look at percentage error performance of model : ')
print('Type 2 to look at visual showing predicted MVP and \
 predicted # of votes for 2019-2020 season: ')
print('Type 3 to look at a list of top players and their predicted votes')
print('Type 4 to clear the screen')

while True:
  userinput = input("PLEASE TYPE IN A NUMBER BETWEEN 0-4: ")
  if userinput == '0':
    break
    exit()
  elif userinput == '1':
      DataVisualizationTurtle.bargraph(percent_storage)
  elif userinput == '2':
    DataVisualizationTurtle.Draw_Scoreboard(top_player_name,top_score)
  elif userinput == '3':
    for key, value in player_votes.items():
      key = key.split('\\')
      print(key[0],'----->',value,'votes')
  elif userinput == '4':
    DataVisualizationTurtle.clear_screen()
  else:
    print("Sorry, I don't understand " + userinput)

