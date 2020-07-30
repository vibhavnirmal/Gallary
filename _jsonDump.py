import json


class saveEncodings:
    def __init__(self):
        super(saveEncodings, self).__init__()

    def saveData(self, filename, faceLocation, theEncodings, name='unknown'):
        data = {}
        data['image_filename'] = []
        data['face_location'] = []
        data['face_encodings'] = []

        data['image_filename'].append({'filename': filename,})
        data['face_location'].append({'faceLocation': faceLocation,})
        data['face_encodings'].append({'encoding': theEncodings,})
        # data['people'].append({'name': name,})

        return data

    def saveName(self, name, location, theOriginalDataDict):
        if theOriginalDataDict is not {}:
            # for encoding in theOriginalDataDict['face_encodings']:
            for i in theOriginalDataDict['face_location'][0]['faceLocation']:
                # print(location)
                # print(i)
                if location == i:
                    print("True")
                # theOriginalDataDict['face_encodings'].append({'name': name,})

    def saveJSONFile(self, data, filename='test'):
        with open(str(filename)+'.json', 'w') as outfile:
            json.dump(data, outfile)