import urllib.parse
import requests
from urllib.parse import urlsplit
from urllib.parse import urljoin
import argparse
import json
import datetime

def getHistory(history):
    print(history)
    saveHistory = []
    for x in range(0, len(history)):
        print(history[x].status_code)
        historyInfo = {
            'status':history[x].status_code,
            'content':history[x].text,
            'cookies':requests.utils.dict_from_cookiejar(history[x].cookies),
            'headers':history[x].headers,
            'finalURL':history[x].url
        }
        saveHistory.append(historyInfo)
    return saveHistory

if __name__ == '__main__':
    try:
        # update_tld_names()
        argParser = argparse.ArgumentParser(description='Save request information for a website.')
        argParser.add_argument('url', nargs=1, help='The url of the website (including http/s)')
        argParser.add_argument('-o', dest='o', nargs=1, help='Output as JSON file with name specified.')

        args = argParser.parse_args()

        result = {}

        result['startTime'] = datetime.datetime.now()

        url = args.url[0]
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        timeout = 8

        try:
            page = requests.get(url,headers=headers,timeout=timeout,verify=False)
            result['page'] = {}
            requestInfo = {
                'history':getHistory(page.history),
                'status':page.status_code,
                'content':page.text,
                'cookies':requests.utils.dict_from_cookiejar(page.cookies),
                'headers':page.headers,
                'finalURL':page.url
            }
            result['page'] = requestInfo
        except requests.ConnectionError:
            result['error'] = True
            result['errorDesc'] = 'ConnectionError'
        except requests.TooManyRedirects:
            result['error'] = True
            result['errorDesc'] = 'TooManyRedirects'
        except requests.ReadTimeout:
            result['error'] = True
            result['errorDesc'] = 'ReadTimeout'


        result['stopTime'] = datetime.datetime.now()
        with open(args.o[0], 'w') as dumpfile:
            json.dump(result, dumpfile, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print('[main]',e)
    finally:
        print('Done.')
        exit()
