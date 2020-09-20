# Datamining for Item Trade

This project systematically mines data from RL Trading by taking a user's offer list, desired list, and interpreting their post using NLP to store each item's worth into a database. If a user offers an item for another instead of RL Trading currency, the database can be used to label an item with its estimated numerical value. Optimized costs and prices are then extracted for every possible item.

Features from each user are extracted from their listing and profile account to be judged by a trained bot detector. Using a labeled data set derived from contacting individual users, phishing bots and unscrupulous traders can be detected with machine learning. Future work will involve getting metrics of true/false positives/negatives.

## Import Dependencies

keras, 
pandas, 
numpy, 
re, 
matplot-lib, 
beautifulsoup4, 
pickle, 
math, 
time, 
datetime, 
copy, 
os, 
requests

## RL Trading

Running RLTrading/RLTrading.py will prompt the user for the settings defined in SavedQueries.py

1. Optimize: This action will take the most recent posts for all items on trading site and optimize by best cost and price. If a pickled database exists, it will be loaded in and new items will be highlighted.

2. Delete Pickle: This action deletes the existing database.

3. Data Mine: This action will load the existing database and saves all unique user posts locally, which can be used as a training set to improve bot detection from SBotDetection.

4. Watch: This action will save a specific item's listings and append it to a file, so prices over time can be monitored and visualized using RLPlot.py

# Steam Bot Detection

Once data is mined from RLTrading, SBotDetection extracts the features from each account. Metadata, profile statistics, poster comments, and user content language features are stored into a data set. Gathering statistical significance for labeled scammers is currently a work in progress. The flaws from rule-based bot detection are proving to be overcome by machine learning classification predictions.

