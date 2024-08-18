import tkinter as tk
from tkinter import messagebox
import pickle
import requests
import re
import numpy as np
from adblockparser import AdblockRules

# Constants
URL_PKL_PATH = "C:/Users/Samira/Downloads/mladblocker-master/mladblocker-master/data/url_block_map.pkl"
MODEL_PKL_PATH = "C:/Users/Samira/Downloads/mladblocker-master/mladblocker-master/data/trained_model.pkl"
FEAT_PKL_PATH = "C:/Users/Samira/Downloads/mladblocker-master/mladblocker-master/data/features.pkl"
EL_PATH = "C:/Users/Samira/Downloads/mladblocker-master/mladblocker-master/easylist/easylist_22-12-18.txt"
URL_PATH = "C:/Users/Samira/Downloads/mladblocker-master/mladblocker-master/data/URLs_to_adblock.csv"

# Load EasyList rules
try:
    with open(EL_PATH, encoding='utf-8') as f:
        content = f.readlines()
    rule_strings = [rule.strip() for rule in content]
    rules = AdblockRules(rule_strings)
except FileNotFoundError:
    raise FileNotFoundError(f"EasyList file not found at {EL_PATH}")

# Initialize global variables
clf = None
features = None

def load_model_and_features():
    global clf, features
    try:
        with open(MODEL_PKL_PATH, 'rb') as model_file:
            clf = pickle.load(model_file)
        with open(FEAT_PKL_PATH, 'rb') as features_file:
            features = pickle.load(features_file)
        messagebox.showinfo("Success", "Model and features loaded successfully.")
    except Exception as e:
        messagebox.showerror("Loading Error", f"Error loading model or features: {e}")
        root.quit()  # Close the application if loading fails

def check_url(url):
    try:
        # Validate URL
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def predict_ad():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    # Check for HTTPS
    if url.startswith("http://"):
        messagebox.showinfo("Prediction Result", "The ad is: Not Safe (Uses HTTP)")
        return

    if not check_url(url):
        messagebox.showwarning("Invalid URL", "The website URL is not valid or cannot be reached.")
        return

    if clf is None or features is None:
        messagebox.showwarning("Model Error", "Model and features are not loaded.")
        return

    # Convert URL to feature matrix
    fMat = np.zeros(len(features))
    tokens = re.findall(r"[\w']+", url)
    for token in tokens:
        if token in features:
            fMat[features[token]] += 1
    fMat = [fMat]

    # Predict using the model
    prediction = clf.predict(fMat)[0]
    if prediction > 0:
        result_text = "Not Safe (Malicious)"
    else:
        result_text = "Safe (Not Malicious)"
    
    messagebox.showinfo("Prediction Result", f"The ad is: {result_text}")

def block_ad():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    if not check_url(url):
        messagebox.showwarning("Invalid URL", "The website URL is not valid or cannot be reached.")
        return

    messagebox.showinfo("Block Action", "This URL has been marked for future blocking reference.")

# Set up GUI
root = tk.Tk()
root.title("Adblocker GUI")

# Layout configuration
root.geometry("500x300")

# Load model and features
load_model_and_features()

# Create and place widgets
url_label = tk.Label(root, text="Enter URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

predict_button = tk.Button(root, text="Predict Safety", command=predict_ad)
predict_button.pack(pady=10)

block_button = tk.Button(root, text="Block Ad", command=block_ad)
block_button.pack(pady=10)

# Start GUI loop
root.mainloop()
