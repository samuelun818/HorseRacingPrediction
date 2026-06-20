# Horse Racing Prediction #
1. Background 
2. Data Source 
3. Preparation
4. Training 
5. Output

## 1. Background ##
Horse racing is one of the most popular sports in the world.  In Hong Kong, there are over 80 race meetings per season.
Some fo them are world-class  international racing events.  The most notably the LONGINES Hong Kong International Races 
attracts top horses, trainers and jockeys from around the world. These famed Hong Kong races are broadcast internationally and 
are enabled oversea wagering which engage fans to enjoy the thrill of every race.   

With the information of every races in last 10 years, this project is trying to use Deep Learning Technology to predict 
the race result.  

## 2. Data Source ##
All the data are directly downloaded on the web site of Hong Kong Jockey Club, www.HKJC.com. Hong Kong Jockey Club is the 
only authorized organization to operate horse racing and racecourses in Hong Kong.  Races results are extract from its web 
site directly.  

## 3. Preparation ##
Data extracted form web pages are usually unstructured and non-numeric.  However, Neural Neworks require to use numeric data for training.
Extracted information need to be restructured with the idea of "Bag-of-Words".  

* ### Bag of Words ###
    Bag of Words is a feature extraction technique which is usually used in Nature Language Processing (NLP).  It wildly helps in training document 
    classification, segmentation and text generation models.  Its logic is simple.   Imagining a bag that contains all the words existed in several
    related documents.  Removed the stop words, such as "i", "we", "you", "they", etc.  We got the words which mostly related to the topic.  
    Then we read a new document, if it contains these related words, this new document may be categorized as related.  
    In the same way, all horses that have competed in races during the past 10 years are stored in a numeric array (Bad of Horse).  Then, we have a three dimension array contains [Race, horse, no. of winning] which state the probability of winning of each horse. 
    This numeric array is suitable for **Neural Neworks**  training.

<pre>
Before data transformation, non-numeric data extracted from web page. 
'Race' : [{ 
  'date': '2026/01/01', 
  'venue': 'ST', 
  'race_no': '1', 
  'horses': ['SMILING EMPEROR', 'JOLLY JUMPER', 
              'PANDA LEGEND', 'IRON LEGION', 
              'SMART TRIO', 'WINDICATOR FAMILY', 
              'SHINE BRIGHT', 'DRACO', 'DRAGON SUNRISE', 
              'GANGNAM STAR', 'ISLAND GOLDEN', 'SILVER KING', 
              "HARRY'S HERO", 'STRONGEST BOY', '', ''
            ], 
  'win': 'IRON LEGION'
}]
</pre>

<pre>
3-D array which contains after data tranformation: 
Vectorize train Races [no. of Race, no. of horse, no. of winning]: (17588, 16) 
</pre>



## 4. Training ##

## 5. Output ##