import os
import zipfile


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


zipf = zipfile.ZipFile('my_zipfile.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir('directory_to_zip/', zipf)
zipf.close()