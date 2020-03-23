from file import File
import json
import logging

py = File()

class mainMachine:
    def proses(self,string_to_process, data):
        s = string_to_process
        cstring = s.split(" ")
        try:
            command = cstring[0].strip()
            if (command=='upload'):
                logging.warning("upload")
                nama = cstring[1].strip()
                py.Upload(nama,data)
                return "OK"
            elif (command=='list'):
                logging.warning("list")
                hasil = py.List()
                hasil={"file":hasil}
                return json.dumps(hasil)
            elif (command=='download'):
                logging.warning("download")
                nama = cstring[1].strip()
                hasil = py.Download(nama)

                return hasil
            else:
                return "ERRCMD!!"
        except:
            return "ERROR"