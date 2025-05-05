import credentials
from twython import Twython
import webbrowser


CONSUMER_KEY = credentials.key
CONSUMER_SECRET = credentials.secret


def get_acces_token():
# Conf a temp client to recover a authentication URL
    temp_client = Twython(CONSUMER_KEY, CONSUMER_SECRET)
    temp_creds = temp_client.get_authentication_tokens()
    url = temp_creds['auth_url']

# Access URL to autorize the aplication and obtain the PIN
    print(f'Go visit {url} and get the PIN code and paste it below')
    webbrowser.open(url)
    PIN_CODE = input('please enter the PIN code: ')

# We use the PIN_CODE to obtain the real tokens
    auth_client = Twython(CONSUMER_KEY,
                          CONSUMER_SECRET,
                          temp_creds['oauth_token'],
                          temp_creds['oauth_token_secret'])
    final_step = auth_client.get_authorized_tokens(PIN_CODE)
    ACCESS_TOKEN = final_step['oauth_token']
    ACCESS_TOKEN_SECRET = final_step['oauth_token_secret']
    with open("credentials.py", "a") as f:
         f.write(f"ACCESS_TOKEN = '{ACCESS_TOKEN}'\nACCESS_TOKEN_SECRET = '{ACCESS_TOKEN_SECRET}'")

    return ACCESS_TOKEN, ACCESS_TOKEN_SECRET


# Start a new instance of Twython with this
def create_twitter_instance(ACCESS_TOKEN=credentials.ACCESS_TOKEN,
                            ACCESS_TOKEN_SECRET=credentials.ACCESS_TOKEN_SECRET):
    twitter = Twython(CONSUMER_KEY,
                      CONSUMER_SECRET,
                      ACCESS_TOKEN,
                      ACCESS_TOKEN_SECRET)
    return twitter


def search_on_twitter():
    tw = create_twitter_instance()
    i = 0
    for status in tw.search(q='"data science"')["status"]:
        user = status["user"]["screen_name"]
        text = status["text"]
        i+=1
        print(f"i:{i} {user}: {text}\n")
        if 1==30:
            break


if __name__ == '__main__':
    #_,_ = get_acces_token()
    search_on_twitter()

