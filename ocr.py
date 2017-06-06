import time
import requests
import operator
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64


_url = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/describe'
_key = '6f487d230e484a1ea926d569682fa8f7'
_maxNumRetries = 10


def find_dict(d, sent):
    for key, val in d.items():
        if key == "text":
            sent.append(val)
        if isinstance(val, dict):
            find_dict(val, sent)
        elif isinstance(val, list):
            find_list(val, sent)


def find_list(l, sent):
    for item in l:
        if isinstance(item, dict):
            find_dict(item, sent)
        elif isinstance(item, list):
            find_list(item, sent)



def printed_text(url_of_pic):
    headers = {
        # Request headers.
        'Content-Type': 'application/json',

        # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
        'Ocp-Apim-Subscription-Key': '6f487d230e484a1ea926d569682fa8f7',
    }

    params = urllib.parse.urlencode({
        # Request parameters. The language setting "unk" means automatically detect the language.
        'language': 'unk',
        'detectOrientation ': 'true',
    })

    # Replace the three dots below with the URL of a JPEG image containing text.
    # body = "{{'url':{} }}".format(str(url_of_pic))
    body = {'url': str(url_of_pic)}
    body = json.dumps(body, ensure_ascii=False)

    try:
        # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
        #   URL below with "westus".
        conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/ocr?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        lines = json.loads(data.decode())
        print(lines)
        sent = []
        find_dict(lines, sent)
        conn.close()
        result = ' '.join(sent)
        return result

    except Exception as e:
        result = 'Error:{}'.format(str(e))
        return result


def handwritten_text(url_of_pic):

    requestHeaders = {
        # Request headers.
        # Another valid content type is "application/octet-stream".
        'Content-Type': 'application/json',

        # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
        'Ocp-Apim-Subscription-Key': '3c6ebb23c9474c8d8d3feac651914484',
    }

    # Replace the three dots below with the URL of a JPEG image containing text.
    body = {'url': str(url_of_pic)}
    # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
    #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
    #   URL below with "westus".
    serviceUrl = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'

    # For printed text, set "handwriting" to false.
    params = {'handwriting': 'true'}

    try:
        response = requests.request('post', serviceUrl, json=body, data=None, headers=requestHeaders, params=params)
        print(response.status_code)

        # This is the URI where you can get the text recognition operation result.
        operationLocation = response.headers['Operation-Location']

        # Note: The response may not be immediately available. Handwriting recognition is an
        # async operation that can take a variable amount of time depending on the length
        # of the text you want to recognize. You may need to wait or retry this GET operation.

        time.sleep(10)
        response = requests.request('get', operationLocation, json=None, data=None, headers=requestHeaders, params=None)
        data = response.json()
        sent = []
        find_dict(data, sent)
        result = ' '.join(sent)
        return result

    except Exception as e:
        result = 'Error:{}'.format(str(e))
        return result




def main():
    result = printed_text('https://assets.imgix.net/~text?dpr=2&fm=png&txtsize=28&w=320&txtfont64=SGVsdmV0aWNhIE5ldWUgTGlnaHQ&txt64=RmFyIGZhciBhd2F5LCBiZWhpbmQgdGhlIHdvcmQgbW91bnRhaW5zLCBmYXIgZnJvbSB0aGUgY291bnRyaWVzLCB0aGVyZSBsaXZlIHRoZSBibGluZA&txtpad=0&dpr=2&txtclr=212B32')
    print(result)


if __name__ == '__main__':
    main()
