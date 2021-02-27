import requests
import argparse
import json
import datetime
from bs4 import BeautifulSoup

def scanText(text):
    soup = BeautifulSoup(text, "lxml")
    item = {}
    item['nicetext'] = soup.prettify()
    inputTags = soup.find_all("input")
    scriptTags = soup.find_all("script")
    linkTags = soup.find_all("link")
    formTags = soup.find_all("form")
    iframeTags = soup.find_all("iframe")
    item['inputHtml'] = []
    item['scriptHtml'] = []
    item['linkHtml'] = []
    item['formHtml'] = []
    item['iframeHtml'] = []
    for input in inputTags:
        type = input['type'] if input.has_attr('type') else 'none';
        value = input['value'] if input.has_attr('value') else 'none';
        placeholder = input['placeholder'] if input.has_attr('placeholder') else 'none';
        item['inputHtml'].append({'value':value,'placeholder':placeholder,'type':type})
    for script in scriptTags:
        src = script['src'] if script.has_attr('src') else 'none';
        type = script['type'] if script.has_attr('type') else 'none';
        item['scriptHtml'].append({'source':src,'type':type})
    for link in linkTags:
        src = link['src'] if link.has_attr('src') else 'none';
        type = link['type'] if link.has_attr('type') else 'none';
        item['linkHtml'].append({'source':link['href'],'type':type})
    for form in formTags:
        action = form['action'] if form.has_attr('action') else 'none';
        method = form['method'] if form.has_attr('method') else 'none';
        target = form['target'] if form.has_attr('target') else 'none';
        item['inputHtml'].append({'method':method,'target':target,'action':action})
    for iframe in iframeTags:
        src = iframe['src'] if iframe.has_attr('src') else 'none';
        sandbox = iframe['sandbox'] if iframe.has_attr('sandbox') else 'none';
        csp = iframe['csp'] if iframe.has_attr('csp') else 'none';
        referrerpolicy = iframe['referrerpolicy'] if iframe.has_attr('referrerpolicy') else 'none';
        srcdoc = iframe['srcdoc'] if iframe.has_attr('srcdoc') else 'none';
        item['iframeHtml'].append({'source':src,'sandbox':sandbox,'csp':csp,'referrerpolicy':referrerpolicy,'srcdoc':srcdoc})
    textSplit = text.split('\n')
    item['textSplit'] = textSplit
    item['loginLoc'] = text.find('login')
    item['inputLoc'] = text.find('input')
    return item


if __name__ == '__main__':
    try:
        # update_tld_names()
        argParser = argparse.ArgumentParser(description='See if a website is phishing.')
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
            result['textScan'] = scanText(page.text)
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
        if args.o:
            with open(args.o[0], 'w') as dumpfile:
                json.dump(result, dumpfile, indent=4, sort_keys=True, default=str)
        else:
            print('Please specify an output file with "-o filename". Shutting down.')
            exit()

    except Exception as e:
        print('[main]',e)
        traceback.print_stack()
        traceback.print_exception()
    finally:
        print('Done.')
        exit()
