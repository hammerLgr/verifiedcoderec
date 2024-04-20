# 验证码识别模型（VerifiedCodeRec）

为降低部署落地成本，接口部分以最小改动原则，在ddddocr项目基础上进行修改。感谢原作者。

## VerifiedCodeRec项目架构：

```.
├── Dockerfile          #docker file文件
├── README_CN.md        #readme文件
├── api_server.py       #接口文件
├── base
│   ├── __init__.py     #推理脚本
│   └── best.onnx       #模型文件
├── ppocr               #功能性脚本
├── requirements.txt    #依赖文件
├── tmp_imgs            #暂存传到接口的图片文件
└── tools
    └── infer
        └── utility.py  #常用功能性函数
```

## Version 1.0

### 1. 部署

使用项目中Dockerfile拉取镜像

### 2. 验证部署

浏览器输入：http://127.0.0.1:9898/ping，如返回“pong”，说明部署成功。

### 3. 应用示例

Dockerfile中的启动参数：
`CMD ["python3", "api_server.py", "--port", "9898", "--ocr"]`

--port: 可进行修改，默认保持9898
--ocr：传入此参数表示启动识别模型

调用实例：

```python
import requests
import base64
import json

# # Read image file and encode to base64
# with open("image.jpg", "rb") as image_file:
# encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
import time
start = time.time()
img_base64 = 'iVBORw0KGgoAAAANSUhE...UVORK5CYII=' # for example
# Prepare data for POST request
data = json.dumps({ "image": img_base64 })

# Send POST request to server
response = requests.post('http://127.0.0.1:9898/ocr/b64', data=data, headers={'Content-Type': 'application/json'})
print(f'time: {time.time() - start:.4f}s')

# Print the response
print(response.text)

```

输出：

第一行：推理时长

第二行：推理结果和置信度

> time: 0.3444s
> 1加4=？, 0.9989894032478333