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
Data extracted form web pages are usually unstructured and non-numeric.  However, Neural Networks require numeric data for 
training. Extracted information needs to be restructured with the idea of "Bag-of-Words".   

* ### Bag of Words ###
    Bag of Words is a feature extraction technique which is usually used in Nature Language Processing (NLP).  It wildly helps in training document 
    classification, segmentation and text generation models.  Its logic is simple.   Imagining a bag that contains all the words that existed in several
    related documents.  Removed the stop words, such as "i", "we", "you", "they", etc.  We got the words which were mostly related to the topic.  
    Then we read a new document, if it contains these related words, this new document may be categorized as related.  
    In the same way, all horses that have competed in races during the past 10 years are stored in a numeric array (Bad of Horse).  Then, we have a three-dimension array that contains [Race, horse, no. of winning] which states the probability of winning of each horse. 
    This numeric array is suitable for **Neural Networks**  training.

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
3-D array which contains after data transformation: 
Vectorize train Races [no. of Race, no. of horse, no. of winning]: (17588, 16) 
</pre>

## 4. Training ##
In this project, I train the models with two difference keras layer: Dense and LSTM. Both layers are usually used in Neural Networks.  
 

### i. Dense Layer ###
Dense Layer is most commonly used with difference activation functions which suitable for difference scenario. In this project, there are 
two hidden layers.  

![dense_neural_network.png](plots%2Fdense_neural_network.png)

<pre>
Testing loss : 9.344161033630371; accuracy: 0.04831332340836525
</pre>

![plot_RacingPredictionTraining_dense.png](plots%2Fplot_RacingPredictionTraining_dense.png)

### ii. LSTM Layer ###
Long Short-Term Memory is well-designed for modeling sequences and time-series data. LSTMs are designed to overcome 
the limitations of traditional RNNs by incorporating memory cells that can maintain information over long periods.

![lstm_neural_network.png](plots%2Flstm_neural_network.png)

<pre>
Testing loss : 9.166614532470703; accuracy: 0.0014212620444595814
</pre>

![RacingPredictionTraining_LSTM.png](plots%2FRacingPredictionTraining_LSTM.png)

## 5. Output ##

