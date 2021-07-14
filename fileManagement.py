import os, shutil
from datetime import datetime
import time

def deleteAllFiles():
    folder = '../WRSGGLSearchWebsite-master_VC/genomesearch/static/exitFiles'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

while True:
    deleteAllFiles()
    print("files deleted at " + datetime.now().strftime("%H:%M:%S"))
    time.sleep(60 * 10)