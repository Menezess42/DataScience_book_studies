import tweepy
import credentials
from collections import defaultdict

# Substituir pelo seu Bearer Token
BEARER_TOKEN = credentials.BEARER_TOKEN

# Autenticação com OAuth2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def search_tweets(query, max_results=42):
    dict_ = defaultdict(list)
    # Busca no endpoint /2/tweets/search/recent
    response = client.search_recent_tweets(
        query=query,
        tweet_fields=['author_id', 'created_at'],
        max_results=max_results
    )

    tweets = response.data
    if not tweets:
        print("Nenhum tweet encontrado.")
        return
    
    for i, tweet in enumerate(tweets, start=1):
        print(f"{i}. ({tweet.created_at}) Autor ID: {tweet.author_id} - Texto: {tweet.text}\n")
        dict_[tweet.author_id][tweet.author_id] = tweet.author_id
        dict_[tweet.author_id][tweet.created_at] = tweet.created_id
        dict_[tweet.author_id][tweet.text] = tweet.text

    with open(f'twits.json', 'w') as f:
        s = json.dumps(dict_, indent=4)
        s = re.sub(r'\n +([0-9-\]])', r' \1', s)
        f.write(s)
        

if __name__ == '__main__':
    termo = '"data science"'
    search_tweets(termo, max_results=11)

