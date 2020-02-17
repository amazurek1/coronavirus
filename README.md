# coronavirus

# Spread of the coronavirus epidemic as covered by the news media using NLP
## Aviva Mazurek & Ben Johnson-Laird

# Methodology & Goals

## Goals
Can the progression of the virus be tracked using NLP using newspaper articles. E.g.:
Identity the cities that the virus travelled too
Can the virus symptoms be inferred from the articles

## Methodology
Data source N.Y. Times with time period (Jan-Feb 2020)
Extensible framework using Spacy allows matched articles to be filtered through successive query pipes
N.Y Times API for article URl’s (about coronavirus) → scraped content → NLP for sentences with virus and geographic locations and symptoms


We used the NY Times API to pull all articles since the beginning of january that had coronavirus in it. The Nytimes API actually doesnt let you pull text, so we had to get the URLs, and then scrape the contents of every article, we actually had to run that program overnight


Our exploratory data analysis eventually informed the regression results we got.
We did a lot of EDA

Number of artiches mentions for symptoms with mentions greater than 15 correlated closely with the CDC reported list of main symptoms i.e. 
* Fever
* Cough
* Shortness of breath

Number of mentions for cities with mentions >15 

N.Y Times Mentions and Number of Deaths by Date
We were wondering if the number of ny times mentions of coronavirus per day corrolated with the deaths per day so on this graph, the red series are cumulative deaths, and the blue series is ny times mentions of the coronavirus, so each one of these points are cumulative deaths or nytimes mentions per day, and the graph behavior is really similar so we decided to do linear regression

Would be interesting to see a virus thats old - like sars to see if they level off

## Nearly Linear Relationship Between Article Mentions and Deaths by Date
Y = 0.53x + 28.75
R2 = 0.978
Slightly sigmoidal

## Linear Relationship Between Article Mentions and Cases by Date

Y = 25.17x + 1054.25
R2 = 0.989
Slightly sigmoidal

## Heatmap of Virus Mentions in N.Y Times articles
## Consistent with The Economist’s heatmap

# Conclusions & Future Work
* Map out hot spots of infectious diseases geographically
* Determine symptoms of infectious diseases
* NLP program features
* Reusable framework could be used to track future emergent diseases
* Map out other infectious diseases to further validate model (i.e SARS)
* Differences in newspaper coverages (i.e geographic bias, scaremongering)
