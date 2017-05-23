import zipfile
import sys
import json
import os


if __name__ == "__main__":
    path_to_zip_file = sys.argv[1]
    output_path = "testingFiles"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(output_path)
    zip_ref.close()

    unzipped = path_to_zip_file.split('/')[-1]
    unzipped = unzipped.split('-')[0]

    images = []
    texts = []
    data = []

    basePath = output_path + '/' + unzipped
    imageFolders = os.listdir(basePath)
    imageFolders.sort()
    for imageFolder in imageFolders:
        infos = os.listdir(basePath + '/' + imageFolder)
        infos.sort()
        # print(len(images), len(texts), imageFolder)
        assert(len(images) == len(texts))
        for info in infos:
            infoType = info.split('.')[-1]
            # print(basePath + '/' + imageFolder + '/' + info)
            if '(' not in info:
                if infoType == 'txt':
                    texts.append(basePath + '/' + imageFolder + '/' + info)
                if infoType == 'jpg':
                    images.append(basePath + '/' + imageFolder + '/' + info)

    # print(len(images), len(texts))
    assert(len(images) == len(texts))
    for i in range(len(images)):
        data.append({'image_path': images[i], 'gt': texts[i]})

    with open(output_path + '/' + unzipped + '.json', 'w') as f:
        json.dump(data, f)
        f.close()
