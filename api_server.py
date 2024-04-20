# encoding=utf-8
import argparse
import base64
import json
import os 
import base
from flask import Flask, request
import tools.infer.utility as utility
from ppocr.utils.logging import get_logger
import re 

logger = get_logger()
args = utility.parse_args()
app = Flask(__name__)

class Server(object):
    def __init__(self, ocr=True):
        self.ocr_option = ocr
        self.ocr = None
        if self.ocr_option:
            print("Char-Recognize Server Start!")
            self.ocr = base
        else:
            print("Char-Recognize Server Stop! To start with parameter  --ocr")

    def classification(self, img: bytes):
        if self.ocr_option:
            return self.ocr.recognize_res(image_dir=img)
        else:
            raise Exception("char-recognize model unuse")

server = Server(ocr=args.ocr)

def get_img(request, dir, img_type='file', img_name='image'):
    try:
        if img_type == 'b64':
            img = request.get_data() 
            dic = json.loads(img)
            img = base64.b64decode(dic.get(img_name).encode())  
        else:
            dic = json.loads(img)
            img = dic.get(img_name).encode()
   
        target = dir + os.sep + str(os.getpid()) + ".png"
        file = open(target, "wb")
        file.write(img)
        file.close()
        return target

    except Exception as e: 
        logger.info("e is {}".format(e))
        pass

def set_ret(result, ret_type='text'):
    list = re.sub("\(|\)|\'", "", str(result)).split(",")[1:]
    result = ",".join(list)
    if ret_type == 'json':
        if isinstance(result, Exception):
            return json.dumps({"status": 200, "result": "", "msg": str(result)}, ensure_ascii=False)
        else:
            return json.dumps({"status": 200, "result": result, "msg": ""}, ensure_ascii=False)
    else:
        if isinstance(result, Exception):
            return ''
        else:
            return str(result).strip()


@app.route('/<opt>/<img_type>', methods=['POST'])
@app.route('/<opt>/<img_type>/<ret_type>', methods=['POST'])
def ocr(opt, img_type='file', ret_type='text'):
    dir = "./tmp_imgs"
    if not os.path.exists(dir):
        os.mkdir(dir)
    try:
        img = get_img(request, dir, img_type)
        if opt == 'ocr':
            result = server.classification([img])
            if os.path.exists(img):
                os.remove(img)
        else:
            raise f"<opt={opt}> is invalid"
        return set_ret(result, ret_type)
    except Exception as e:
        print(e)
        return set_ret(e, ret_type)

@app.route('/ping', methods=['GET'])
def ping():
    return "pong"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=args.port)