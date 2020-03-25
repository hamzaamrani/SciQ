# Wolfram|Alpha Show Steps API Reference:
# https://products.wolframalpha.com/show-steps-api/documentation/

import requests
import urllib.parse
import json
import base64

API_URL = 'https://api.wolframalpha.com/v2/query'
API_SIGNUP_PAGE = 'https://developer.wolframalpha.com'
KEY = 'V2WJ46-EEXEV95WXG'


class NoAPIKeyException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class waAPI(object):
    def __init__(self, key=None):
        """
        Initializes the booksAPI class with a developer key. Raises an exception if a key is not given.

        Request a key at https://developer.wolframalpha.com

        :param key: Wolfram Alpha App ID Developer Key

        """
        self.key = key
        self.response_format = 'json'

        if self.key is None:
            raise NoAPIKeyException(
                'Warning: Missing API Key. Please visit ' +
                API_SIGNUP_PAGE +
                ' to register for a key.')

    def full_results(self,
                     response_format=None,
                     key=None,
                     query=None):
        """
        Calls the API and returns a dictionary of the search results

        :param response_format: the format that the API uses for its response,
                                includes JSON (.json) and XML.
                                Defaults to '.json'.

        :param key: a developer key. Defaults to key given when the waAPI class was initialized.

        :**kwargs examples:
                        query = 'How many megabytes are in a gigabyte'
        """
        if key is None:
            key = self.key
        if response_format is None:
            response_format = self.response_format
        if query is None:
            return 'Sorry, I did not get your question.'
        else:
            url = '%s?input=%s&podstate%s&output=%s&appid=%s' % (API_URL, urllib.parse.quote(
                query), 'Result__Step-by-step+solution', response_format, key)
            r = requests.get(url)
            print(r)
            print("\n\n")
            return r.json()


class Expression(object):
    def __init__(self, query, results):
        """
        Initializes the Expression class with a results from Wolfram Alpha API.

        Request a query.
        Request a JSON results.

        :param results: Results of query from Wolfram Alpha App
        :param results: Results of query from Wolfram Alpha App

        """

        data = results['queryresult']
        pods = data['pods']

        self.query = query
        self.execution_time = data['timing']
        self.type = pods[0]['scanner']
        self.plots = []
        for i in range(len(pods[1]['subpods'])):
            base64_img = base64.b64encode(requests.get(
                pods[1]['subpods'][i]['img']['src']).content)
            self.plots.append(base64_img)
        self.alternate_forms = []
        for i in range(len(pods[2]['subpods'])):
            self.alternate_forms.append(pods[2]['subpods'][i]['plaintext'])
        self.solutions = []
        for i in range(len(pods[4]['subpods'])):
            self.solutions.append(pods[4]['subpods'][i]['plaintext'])


if __name__ == "__main__":
    api = waAPI(KEY)

    query = 'x^2+8(x-1)+89*e=7'
    results = api.full_results(query=query)

    #print(json.dumps(results, indent=2))

    # with open('example4.json') as f:
    #     results = json.load(f)

    obj = Expression(query, results)

    print(obj.query)
    print(obj.execution_time)
    print(obj.type)
    print(obj.plots)
    print(obj.alternate_forms)
    print(obj.solutions)
