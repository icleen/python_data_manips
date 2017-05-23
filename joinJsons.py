import sys
import json
import os

if __name__ == "__main__":
    path_to_json1 = sys.argv[1]
    path_to_json2 = sys.argv[2]
    output_path = "testingFiles"
    fileName = sys.argv[3]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    data = []

    f = open(path_to_json1, 'r')
    objects = json.load(f)
    for j in objects:
        data.append(j)


    f = open(path_to_json2, 'r')
    objects = json.load(f)
    for j in objects:
        data.append(j)


    with open(output_path + '/' + fileName + '.json', 'w') as f:
        json.dump(data, f)
        f.close()
