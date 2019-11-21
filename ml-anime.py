#!/usr/bin/env python3
import io
import errno
import os
import glob
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

def create_box(image, filename, objectname, verts, count):
    basename = filename.split('/')[-1].split('.')[0]
    filetype = filename.split('.')[-1]
    try:
        os.mkdir("./out/" + basename + "/")
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    draw = ImageDraw.Draw(image)
    draw.line(verts, fill="red", width=3)
    image.save("./out/" + basename + "/" + objectname + "-{}.".format(count) + filetype)




def find_objects_with_ml(f):
    client = vision.ImageAnnotatorClient()
    file_name = os.path.abspath(f)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    objects = client.object_localization(image=image).localized_object_annotations
    print('Number of objects found for {}: {}'.format(f, len(objects)))
    image = Image.open(file_name)
    x_size = image.width
    y_size = image.height
    count=1
    for object_ in objects:
        print('Found "{}": (confidence: {})'.format(object_.name, object_.score))
        verts=[]
        f_vert=None
        for vertex in object_.bounding_poly.normalized_vertices:
            if not f_vert:
                f_vert=(vertex.x * x_size, vertex.y * y_size)
            verts.append((vertex.x * x_size, vertex.y * y_size))
        verts.append(f_vert)
        create_box(image.copy(), f, object_.name, verts, count)
        count = 1 + count


def main():
    images = glob.glob("src/*.jpg") + glob.glob("src/*.png")
    for f in images:
        find_objects_with_ml(f)


if __name__ == "__main__":
    main()
