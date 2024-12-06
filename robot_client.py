import requests

########### 机器人上传图片信息 ####################

def send_file_to_server(file_path, server_url):
    # 打开文件，准备上传
    with open(file_path, 'rb') as file:
        # 准备文件数据，'file' 是服务器端接收文件的字段名
        files = {'file': (file_path, file, 'application/zip')}#'application/zip' 正确的 MIME 类型，表示文件是 ZIP 格式的
        
        # 如果需要传递其他属性，可以添加 data 字段
        data = {'destinationDir': destination_dir}  # 例如传递用户名或文件描述

        # 向服务器发送 POST 请求，上传文件
        response = requests.post(server_url, files=files, data=data)
        
        # 打印服务器响应
        if response.status_code == 200:
            print("File uploaded successfully.")
            print(f"Response: {response.text}")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")

# 示例调用
file_path = '/home/whw/20241120115422.zip'  # 替换为你的文件路径
# server_url = 'http://75b6c06e.r29.cpolar.top/loadZip'  # 替换为目标服务器地址和端口
server_url = 'http://192.168.78.242:8080/loadZip'  # 替换为目标服务器地址和端口
destination_dir='59_API'  # 指定服务器端保存的子目录
send_file_to_server(file_path, server_url)
