import requests
import json

# # 定义要发送的 JSON 数据
# data = {
#     "inspection_id": "001",
#     "map_id": "001",
#     "map_name": "001号地图",
#     "name": "fc6528ce-4127-468f-ab7f-fd121784cbb5",
#     "time": "2024-10-26 15:00:00",
#     "tasks": [
#         {
#             "racks": [
#                 {
#                     "rack_id": "rack1",
#                     "samples": [
#                         {
#                             "sample_id": "sample1.1",
#                             "collection_task": {
#                                 "sample_name": "1849360661742436354",
#                                 "parameters": {
#                                     "format": "JPEG",
#                                     "resolution": "1920x1080"
#                                 }
#                             }
#                         },
#                         {
#                             "sample_id": "sample1.2",
#                             "collection_task": {
#                                 "sample_name": "1849360661742436355",
#                                 "parameters": {
#                                     "format": "JPEG",
#                                     "resolution": "1920x1080"
#                                 }
#                             }
#                         },
#                         {
#                             "sample_id": "sample1.3",
#                             "collection_task": {
#                                 "sample_name": "1849360661742436356",
#                                 "parameters": {
#                                     "format": "JPEG",
#                                     "resolution": "1920x1080"
#                                 }
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     "rack_id": "tongyx.rack.NO.A1",
#                     "samples": [
#                         {
#                             "sample_id": "tongyx.NO.A1",
#                             "collection_task": {
#                                 "sample_name": "1849360661742436352",
#                                 "parameters": {
#                                     "format": "JPEG",
#                                     "resolution": "1920x1080"
#                                 }
#                             }
#                         },
#                         {
#                             "sample_id": "tongyx.NO.A2",
#                             "collection_task": {
#                                 "sample_name": "1849360661742436353",
#                                 "parameters": {
#                                     "format": "JPEG",
#                                     "resolution": "1920x1080"
#                                 }
#                             }
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
# }

data = {
    "inspection_id": "93b11bf7-90f2-449f-9380-e1051b528fb9",
    "map_name": "地图001",
    "map_id": "001",
    "time": 1731403958000,
    "tasks": [{
        "racks": [{
            "rack_id": "rack_1",
            "samples": [{
                "sample_id": "0",
                "collection_task": {
                    "sample_name": "1854093306030252033",
                    "parameters": {
                        "resolution": "1920x1080",
                        "format": "JPEG"
                    }
                }
            }]
        },
        {
            "rack_id": "rack_2",
            "samples": [{
                "sample_id": "8",
                "collection_task": {
                    "sample_name": "1854093306030252032",
                    "parameters": {
                        "resolution": "1920x1080",
                        "format": "JPEG"
                    }
                }
            }]
        },
        {
            "rack_id": "rack_3",
            "samples": [{
                "sample_id": "19",
                "collection_task": {
                    "sample_name": "1854093306030252032",
                    "parameters": {
                        "resolution": "1920x1080",
                        "format": "JPEG"
                    }
                }
            }]
        }]
    }]
}

# data = [
#     {
#         "rack_id": "rack_1",
#         "sample_id": "0",
#         "rack_world_location": {
#             "position": [0.40393909, -0.889733337, 0.0],
#             "orientation": [0, 0, -0.7473709219392113, 0.6643783295127215]
#         }
#     },
#     {
#         "rack_id": "rack_2",
#         "sample_id": "0",
#         "rack_world_location": {
#             "position": [1, 2, 3],
#             "orientation": [4, 5, 6, 7]
#         }
#     }
# ]


# data={
#     "action": "start_all"
# } 

# 发送 POST 请求
url = 'http://192.168.3.4:8080/receive_json'  # 服务器端接收 JSON 数据的 URL
# url = 'http://192.168.3.4:8080/start_task_queue'
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)

# 打印响应内容
print(response.text)