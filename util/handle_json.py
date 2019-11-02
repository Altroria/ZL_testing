#coding=utf-8
import json
import os
file_path = os.path.join(os.getcwd() + "/config/" + "cookie.json")


class HandleJson(object):
    def load_json(self):
        with open(file_path) as fp:
            data = json.load(fp)
        for cookie in data:
            return ({
                'domain': cookie['domain'],
                "httpOnly": cookie['httpOnly'],
                "name": cookie['name'],
                "path": cookie['path'],
                "secure": cookie['secure'],
                "value": cookie['value']
            })

    def get_data(self):
        return self.load_json()

    def write_data(self, data):
        with open(file_path, 'w') as fp:
            fp.write(json.dumps(data) + '\n')


handle_json = HandleJson()
