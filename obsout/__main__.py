import json
import requests

def main():
 
    headers = {
        # Already added when you pass json=
        # 'content-type': 'application/json',
        'accept': 'application/json',
    }

    json_data = {
        'token': 'ol_api_NeDDfQEANwPyJkmCn0LJqkma8YCYEgsMJkqtmt',
        'offset': 0,
        'limit': 25,
    }

    response = requests.post('https://wiki.local.flaskforge.com/api/collections.list', headers=headers, json=json_data)
    # print(response.text)
    collections = json.loads(response.text)
    print("ID: {}\nName: {}".format(collections['data'][0]['id'], collections['data'][0]['name']))

if __name__ == "__main__":
    main()