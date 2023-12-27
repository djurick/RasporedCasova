import codecs
import pathlib
import os
import sys
import tempfile
import time
import traceback

from model.Ogranicenja import Ogranicenja
from GenetskiAlgoritam import GenetskiAlgoritam
from HTMLraspored import HTMLRaspored


def main(file_name):
    start_time = int(round(time.time() * 1000))

    configuration = Ogranicenja()
    target_file = str(pathlib.Path().absolute()) + file_name
    configuration.parseFile(target_file)

    alg = GenetskiAlgoritam(configuration)
    print("Koriscenje genetskog algoritma:", alg, ".\n")
    alg.run()
    html_result = HTMLRaspored.getResult(alg.result)

    temp_file_path = tempfile.gettempdir() + file_name.replace(".json", ".htm")
    writer = codecs.open(temp_file_path, "w", "utf-8")
    writer.write(html_result)
    writer.close()

    seconds = (int(round(time.time() * 1000)) - start_time) / 1000.0
    print("\nCompleted in {} secs.\n".format(seconds))
    os.startfile(temp_file_path)


if __name__ == "__main__":
    file_name = "/Baza.json"
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    try:
        main(file_name)
    except:
        traceback.print_exc()

