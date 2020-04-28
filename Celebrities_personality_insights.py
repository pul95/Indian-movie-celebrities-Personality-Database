# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 00:10:49 2020

@author: 91907
"""
import requests
import bs4
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1
import re
import emoji
import contractions
from autocorrect import spell
from ibm_watson import PersonalityInsightsV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import wikipedia
import pandas as pd

#Twitter Data Extraction
auth_params = {
    'app_key':'exKc7XezqVbTe1oO7KjWyYL6L',
    'app_secret':'1ZDVwkzRul9zVeDjxoCPsDZVtCX36agj9BcOnJX62tA2RN7a73',
    'oauth_token':'1254062767721418752-YFPuQGTVZYxSHhqYE7EHp8iWGXorkk',
    'oauth_token_secret':'AZVsXXvMmNGmUisIkAKo54DxvmDyuU5uGZR3spJbnfSH3'
}

auth = OAuth1 (
    auth_params['app_key'],
    auth_params['app_secret'],
    auth_params['oauth_token'],
    auth_params['oauth_token_secret']
)

list_of_tweets_celebs = []
# url according to twitter API
url_rest = "https://api.twitter.com/1.1/search/tweets.json"

#list of twitter handles of famous bollywood celebrities
List_handles = ['@aamirkhan', '@AapkaAbhijeet','@juniorbachchan', '@aditiraohydari', '@AdityaRoyKapoor', '@AftabShivdasani', '@ajaydevgn', '@AjazkhanActor', '@akshaykumar', '@Zafarsays', '@aliaa08', '@SrBachchan', '@AmritaRao', '@amuarora', '@AnilKapoor', '@anjanasukhani', '@The_AnuMalik', '@Anupsonicp', '@AnupamPkher', '@basuanurag', '@IAmAnushka', '@AnushkaSharma', '@arbaazSkhan', '@apshaha', '@rampalarjun', '@arrahman', '@ArshadWarsi', '@ashabhosle', '@AshishChowdhry', '@AshmitPatel', '@ashwinmushran', '@itsaadee', '@atul_kulkarni', '@Ayeshatakia', '@ayushmannk', '@bipsluvurself', '@bomanirani', '@Bruabdullah', '@IChitrangda', '@ChunkyThePanday', '@CelinaJaitly', '@TheBakraMan', '@DabbooRatnani', '@dalermehndi', '@deepikapadukone', '@dhanushkraja', '@deespeak', '@DianaPenty', '@DibakarBanerjee', '@DinoMorea9', '@divyadutta25', '@EhsaanSEL', '@emraanhashmi', '@TheFarahKhan', '@khanff', '@FarOutAkhtar', '@GAUAHAR_KHAN', '@gauravkapur', '@geneliad', '@GOLDIEBEHL', '@GulPanag', '@gurruchoudhary', '@HimeshOfficial', '@iHrithik', '@humasqureshi', '@eeshatweets', '@jaavedjaaferi', '@Jackie_Shroff', '@Asli_Jacqueline', '@Javedakhtarjadu', '@TheJohnAbraham', '@iam_juhi', '@iKabirBedi', '@kabirkhankk', '@Kailashkher', '@kalkikanmani', '@kamaalrkhan', '@kangna_ranaut', '@KapilSharmaK9', '@karanjohar', '@kkundra', '@karan009wahi', '@kayoze', '@kenghosh', '@konkonas', '@kapoorkkunal', '@kunalkohli', '@KushalT2803', '@LaraDutta', '@mangeshkarlata', '@HaydonLisa', '@Lisaraniray', '@LuvSinha', '@mbhandarkar268', '@MadhuriDixit', '@MaheshNBhatt', '@MallikaLA', '@mandybedi', '@ManishMalhotra1', '@ManishPaul03', '@BajpayeeManoj', '@MikaSingh', '@milindrunning', '@Minissha_Lamba', '@MiraPagliNair', '@GodseMugdha', '@shiekhspear', '@nanditadas', '@NargisFakhri', '@NehaDhupia', '@NeilNMukesh', '@nikhilchinapa', '@nikitindheer', '@OmiOneKenobe', '@ParineetiChopra', '@Payal_Rohatgi', '@PoojaB1972', '@poonamdhillon', '@iPoonampandey', '@1Prachidesai', '@prakashraaj', '@babbarprateik', '@realpreityzinta', '@PritishNandy', '@priyankachopra', '@PulkitSamrat', '@punitdmalhotra', '@Purab_Kohli', '@RahulBose1', '@R_Khanna', '@raimasen', '@mrrajatkapoor', '@superstarrajini', '@rakhisawant', '@RGVzoomin', '@ramkapoor1973', '@RandeepHooda', '@RannvijaySingha', '@RanveerOfficial', '@RanvirShorey', '@_ravidubey', '@Riteishd', '@ritesh_sid', '@riyasen24', '@ActorMadhavan', '@rohansippy', '@rohitroy500', '@RonitBoseRoy', '@RonnieScrewvala', '@roshanabbas', '@salim_merchant', '@BeingSalmanKhan', '@SalmanYKhan', '@reddysameera', '@duttsanjay', '@satishkaushik2', '@singer_shaan', '@AzmiShabana', '@iamsrk', '@shahidkapoor', '@Shankar_Live', '@TheSharmanJoshi', '@shazahnpadamsee', '@shekharkapur', '@SherlynChopra', '@TheShilpaShetty', '@ShirishKunder', '@shivaajisatam', '@ShraddhaKapoor', '@shreyaghoshal', '@shreyastalpade1', '@shrutihaasan', '@Actor_Siddharth', '@S1dharthM', '@sonakshisinha', '@sonamakapoor', '@sonunigam', '@Sophie_Choudry', '@SubhashGhai1', '@SunidhiChauhan5', '@SunnyLeone', '@sureshnmenon', '@thesushmitasen', '@sussannekroshan', '@TanishaaMukerji', '@bombaysunshine', '@iTIGERSHROFF', '@TusshKapoor', '@udaychopra', '@Varun_dvn', '@pathakvinay', '@thevirdas', '@VishalDadlani', '@vivek_oberoi', '@vrajeshhirjee', '@wajidkhan7', '@YamiGautam_YG', '@asliyoyo']
list_celebs = ['Aamir Khan',  'Abhijeet Sawant',  'Abhishek Bachchan',  'Aditi Rao Hydari',  'Aditya Roy Kapoor',  'Aftab Shivdasani',  'Ajay Devgn',  'Ajaz Khan',  'Akshay Kumar',  'Ali Zafar',  'Alia Bhatt',  'Amitabh Bachchan',  'Amrita Rao',  'Amrita Arora',  'Anil Kapoor',  'Anjana Sukhani',  'Anu Malik',  'Anup Soni',  'Anupam Kher',  'Anurag Basu',  'Anushka Manchanda',  'Anushka Sharma',  'Arbaaz Khan',  'Archana Puran Singh',  'Arjun Rampal',  'A. R. Rahman',  'Arshad Warsi',  'Asha Bhosle',  'Ashish Chowdhary',  'Ashmit Patel',  'Ashwin Mushran',  'Atif Aslam',  'Atul Kulkarni',  'Ayesha Takia Azmi',  'Ayushmann Khurrana',  'Bipasha Basu',  'Boman Irani',  'Bruna Abdullah',  'Chitrangada Singh',  'Chunky Pandey',  'Celina Jaitly',  'Cyrus Broacha',  'Dabboo Ratnani- ',  'Daler Mehndi',  'Deepika Padukone',  'Dhanush',  'Dia Mirza',  'Diana Penty',  'Dibakar Banerjee',  'Dino Morea',  'Divya Dutta',  'Ehsaan Noorani',  'Emraan Hashmi',  'Farah Khan',  'Fardeen Khan',  'Farhan Akhtar',  'Gauhar Khan',  'Gaurav Kapur',  'Genelia Deshmukh',  'Goldie Behl',  'Gul Panag',  'Gurmeet Choudhary',  'Himesh Reshammiya',  'Hritik Roshan',  'Huma Qureshi',  'Isha Koppikar',  'Jaaved Jaaferi',  'Jackie Shroff',  'Jacqueline Fernandez',  'Javed Akhtar',  'John Abraham',  'Juhi Chawla',  'Kabir Bedi',  'Kabir Khan',  'Kailash Kher',  'Kalki Koechlin',  'Kamaal R Khan',  'Kangana Ranaut',  'Kapil Sharma',  'Karan Johar',  'Karan Kundra',  'Karan Wahi',  'Kayoze Irani',  'Ken Ghosh',  'Konkona Sen Sharma',  'Kunal Kapoor',  'Kunal Kohli',  'Kushal Tandon',  'Lara Dutta Bhupathi',  'Lata Mangeshkar',  'Lisa Haydon',  'Lisa Ray',  'Luv Sinha',  'Madhur Bhandarkar',  'Madhuri Dixit-Nene ',  'Mahesh Bhatt',  'Mallika Sherawat',  'Mandira Bedi',  'Manish Malhotra',  'Manish Paul',  'Manoj Bajpayee',  'Mika Singh',  'Milind Soman',  'Minissha Lamba',  'Mira Nair',  'Mughda Godse',  'Mushtaq Sheikh',  'Nandita Das',  'Nargis Fakhri',  'Neha Dhupia',  'Neil Nitin Mukesh',  'Nikhil Chinapa',  'Nikitin Dheer',  'Omi Vaidya',  'Parineeti Chopra',  'Payal Rohatgi',  'Pooja Bhatt',  'Poonam Dhillon',  'Poonam Pandey',  'Prachi Desai',  'Prakash Raj',  'Prateik Babbar',  'Preity Zinta',  'Pritish Nandy',  'Priyanka Chopra',  'Pulkit Samrat',  'Punit Malhotra',  'Purab Kohli',  'Rahul Bose',  'Rahul Khanna',  'Raima Sen',  'Rajat Kapoor',  'Rajinikanth',  'Rakhi Sawant',  'Ram Gopal Varma',  'Ram Kapoor',  'Randeep Hooda',  'Rannvijay Singha',  'Ranveer Singh',  'Ranvir Shorey',  'Ravi Dubey',  'Riteish Deshmukh',  'Ritesh Sidhwani',  'Riya Sen',  'R. Madhavan',  'Rohan Sippy',  'Rohit Roy',  'Ronit Roy ',  'Ronnie Screwvala',  'Roshan Abbas',  'Salim Merchant',  'Salman Khan',  'Salman Yusuff Khan',  'Sameera Reddy',  'Sanjay Dutt',  'Satish Kaushik',  'Shaan',  'Shabana Azmi',  'Shah Rukh Khan',  'Shahid Kapoor',  'Shankar Mahadevan',  'Sharman Joshi',  'Shazahn Padamsee',  'Shekhar Kapur',  'Sherlyn Chopra',  'Shilpa Shetty',  'Shirish Kunder',  'Shivaji Satam',  'Shraddha Kapoor',  'Shreya Ghoshal',  'Shreyas Talpade',  'Shruti Haasan',  'Siddharth',  'Sidharth Malhotra',  'Sonakshi Sinha',  'Sonam Kapoor',  'Sonu Nigam',  'Sophie Choudry',  'Subhash Ghai',  'Sunidhi Chauhan',  'Sunny Leone',  'Suresh Menon',  'Sushmita Sen',  'Sussanne K Roshan',  'Tanishaa Mukerji',  'Teejay Sidhu',  'Tiger Shroff',  'Tusshar Kapoor',  'Uday Chopra',  'Varun Dhawan',  'Vinay Pathak',  'Vir Das',  'Vishal Dadlani',  'Vivek Oberoi',  'Vrajesh Hirjee',  'Wajid Khan',  'Yami Gautam',  'Yo Yo Honey Singh']
for twitter_handles in List_handles:
# getting rid of retweets in the extraction results and filtering all replies to the tweet often uncessary for the analysis
    q = twitter_handles +' -filter:retweets -filter:replies' # Twitter handle of celebrities

# count : no of tweets to be retrieved per one call and parameters according to twitter API
    params = {'q': q, 'count': 100, 'lang': 'en',  'result_type': 'mixed'}
    results = requests.get(url_rest, params=params, auth=auth)

    tweets = results.json()

    messages = [BeautifulSoup(tweet['text'], 'html5lib').get_text() for tweet in tweets['statuses']]
    list_of_tweets_celebs.append(messages)

def clean_tweet(tweet):
    #Removing Hashtags
    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet).split())
    #Removing URLs from tweet
    tweet = ' '.join(re.sub("(\w+:\/\/\S+)", " ", tweet).split())
    #Removing punctuations
    tweet = re.sub(r"#(\w+)", ' ', tweet, flags=re.MULTILINE)
    tweet = ' '.join(re.sub("(@[A-Za-z0–9]+)|([0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
    #lowercase
    tweet = tweet.lower()
    #remove contractions
    tweet = contractions.fix(tweet)
    #converting emojis into words
    tweet = emoji.demojize(tweet)
    #handling spelling errors
    tweet = ' '.join([spell(w) for w in tweet.split()])
    return tweet

cleaned_list_of_tweets = []
for tweets in list_of_tweets_celebs:
    temp=[]
    for tweet in tweets:
      tweet = clean_tweet(tweet)
      temp.append(tweet)
    cleaned_list_of_tweets.append(".".join(temp))
    
    
#Personality_Insights:

authenticator = IAMAuthenticator('o4xWNkxbznsrSZG92ewoJgDaBN-8oXZYN_hobDvYbVKr')
personality_insights = PersonalityInsightsV3(
    version='2017-10-13',
    authenticator=authenticator
)

personality_insights.set_service_url('https://api.eu-gb.personality-insights.watson.cloud.ibm.com/instances/07ebbe78-34a1-4099-a58f-dd7cf5589801')

Openness = []
Conscientiousness = []
Extraversion = []
Agreeableness = []
Emotional_range = []
for tweet in cleaned_list_of_tweets:
    if len(tweet) >= 100: #Minimum length of the combination of tweets should be minimum 100 characters to run personality insights
        profile = personality_insights.profile(tweet,accept='application/json').get_result()
        temp = {trait['name']:trait['percentile']for trait in profile['personality']}
        Openness.append(temp['Openness'])
        Conscientiousness.append(temp['Conscientiousness'])
        Extraversion.append(temp['Extraversion'])
        Agreeableness.append(temp['Agreeableness'])
        Emotional_range.append(temp['Emotional range'])
    else:
        Openness.append('NA')
        Conscientiousness.append('NA')
        Extraversion.append('NA')
        Agreeableness.append('NA')
        Emotional_range.append('NA')

#Extracting Images from wikipedia:
    
WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return 0

Image_list = []
for celeb_name in list_celebs:
    wiki_image = get_wiki_image(celeb_name)
    Image_list.append(wiki_image)    

Celebrity_db = {'Name':list_celebs,'Image':Image_list,'Openness':Openness,'Conscientiousness':Conscientiousness,'Extraversion':Extraversion,'Agreeableness':Agreeableness,'Emotional range':Emotional_range}

Celeb_db = pd.DataFrame(Celebrity_db)

#Final Databse of list of celebrities with their personality traits
Celeb_db.to_csv(r'Path\Celebrity_database.csv', index = True)
