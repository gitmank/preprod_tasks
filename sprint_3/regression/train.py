import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# read csv into dataframe
df = pd.read_csv('../LIQUIDS_DATA.csv')

# preview data
print(df.head())
print(df.info())

# separate features and the labels
X = df.drop('Label', axis=1)
y = df['Label']

# split train and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=40)

# init model
model = LinearRegression()
model.fit(X_train, y_train)

# predict
y_pred = model.predict(X_test)

# calculate accuracy
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse:.4f}')

# try with user input
print('Enter the following features:')
features = {}
for col in X.columns:
    features[col] = float(input(f'{col}: '))
features = pd.DataFrame([features])
prediction = model.predict(features)
prediction = prediction[0]
if(prediction < 0.2):
    print('Definitely Lemonade! 🍋')
elif(prediction < 0.4):
    print('Probably lemonade, try a sip 🥤')
elif(prediction < 0.6):
    print('Could be lemonade, let us know if you taste it and find out 🥲')
elif(prediction < 0.8):
    print('Probably not lemonade 🤔')
else:
    print('You definitely shouldn\'t drink this 🫠')

# save model
np.save('model.npy', model)