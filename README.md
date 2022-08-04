# yelp_scraping

## Phase 1

We will start by fetching the data of the restaurants for LA County and comparing it with the results from yelp educational datasets.

Important Git repo with Yelp dataset examples and conversion: https://github.com/Yelp/dataset-examples


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



## Phase 2

![Test Image](/images/yelp_home.png)


There are three parts to the script (or three scripts) - 

1. get_business.py - fetches the businesses in the specified area, using either the latitude and longitude boundary box of the city of the zip codes of the city (stored in file [here](zip_code_database.csv) )

2. get_reviews.py fetches the reviews, user who left the review and the owner's response to the hotels gathered from the previous step.

3. get_image_backlog.py


### Fixes

1. Reviews not populated after the html encodings were removed. Luckily, the check_in flag in yelp_reviews table was set to 2 for all these new reviews.

Function populate_missed_reviews is used to populate these reviews.

`python get_reviews.py --missed_reviews`