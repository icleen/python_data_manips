import sys
from unqlite import UnQLite
import json
import base64
import os
import urllib

def bbox_output(field):
    array = field['source']['qualifiers'][0]['value'].split(',')
    bbox = "[[" + array[0] + "," + array[1] + "],[" + array[2] + "," + array[3] + "]]"
    output = base64.b64decode(field['source']['descriptionId'].split('_')[-1]) + "\t" + bbox + "\t" + field['values'][0]['text'] + "\t" + str(bbox_id) + "\t" + person['id'] + "\n"
    f.write(output.encode('utf-8'))
    # print output

def person_output(field):
    array = field['source']['qualifiers'][0]['value'].split(',')
    bbox = "[[" + array[0] + "," + array[1] + "],[" + array[2] + "," + array[3] + "]]"
    output = person['id'] + "\t" + field['values'][0]['text'] + "\t" + base64.b64decode(field['source']['descriptionId'].split('_')[-1]) + "\t" + person['gender']['type'].split("/")[-1] + "\n"
    f.write(output.encode('utf-8'))
    # print output

def relationship_output(relationship):
    output = relationship['person1']['resourceId'] + "\t" + relationship['type'].split("/")[-1] + "\t" + relationship['person2']['resourceId'] + "\n"
    f.write(output.encode('utf-8'))
    # print output

if __name__ == "__main__":
    database_path = sys.argv[1]
    output_path = "output"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    db = UnQLite(database_path)
    for k in db:

        COLLECTION_DIRECTORY = output_path + "/" + k[0]

        if not os.path.exists(COLLECTION_DIRECTORY):
            os.makedirs(COLLECTION_DIRECTORY)

        data = json.loads(k[1])
        # print data.keys()
        # print json.dumps(data, sort_keys=True, indent=4)
        with open(COLLECTION_DIRECTORY + '/bboxes.txt', 'w') as f:
            bbox_id = 0
            for person in data['persons']:
                for name in person['names']:
                    for nameForm in name['nameForms']:
                        for part in nameForm['parts']:
                            for field in part['fields']:
                                bbox_output(field)
                                bbox_id += 1
                        if 'fields' in nameForm:
                            for field in nameForm['fields']:
                                bbox_output(field)
                                bbox_id += 1
            f.close()

        with open(COLLECTION_DIRECTORY + '/persons.txt', 'w') as f:
            person_id = 0
            for person in data['persons']:
                for name in person['names']:
                    for nameForm in name['nameForms']:
                        for part in nameForm['parts']:
                            for field in part['fields']:
                                person_output(field)
                                person_id += 1
                        if 'fields' in nameForm:
                            for field in nameForm['fields']:
                                person_output(field)
                                person_id += 1
            f.close()

        with open(COLLECTION_DIRECTORY + '/relationships.txt', 'w') as f:
            for relationship in data['relationships']:
                relationship_output(relationship)
            f.close()

        IMAGE_DIRECTORY = output_path + "/" + k[0] + "/image"

        if not os.path.exists(IMAGE_DIRECTORY):
            os.makedirs(IMAGE_DIRECTORY)

        # Download the corresponding images from familysearch
        # the file name of https://familysearch.org/ark:/61903/3:1:3QS7-L97V-ZSVT.jpg
        # will be 3-1-3QS7-L97V-ZSVT.jpg

        urls = open(COLLECTION_DIRECTORY + '/bboxes.txt', 'r')
        for line in urls:
            url = line.split("\t")[0]
            name = url.split("/")[-1].replace(":","-")
            print name

            filename = os.path.join(IMAGE_DIRECTORY,name)

            if not os.path.isfile(filename):
                print (filename)
                try:
                    urllib.urlretrieve(url, filename)
                except Exception as inst:
                    print(inst)
                    print('\tEncountered unknown error.')
