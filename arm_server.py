# import rospy
from flask import Flask, request, jsonify
import json
from datetime import datetime
from std_msgs.msg import String
import os
import threading
import subprocess

app = Flask(__name__)
@app.route('/receive_arm_node', methods=['POST'])
def receive_arm_node():
    if request.method == 'POST':
        data = request.get_json()
        
        aruco_to_capture = parse_rack_data(data)

        print(aruco_to_capture)

        return jsonify({'message': 'Data received successfully'})  

#将 extracted_data数据 换成 机械臂 能用的数据
def parse_rack_data(data_list):
    data_dict = {}

    # Loop through the data_list to process each rack
    for item in data_list:
        # Extract rack_id and sample_id
        rack_id = item["rack_id"]
        sample_id = int(item["sample_id"])

        # Extract rack number from rack_id (e.g., 'rack_1' -> 1)
        rack_number = int(rack_id.split('_')[1])

        # If the rack_number is not in the dictionary, add it with an empty list
        if rack_number not in data_dict:
            data_dict[rack_number] = []

        # Append the sample_id to the corresponding rack_number
        data_dict[rack_number].append(sample_id)

    # Sort the sample_id values for each rack
    for key in data_dict:
        data_dict[key] = sorted(data_dict[key])

    return data_dict

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True) #服务器绑定的 IP 地址
