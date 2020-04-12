import logging
import threading
import requests
import os

def download(url=None):
    if (url is None):
        return False
    filename = os.path.basename(url)
    logging.warning(f"writing image {filename}")
    ff = requests.get(url)
    tipe = dict()
    tipe['image/png']='png'
    tipe['image/jpg']='jpg'
    tipe['image/jpeg']='jpeg'

    content_type = ff.headers['Content-Type']
    if (content_type in list(tipe.keys())):

        fp = open(f"{filename}","wb")
        fp.write(ff.content)
        fp.close()
        logging.warning(f"writing {filename} success")
    else:
        return False

if __name__=='__main__':
    gambar=['https://f0.pngfuel.com/png/244/839/black-and-white-striped-woman-with-red-lips-illustration-beauty-parlour-hairstyle-artificial-hair-integrations-hair-care-hair-png-clip-art.png',
            'https://upload.wikimedia.org/wikipedia/commons/5/57/PT05_ubt.jpeg',
            'https://onlinejpgtools.com/images/examples-onlinejpgtools/mouse.jpg']
    threads = []
    for i in range(3):
        t = threading.Thread(target=download, args=(gambar[i],))
        threads.append(t)

    for thr in threads:
        thr.start()