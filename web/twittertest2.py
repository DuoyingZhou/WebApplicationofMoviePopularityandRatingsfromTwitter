import os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()

from TwitterAPI import TwitterAPI,TwitterRequestError,TwitterConnectionError
from watson_developer_cloud import AlchemyLanguageV1
import json
from movie.models import furious
from django.db.models import Count

ALCH_API_KEY = 'bbe73189d3c87a070cea5b35ea48615cf55504c9'
alchemy_language = AlchemyLanguageV1(api_key=ALCH_API_KEY)

consumer_key = 'NIQpSybvhSANztWysLINzu4qn'
consumer_secret = '8udQR80ylsGUaTsj3l2YF9vvfKxFxNZO1SA78HuVgWjV01TVO3'
access_token_key = '839610378145378304-LV4rTa0hiS6UEEm9fvUtRXV5f0vYX2Q'
access_token_secret = 'FMFTc4IQnVVqwb56Q3oC3ybwXYCCuhuQlMg9w4AykXUca'
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

while True:
    try:
        iterator = api.request('statuses/filter', {'track':'The Fate of the Furious','lang':'en'}).get_iterator()
        for item in iterator:
            if 'text' in item and 'user'  in item:
                furious.objects.create(
                    name=item['user']['id'],
                    content=item['text'],
                    result=alchemy_language.sentiment(text=item['text'])["docSentiment"]["type"])
                print alchemy_language.sentiment(text=item['text'])["docSentiment"]["type"],': ',furious.objects.filter(result=alchemy_language.sentiment(text=item['text'])["docSentiment"]["type"]).aggregate(Count('id'))
                print item['user']['id'],item['text'],alchemy_language.sentiment(text=item['text'])["docSentiment"]["type"],'\n'
            elif 'disconnect' in item:
                event = item['disconnect']
                if event['code'] in [2,5,6,7]:
                    # something needs to be fixed before re-connecting
                    raise Exception(event['reason'])
                else:
                    # temporary interruption, re-try request
                    break
    except TwitterRequestError as e:
        if e.status_code < 500:
            # something needs to be fixed before re-connecting
            pass
        else:
            # temporary interruption, re-try request
            pass
    except TwitterConnectionError:
        # temporary interruption, re-try request
        pass