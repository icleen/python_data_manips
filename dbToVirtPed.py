import sys
from unqlite import UnQLite
import json
import base64
import os
import urllib

def image_creator(field):
    imagePath = base64.b64decode(field['source']['descriptionId'].split('_')[-1])
    n = field['values'][0]['text']
    gender = person['gender']['type'].split("/")[-1]
    di = person['id'][1:]
    # x = {di: {'ascBranchIds': [], 'data': {'image': imagePath, 'name': n, 'gender': gender, 'id': di}} }
    x = {'ascBranchIds': [], 'data': {'image': imagePath, 'name': n, 'gender': gender, 'id': int(di)}}
    images[di] = x
    # if temp < 20:
    #     print(di)

def relationship_creator(relationship):
    person1 = relationship['person1']['resourceId'][1:]
    person2 = relationship['person2']['resourceId'][1:]
    # if temp < 20:
    #     print(person1)
    if person1 in images:
        images[person1]['ascBranchIds'].append(int(person2))
        # if temp < 20:
        #     print(person1)

if __name__ == "__main__":
    database_path = sys.argv[1]
    output_path = "output"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    db = UnQLite(database_path)
    images = {}
    for k in db:

        COLLECTION_DIRECTORY = output_path + "/" + k[0]

        if not os.path.exists(COLLECTION_DIRECTORY):
            os.makedirs(COLLECTION_DIRECTORY)

        data = json.loads(k[1])
        temp = 0
        with open(COLLECTION_DIRECTORY + '/jiapu_test.js', 'w') as f:
            f.write('staticData = ')

        with open(COLLECTION_DIRECTORY + '/jiapu_test.js', 'a') as f:
            for person in data['persons']:
                for name in person['names']:
                    for nameForm in name['nameForms']:
                        for part in nameForm['parts']:
                            for field in part['fields']:
                                image_creator(field)
                                temp += 1
                        if 'fields' in nameForm:
                            for field in nameForm['fields']:
                                image_creator(field)
                                temp += 1

            temp = 0
            for relationship in data['relationships']:
                relationship_creator(relationship)
                temp += 1

            json.dump(images, f)
            f.close()

        # Download the corresponding images from familysearch
        # the file name of https://familysearch.org/ark:/61903/3:1:3QS7-L97V-ZSVT.jpg
        # will be 3-1-3QS7-L97V-ZSVT.jpg
