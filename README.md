# Nigerian Real Estate Price Prediction App

## Project Overview

This project is a **Nigerian real estate house price prediction web application** built with **Python** and **Streamlit**. The application allows users to estimate the price of a house in Nigeria by entering basic property information such as the number of bedrooms, number of bathrooms, house type, town, and state.

The project also includes an **exploration/insights page** where users can view charts that explain patterns in the housing dataset. These charts help users understand how house prices differ by location, state, and property type.

In simple terms, this project does two main things:

1. **Predicts house prices** using a trained machine learning model.
2. **Displays real estate market insights** using data visualisation.

---

## Project Demo Video

A recorded demonstration of the project has been included in the project files. The video shows how the application works and can be used to present the project during assessment or review.

[Watch the Project Demo Video](stock%20price%20prediction%20project.mp4)

---

## What the Project Does

The application uses historical Nigerian housing data to learn patterns between property features and house prices. After the model has been trained, the app can estimate the price of a property based on the details selected by the user.

For example, a user can select:

- Number of bedrooms
- Number of bathrooms
- House type
- State
- Town

The app then sends those values into the trained machine learning model and returns an estimated property price in Nigerian Naira.

The application also tries to display the selected property location on a map using the town and state selected by the user.

---

## Main Features

### 1. House Price Prediction

The prediction page allows users to enter property details and receive an estimated house price.

The model uses the following input features:

- `bedrooms`
- `bathrooms`
- `house_type`
- `town`
- `state`

The predicted output is:

- Estimated house price in Nigerian Naira

---

### 2. Market Insights / Explore Page

The explore page gives visual information about the Nigerian housing market. It loads the dataset, cleans it, removes outliers, and then displays charts.

The charts include:

- Most expensive towns
- Average house price by state
- Average house price by house type
- Relationship between price and price per room

This helps users understand which locations and property types are generally more expensive.

---

### 3. Location Map

After a prediction is made, the app can show the selected property location on a map.

It uses:

- `geopy` to search for the location coordinates
- `folium` to create the map
- `streamlit-folium` to display the map inside the Streamlit app

---

## How the Project Works

The project works in four main stages:

1. The dataset is loaded.
2. The data is cleaned and prepared.
3. A machine learning model is trained and saved.
4. The Streamlit app loads the saved model and uses it to make predictions.

---

## Dataset

The project uses the file:

```text
nigeria_houses_data.csv
```

This dataset contains Nigerian house listing records. The important columns include:

```text
bedrooms
bathrooms
toilets
parking_space
title
town
state
price
```

The `title` column represents the type of house. During cleaning, it is renamed to `house_type`.

Example house types include:

- Detached Duplex
- Detached Bungalow
- Semi Detached Duplex
- Terraced Duplexes
- Block of Flats

---

## Data Cleaning Process

Before the data is used for training or visualisation, the project cleans it.

The cleaning process includes:

### 1. Dropping Unneeded Columns

The `toilets` column is removed if it exists because the model mainly uses bedrooms, bathrooms, house type, town, and state.

### 2. Removing Outliers

The project removes extreme values from numeric columns such as:

- `bedrooms`
- `bathrooms`
- `parking_space`
- `price`

This is done using the Interquartile Range method, also known as the IQR method.

### 3. Renaming the House Type Column

The dataset column named `title` is renamed to:

```text
house_type
```

This makes the data easier to understand in the rest of the project.

### 4. Creating New Features

The project creates two extra calculated columns:

```text
total_rooms = bedrooms + bathrooms
price_per_room = price / total_rooms
```

These columns help the project identify unusual price patterns.

### 5. Removing Rare States and Towns

The project removes states and towns that have too few records. This helps the model train on locations that have enough examples in the dataset.

---

## Machine Learning Model

The model training code is located in:

```text
train_model.py
```

The project uses a **Random Forest Regressor** to predict house prices.

A regressor is used because the target value, house price, is a number.

The model is trained using:

```python
RandomForestRegressor
```

The model learns from the following columns:

```text
bedrooms
bathrooms
house_type
town
state
```

The target column is:

```text
price
```

---

## Encoding Categorical Data

Machine learning models cannot directly understand text values like `Lagos`, `Abuja`, or `Detached Duplex`.

Because of this, the project uses `LabelEncoder` to convert text columns into numbers.

The encoded columns are:

- `house_type`
- `town`
- `state`

The encoders are saved together with the model so that the Streamlit app can encode user-selected values in the same way during prediction.

---

## Saved Model File

The trained model and encoders are saved in:

```text
model.joblib
```

This file contains:

- The trained Random Forest model
- Label encoder for house type
- Label encoder for town
- Label encoder for state
- List of available states
- List of towns grouped by state
- List of available house types

The Streamlit app loads this file when the prediction page starts.

---

## Main Project Files

```text
Real-estate-prediction-main/
│
├── app.py
├── predict_page.py
├── explore_page.py
├── train_model.py
├── nigeria_houses_data.csv
├── model.joblib
├── requirements.txt
├── README.md
├── homescreen.png
├── resultandlocation.png
├── EDAhouseprices.png
└── Nigeria (1).ipynb
```

---

## File Explanation

### `app.py`

This is the main entry point of the Streamlit application.

It controls the navigation between the two main pages:

- Price Prediction
- Market Insights

It also sets up the page design and sidebar.

---

### `predict_page.py`

This file contains the prediction page.

It does the following:

1. Loads the saved model from `model.joblib`.
2. Displays form inputs for property details.
3. Converts the selected text values into encoded numeric values.
4. Sends the final input into the trained model.
5. Displays the predicted house price.
6. Displays a map for the selected town and state.

---

### `explore_page.py`

This file contains the market insights page.

It does the following:

1. Loads the housing dataset.
2. Cleans the dataset.
3. Removes outliers.
4. Calculates useful summary statistics.
5. Displays charts showing price trends.

---

### `train_model.py`

This file is used to train the machine learning model.

It does the following:

1. Loads `nigeria_houses_data.csv`.
2. Cleans the data.
3. Encodes categorical columns.
4. Splits the data into training and testing data.
5. Trains a Random Forest Regressor model.
6. Prints model evaluation results.
7. Saves the trained model into `model.joblib`.

You only need to run this file if you want to retrain the model.

---

### `nigeria_houses_data.csv`

This is the dataset used by the project.

It contains Nigerian housing data used for both training and data visualisation.

---

### `model.joblib`

This is the saved trained model file.

The Streamlit application needs this file to make predictions.

Do not delete this file unless you plan to retrain the model.

---

### `requirements.txt`

This file lists the Python packages needed to run the project.

The packages include:

```text
streamlit
pandas
numpy
matplotlib
seaborn
scikit-learn
geopy
folium
streamlit-folium
joblib
```

---

### `Nigeria (1).ipynb`

This is the Jupyter Notebook used during experimentation or model development.

You do not need to open or edit this file to run the app.

---

## Important Note Before Running the Project

If the project files contain Git merge conflict markers like this:

```text
```

then the project will not run correctly until those conflict markers are removed.

Make sure files like `app.py`, `predict_page.py`, `explore_page.py`, and `README.md` do not contain those markers before running the app.

---

# How to Start and Run the Project

The steps below explain how to run the project from the beginning.

These instructions are written mainly for **Windows users using VS Code**, but the same idea works in other code editors.

---

## Step 1: Open the Project Folder in Your Code Editor

First, locate the project folder on your computer.

The folder may be named something like:

```text
Real-estate-prediction-main
```

Open this folder in your editor, such as Visual Studio Code.

Make sure you open the main project folder, not just one individual file.

---

## Step 2: Open the Integrated Terminal

Inside your code editor, right-click the project folder.

Then click:

```text
Open in Integrated Terminal
```

This will open a terminal at the bottom of the editor.

The terminal should already be inside the project folder.

You should see a path similar to this:

```powershell
PS C:\Users\YourName\Downloads\Real-estate-prediction-main>
```

This is important because the app must be run from the project root folder where `app.py`, `requirements.txt`, and `model.joblib` are located.

---

## Step 3: Create a Virtual Environment

A virtual environment keeps the project packages separate from other Python projects on your computer.

In the integrated terminal, run:

```powershell
python -m venv venv
```

This creates a new folder called:

```text
venv
```

That folder will contain the isolated Python environment for this project.

---

## Step 4: Activate the Virtual Environment

After creating the virtual environment, activate it.

On Windows PowerShell, run:

```powershell
venv\Scripts\Activate.ps1
```

If you are using Command Prompt instead of PowerShell, run:

```cmd
venv\Scripts\activate.bat
```

If activation works, you should see something like this at the beginning of your terminal line:

```text
(venv)
```

Example:

```powershell
(venv) PS C:\Users\YourName\Downloads\Real-estate-prediction-main>
```

This means the virtual environment is active.

---

## Step 5: Fix PowerShell Activation Error If Needed

Sometimes PowerShell may block the virtual environment activation script and show an error about execution policies.

If that happens, run this command:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating the virtual environment again:

```powershell
venv\Scripts\Activate.ps1
```

---

## Step 6: Install the Required Packages

Once the virtual environment is active, install the project dependencies.

Run:

```powershell
pip install -r requirements.txt
```

This installs all the packages listed in `requirements.txt`.

If you want to make sure `pip` is up to date, you can run:

```powershell
python -m pip install --upgrade pip
```

Then run the install command again:

```powershell
pip install -r requirements.txt
```

---

## Step 7: Run the Streamlit Project

After installing the packages, run the app using:

```powershell
streamlit run app.py
```

If that command does not work, use:

```powershell
python -m streamlit run app.py
```

Streamlit will start the app and show a local URL.

It usually looks like this:

```text
Local URL: http://localhost:8501
```

Open that link in your browser.

The application should now be running.

---

## Step 8: Use the Application

When the app opens in the browser, use the sidebar to navigate between pages.

You should see options similar to:

```text
Price Prediction
Market Insights
```

### To Predict a House Price

1. Go to the prediction page.
2. Select the number of bedrooms.
3. Select the number of bathrooms.
4. Select the house type.
5. Select the state.
6. Select the town.
7. Click the estimate button.
8. View the predicted house price.
9. View the location map if available.

### To Explore Market Insights

1. Go to the market insights page.
2. View the summary cards.
3. View the charts for towns, states, and house types.

---

## How to Retrain the Model

The project already includes a saved model file:

```text
model.joblib
```

Because of this, you do not need to retrain the model just to run the app.

However, if you change the dataset or want to train the model again, run:

```powershell
python train_model.py
```

This will:

1. Load the dataset.
2. Clean the data.
3. Train a new Random Forest model.
4. Save a new `model.joblib` file.

After retraining, run the Streamlit app again:

```powershell
streamlit run app.py
```

---

## Common Problems and Solutions

### Problem 1: `streamlit` is not recognized

If you see:

```text
streamlit is not recognized as the name of a cmdlet
```

Use:

```powershell
python -m streamlit run app.py
```

Also make sure your virtual environment is activated and dependencies are installed.

---

### Problem 2: `ModuleNotFoundError`

If you see an error like:

```text
ModuleNotFoundError: No module named 'streamlit'
```

It means the required packages are not installed in the active environment.

Run:

```powershell
pip install -r requirements.txt
```

---

### Problem 3: `model.joblib` not found

If you see an error saying `model.joblib` is missing, make sure the file exists in the same folder as `app.py`.

If it is missing, retrain the model:

```powershell
python train_model.py
```

---

### Problem 4: App does not run because of `<<<<<<< HEAD`

If Python shows an error near lines containing:

```text
```

then the file has unresolved Git merge conflicts.

Open the affected file and remove the conflict markers. Keep only the correct version of the code.

Files to check include:

```text
app.py
predict_page.py
explore_page.py
README.md
```

---

### Problem 5: Map does not load

The map feature depends on geocoding the selected town and state.

If the location cannot be found or there is no internet connection, the map may not load.

The prediction feature can still work even if the map does not load.

---

## Recommended Run Commands Summary

From the project root folder, run these commands:

```powershell
python -m venv venv
```

```powershell
venv\Scripts\Activate.ps1
```

```powershell
pip install -r requirements.txt
```

```powershell
streamlit run app.py
```

If Streamlit does not run directly, use:

```powershell
python -m streamlit run app.py
```

---

## Technologies Used

This project uses:

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Joblib
- Geopy
- Folium
- Streamlit-Folium

---

## Final Summary

This project is a machine learning web application for predicting Nigerian house prices. It uses a cleaned real estate dataset, trains a Random Forest regression model, and displays the result through a Streamlit interface.

The user can enter property details, receive an estimated price, and explore real estate trends through charts. The project is useful for demonstrating data cleaning, machine learning regression, model saving/loading, and interactive web app development using Streamlit.

