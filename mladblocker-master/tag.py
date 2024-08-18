from adblockparser import AdblockRules
from collections import Counter
import pickle

# Constants

EL_PATH = r"C:\Users\Samira\Downloads\mladblocker-master\mladblocker-master\easylist\easylist_22-12-18.txt"
URL_PATH = r"C:\Users\Samira\Downloads\mladblocker-master\mladblocker-master\data\URLs_to_adblock.csv"
URL_MAP_PKL_PATH = r"C:\Users\Samira\Downloads\mladblocker-master\mladblocker-master\data\url_block_map.pkl"

# Load EasyList file

print("Loading EasyList rules...")

with open(EL_PATH, encoding='utf-8') as f:
    content = f.readlines()

rule_strings = [rule.strip() for rule in content]

# Parse rules

print("Parsing rules...")

rules = AdblockRules(rule_strings)

# Load url dataset

print("Loading URLs...")

urls = []

with open(URL_PATH, 'r', encoding='utf-8') as infile:
    for line in infile:
        url, _ = line.strip().split("\t")
        # Ensure this slicing is correct for your data format
        url = url[1:-2]  # Adjust as needed
        urls.append(url)

print(len(urls), "URLs loaded!")

# Make a mapping from urls to whether they should be blocked

print("Parsing URLs...")

block_map = Counter()

for url in urls:
    block_map[url] = rules.should_block(url)

print("Finished!")

# Save mapping to pickle

with open(URL_MAP_PKL_PATH, 'wb') as output:  # Overwrites any existing file.
    pickle.dump(block_map, output, pickle.HIGHEST_PROTOCOL)
