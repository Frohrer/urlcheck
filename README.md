# urlcheck
urlcheck is a website scanning tool, similar to urlscan.io but worse. The goal is to scan a website very quickly, save a screenshot and check for login forms.

urlcheck consists of 3 separate python scripts:
* selpy.py for providing the headless screenshot using selenium chromedriver
* phishFinder.py for checking for inputs, scripts, links, iframes etc that could be used to extract login information from a page
* requestinfo.py for checking the http requests, redirects, session and cookies

These scripts can be used standalone or with the included node server for queuing and combining results.


## install

1. Install chromedriver and selenium dependencies. This process varies from time to time but this should give you a good starting point: https://chromedriver.chromium.org/getting-started
2. Install node.js if you need it. Then run `npm install` or install dependencies from the package.js manually
3. Install Python 3.5 or higher and the following dependencies: 
```
pip install selenium
pip install Pillow
pip install requests
pip install urllib3
pip install beautifulsoup4
```

Warning, the node server accepts incoming connections on port 8080. It will wait for a scan request, queue the corresponding python packages, then return the results. The image is returned as base64 string.
Example request object (javascript)
```
data = {
		siteURL: 'example.com',
		urlHref: 'https://example.com/',
		settings: {
			lighthouseFR:false,
		}
	}
```
lighthouseFR is a separate package found here: https://github.com/Frohrer/lighthouse2
