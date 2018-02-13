#!/usr/bin/env python

import json
import urllib.request
import os

response = urllib.request.urlopen("https://downloads.mesosphere.com/assets/icon-processed.json")

processed = json.load(response)

def get_icon_by_format(icons, sformat):
    for icon in icons:
        if icon['format'] == sformat:
            return icon
    return None

for package in processed:
    name = str(package['name'])
    icons = package['icons']

    path = "repo/packages/{}/{}".format(name[0].capitalize(), name)
    if os.path.isdir(path):
        versions = os.listdir(path)
        for version in versions:
            resourcepath = "{}/{}/resource.json".format(path, version)
            if os.path.exists(resourcepath):

                with open(resourcepath, 'r+') as f:
                    data = json.load(f)
                    if 'images' in data.keys():
                        if "icon-small" in data['images']:
                            data['images']['icon-small'] = get_icon_by_format(icons, "small")['url']
                        if "icon-medium" in data['images']:
                            data['images']['icon-medium'] = get_icon_by_format(icons, "medium")['url']
                        if "icon-large" in data['images']:
                            data['images']['icon-large'] = get_icon_by_format(icons, "large")['url']
                    f.seek(0)        # <--- should reset file position to the beginning.
                    json.dump(data, f, indent=2)
                    f.truncate()     # remove remaining part
