# Indian-movie-celebrities-Personality-Database
This is a program to create a database which contains the personality traits of the Indian Bollywood Celebs

I did the following to create the database:

1) Getting a list of twitters handles of celebrities:
  There are already websites available which provide the info about the twitter handles of various bollywood celebs, I just picked one of 
  the websites and extracted all the twitter handles and kept it in a list.
 
 2) Creating repo of tweets of the Celebs:
    For this I used the twitter API, Kindly google search on creating twitter API to create your own API key and then you can easilty extract the 
    tweets. After getting the tweets I performed the basic cleaning so that it is ready for next step.
 
 3) Creating repo of personlity traits for each celeb:
 
      I used the IBM's personality insights to create a model which will draw out personality insights from the tweets.I have covered 
      5 important personality traits: Openness,Conscientiousness,Extraversion,Agreeableness,Emotional_range. Every celeb has been scored against 
      these 5 traits
      
  4) Extracting Images of Each celeb:
      Since we only want one image for each celeb and we also know that each celeb has his/her wikipedia page, hence we directly extracted the
      image from wikipedia.
      
  
  After performing the above steps, I just aggregated all the list into one dataframe using pandas and then extracted in the excel format
