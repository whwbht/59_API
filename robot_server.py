#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import json
from datetime import datetime
from std_msgs.msg import String
import os
import threading
import subprocess

app = Flask(__name__)


########################## 机器人任务接收 #####################################################
@app.route('/receive_json', methods=['POST']) 
def receive_json():
    if request.method == 'POST':
        data = request.get_json()

        # 保存 JSON 数据到文件
        if data:
            save_to_json(data,'received_data.json')

            # 获取当前系统时间并格式化为 ISO 8601 格式
            current_time = datetime.utcnow().isoformat() + "Z"

            # 创建返回reponse的 JSON 响应，使用接收的数据填充响应内容
            response_data = {
            "data": {
                "name": data.get("name", "NULL"), #有数据就填充，默认NULL
                "inspection_id": data.get("inspection_id", "NULL"),
                "map_name": data.get("map_name", "NULL"),
                "status": data.get("status", "pending"),
                "submitted_time": data.get("time", "NULL"), #任务队列提交时间
                "errorCode": data.get("errorCode", None)
            },
            "msg": "Task queue is in progress",
            "timestamp": current_time, #响应时间
            "successed": data.get("successed", True)
            }

            #解析 received_data.json数据 与 本地文件配对 解析出 导航点坐标
            # 从文件中读取坐标数据
            with open('Global_location_sample.json', 'r', encoding='utf-8') as file:
                location_data = json.load(file)
            racks_samples_patrol = match_and_extract_coordinates(data,location_data)
            #保存 extracted_data.json
            save_to_json(racks_samples_patrol,'extracted_data.json')

            # 返回 JSON 响应
            return jsonify(response_data), 200
        
        else:
            return jsonify({"error": "******No JSON data received*********."}), 400    

# 匹配 json字典格式 获取 坐标点信息
def match_and_extract_coordinates(data1, data2):
    # 创建一个字典，方便快速查找第二个 JSON 文件中每个样本的位置数据
    location_map = {}
    for item in data2:
        rack_id = item.get("rack_id")
        sample_id = item.get("sample_id")
        if rack_id and sample_id:
            location_map[(rack_id, sample_id)] = {
                "rack_world_location": item.get("rack_world_location"),
                # "sample_location": item.get("sample_location")
            }

    # 结果列表
    result = []

    # 遍历第一个 JSON 文件的 racks 和 samples
    for task in data1.get('tasks', []):
        for rack in task.get('racks', []):
            rack_id = rack.get("rack_id")
            for sample in rack.get("samples", []):
                sample_id = sample.get("sample_id")
                sampe_name= sample['collection_task']['sample_name']

                # 查找对应的坐标位置
                location = location_map.get((rack_id, sample_id))
                if location:
                    # 将样本的坐标信息添加到结果
                    result.append({
                        "rack_id": rack_id,
                        "sample_id": sample_id,
                        "rack_world_location": location.get("rack_world_location"),
                        "sampe_name":sampe_name,
                        # "parameters":
                        # "sample_location": location.get("sample_location")
                    })
                else :
                    print("error:Matching is error,not find racks and samples locations")    
    
    return result  

# 保存提取的数据到新的 JSON 文件
def save_to_json(data, output_file_path):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"数据已成功保存到 {output_file_path}")
    except IOError as e:
        print(f"错误: 不能写入 '{output_file_path}'. {e}")




########################## 机器人任务开始 #####################################################################################
@app.route('/start_task_queue', methods=['POST'])
def start_task_queue():
    if request.method == 'POST':
        data = request.get_json()

        if data and data.get("action") == "start_all":
            current_time = datetime.utcnow().isoformat() + "Z"

            # 创建响应数据
            response_data = {
            "msg": "All inspection tasks have been started successfully.",
            "timestamp": current_time,
            "successed": True
            }  
            
            # 设置.sh文件的路径
            sh_file = '/home/ris/patrol_ws/建图.sh'  # 请将此路径替换为你的 .sh 文件路径
            # 在后台线程中执行脚本
            threading.Thread(target=run_shell_script, args=(sh_file,)).start()

            # 返回 JSON 响应
            return jsonify(response_data), 200
        else:
            # 如果接收的数据不正确，返回错误信息
            return jsonify({"error": "*******Invalid action or no JSON data received******."}), 400
        
# 运行sh文件
def run_shell_script(sh_file):
    # 确保.sh文件具有执行权限
    if not os.access(sh_file, os.X_OK):
        print(f"文件 {sh_file} 没有执行权限。尝试添加执行权限...")
        os.chmod(sh_file, 0o755)  # 给文件添加执行权限

    # 使用subprocess模块运行.sh文件
    try:
        result = subprocess.run(['bash', sh_file], check=True, text=True, capture_output=True)
        print("脚本输出:", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"执行脚本时出错: {e}")
        print(f"错误输出: {e.stderr}")

########################### 采样ZIP文件接收 ######################
@app.route('/loadZip', methods=['POST'])
def loadZip():
    # 配置保存目录
    BASE_UPLOAD_FOLDER = '/home/whw/'  # 存放上传文件的目录
    os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # 检查文件类型（可选）
    if not file.filename.endswith('.zip'):
        return jsonify({"error": "Uploaded file is not a ZIP file"}), 400
    
    # 确保只提取文件名
    file_name = os.path.basename(file.filename)

    # 从客户端获取自定义子目录
    destination_dir = request.form.get('destinationDir', '')  # 例如 'project_a/subfolder'
    # 检查是否指定了目标子目录
    if destination_dir:  # 如果 destination_dir 不为空
        save_folder = os.path.join(BASE_UPLOAD_FOLDER, destination_dir)  # 拼接目标保存路径
        print("用户自定义路径 destinationDir")
    else:  # 如果没有指定 destination_dir
        save_folder = BASE_UPLOAD_FOLDER  # 使用默认基础保存目录
        print("默认路径保存2")

    # 确保保存目录存在
    os.makedirs(save_folder, exist_ok=True)
    # 定义文件完整保存路径
    file_path = os.path.join(save_folder, file_name)
    file.save(file_path)
    print(f"File saved to {file_path}")

    return jsonify({"message": "File uploaded successfully", "saved_path": file_path})


if __name__ == '__main__':

    app.run(host='192.168.144.187', port=8080, debug=True) #服务器绑定的 IP 地址
