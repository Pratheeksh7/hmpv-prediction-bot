import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv('interactive_covid_dataset.csv')

# Define features and target
X = data[['fever', 'cough', 'runny_nose', 'breath_difficulty', 'age','rash']]
y = data['positive']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the model
with open('covid_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model trained and saved as covid_model.pkl")
