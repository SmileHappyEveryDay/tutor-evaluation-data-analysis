import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # 用于进度条
from threading import Lock
from getopenaires import analyze_evaluation

# 进度条和计数器
lock = Lock()

# 存储文件路径
output_filename = "expanded_comments_data.txt"

# 读取存储文件，并解析已处理过的记录
def load_processed_records():
    if os.path.exists(output_filename):
        processed = {}
        with open(output_filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                records = content.split("\n\n")
                for record in records:
                    try:
                        data = json.loads(record)
                        key = (data["university"], data["supervisor"])
                        processed[key] = data
                    except json.JSONDecodeError:
                        continue
        return processed
    else:
        # 如果文件不存在，返回空字典
        return {}

# 追加新记录到存储文件
def append_record_to_file(record):
    with lock:  # 确保多线程下安全访问文件
        with open(output_filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, indent=4))
            f.write("\n\n")  # 使用两个换行符作为记录间隔

# 处理单条记录
def process_record(record, processed_records_dict):
    key = (record["university"], record["supervisor"])
    
    # 如果记录已存在，则跳过处理
    if key in processed_records_dict:
        return
    
    # 扩展处理记录
    expanded_record = analyze_evaluation(record)
    
    # 将扩展后的记录追加到文件中
    append_record_to_file(expanded_record)
    
    # 更新进度条
    with lock:
        pbar.update(1)

MAX_WORKER = 50  # 10
# 多线程处理数据
def process_data_multithreaded(records, processed_records_dict):
    with ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        futures = [executor.submit(process_record, record, processed_records_dict) for record in records]
        for future in as_completed(futures):
            try:
                future.result()  # 获取结果，确保异常被捕获
            except Exception as e:
                print(f"处理记录时出错: {e}")

# 主程序逻辑
def main():
    global pbar

    # 读取输入数据
    input_filename = "merged_comments_data.json"
    with open(input_filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 加载已处理的记录
    processed_records_dict = load_processed_records()

    # 计算总数和已处理的记录数
    total_records = len(data)
    processed_count = len(processed_records_dict)  # 已处理的记录数
    print("processed_count:", processed_count, ", total_records:", total_records)
    pending_records = [record for record in data if (record["university"], record["supervisor"]) not in processed_records_dict]

    # 初始化进度条，初始进度是已处理的记录数，目标总数是源文件的总数
    pbar = tqdm(total=total_records, initial=processed_count, desc="处理进度")

    # 开始多线程处理
    process_data_multithreaded(pending_records, processed_records_dict)

    pbar.close()

if __name__ == "__main__":
    main()
