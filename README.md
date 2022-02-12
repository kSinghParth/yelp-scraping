# yelp_scraping

## Phase 1

We will start by fetching the data of the resteraunts for LA County and comparing it with the rsults from yelp educational datasets.

Important Git repo with Yelp dtaset examples and conversion: https://github.com/Yelp/dataset-examples


To access the API of yelp, I have registered an app on the yelp developer support website. Accordingly, I have received an API key with a certain usage limit.

### AppName on yelp 
Yelp-Scraping-USC-2022

### Api Usage
![Api Usage](/images/api_usage.png)

### Coverage of the current boundary for LA

![Api Usage](/images/coverage.png)

### Instalation

#### Step 1
 `pip install -r requirements.txt`

 #### Step 2
 `python main.py --businesses --reviews`