import json

# 读取并解析 JSON 文件
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return None

# 提取 rack_id 和 sample_id
def extract_rack_and_sample_ids(data):
    racks_samples = []
    
    # 遍历 tasks 列表，循环获取信息
    for task in data.get("tasks", []):
        for rack in task.get("racks", []):
            rack_id = rack.get("rack_id")
            for sample in rack.get("samples", []):
                sample_id = sample.get("sample_id")
                
                # 将 rack_id 和 sample_id 添加到列表
                racks_samples.append({
                    "rack_id": rack_id,
                    "sample_id": sample_id
                })
                
    return racks_samples

# 保存提取的数据到新的 JSON 文件
def save_to_json(data, output_file_path):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"数据已成功保存到 {output_file_path}")
    except IOError as e:
        print(f"Error: Could not write to file '{output_file_path}'. {e}")

# 示例：读取并打印 rack_id 和 sample_id
def main():
    file_path = 'received_data.json'  # 你的 JSON 文件路径
    extracted_file_path = 'extracted_data.json'  # 输出 JSON 文件路径
    data = load_json(file_path)
    
    if data:
        racks_samples = extract_rack_and_sample_ids(data)
        print("提取的 rack_id 和 sample_id 如下:")
        # for item in racks_samples:
        #     print(f"rack_id: {item['rack_id']}, sample_id: {item['sample_id']}")
        save_to_json(racks_samples, extracted_file_path)

if __name__ == "__main__":
    main()
