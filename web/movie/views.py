from django.shortcuts import render
import os,django
from TwitterAPI import TwitterAPI,TwitterRequestError,TwitterConnectionError
from watson_developer_cloud import AlchemyLanguageV1,WatsonException
import json
from movie.models import furious
from django.db.models import Count
from django.http import HttpResponse
from credential import consumer_key, consumer_secret, access_token_key, access_token_secret
import requests
def index1(request):
    return render(request, 'main.html')

def index2(request):
    return render(request, 'movie.html')

def add(request):

    ret1=furious.objects.filter(result='pos').aggregate(Count('id'))['id__count']
    ret2=furious.objects.filter(result='neutral').aggregate(Count('id'))['id__count']
    ret3=furious.objects.filter(result='neg').aggregate(Count('id'))['id__count']
    ret4=furious.objects.all().aggregate(Count('id'))['id__count']
    return HttpResponse('positive: '+str(ret1)+'\n'+'neutral: '+str(ret2)+'\n'+'negative: '+str(ret3)+'\n'+'sum: '+str(ret4))


def index3(request):
    url="http://text-processing.com/api/sentiment/"
    #alchemy_language = AlchemyLanguageV1(api_key=ALCH_API_KEY)
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    #print ALCH_API_KEY
    while True:
        try:
            iterator = api.request('statuses/filter', {'track':'fast and furious','lang':'en'}).get_iterator()
            for item in iterator:
                if 'text' in item and 'user'  in item:
                    try:
                        print json.loads(requests.post(url, data='text='+str(item['text'])).content.decode('utf-8'))["label"]
                        furious.objects.create(
                            name=item['user']['id'],
                            content=item['text'],
                            result=json.loads(requests.post(url, data='text='+str(item['text'])).content.decode('utf-8'))["label"])
                    except:
                        continue

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
        except WatsonException:
            pass
