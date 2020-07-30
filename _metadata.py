import json, glob, os, piexif
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


class ImageMetaData:
    def __init__(self):
        super(ImageMetaData, self).__init__()

    def change_meta_data(self, image):
        im = Image.open(image)
        exif_dict = piexif.load(im.info["exif"])

        # exif_bytes = piexif.dump(exif_dict)
        # im.save("newfile.png", "png", exif=exif_bytes)

    def all_meta_data(self, image):
        myPsnlD = {}
        imagePIL = Image.open(image)
        Lat, Lon = self.get_lat_lon(self.get_exif_data(imagePIL))
        myPsnlD["latitude"] = Lat
        myPsnlD["longitude"] = Lon
        pr = json.dumps(TAGS)
        newD = json.loads(pr)
        try:
            exif_dict = piexif.load(image)
            thumbnail = exif_dict.pop("thumbnail")
        except ValueError:
            exif_dict = {}
        # makerData = exif_dict.pop("MakerNote")
        # if thumbnail is not None:
            # with open("thumbnail.jpg", "wb+") as f:
                # f.write(thumbnail)

        for ifd_name in exif_dict:
            for key in exif_dict[ifd_name]:
                if ifd_name == "GPS":
                    gpsKey = GPSTAGS[key]
                    gpsValue = exif_dict[ifd_name][key]
                    myPsnlD[gpsKey] = gpsValue
                elif ifd_name == "Interop":
                    if key == 1:
                        interKey = "InteroperabilityIndex"
                        interValue = exif_dict[ifd_name][key]
                        myPsnlD[interKey] = interValue
                else:
                    exifKey = newD[str(key)]
                    if exifKey == "MakerNote":
                        pass
                    else:
                        exifValue = exif_dict[ifd_name][key]
                        myPsnlD[exifKey] = exifValue

        return(myPsnlD)

    def get_exif_data(self, image):
        """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
        exif_data = {}
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

        return exif_data

    def _get_if_exist(self, data, key):
        if key in data:
            return data[key]

        return None

    def _convert_to_degress(self, value):
        """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    def get_lat_lon(self, exif_data):
        """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
        lat = None
        lon = None

        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]

            gps_latitude = self._get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = self._get_if_exist(gps_info, 'GPSLatitudeRef')
            gps_longitude = self._get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = self._get_if_exist(gps_info, 'GPSLongitudeRef')

            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self._convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":
                    lat = 0 - lat

                lon = self._convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    lon = 0 - lon

        return lat, lon


if __name__ == "__main__":
    p = ImageMetaData()
    image = r"F:\mobile\MOTO MEM CARD DATA 18NOV\Download\IMG_20181016_000943.jpg"
    ExifDataDict = p.all_meta_data(image)
    print(p.change_meta_data(image))
    # print(ExifDataDict)
