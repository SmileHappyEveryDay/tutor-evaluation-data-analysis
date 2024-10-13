import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # 用于进度条
from threading import Lock
from getopenaires import analyze_evaluation

# 存储文件路径
expanded_output_filename = "expanded_comments_data.txt"
extra_output_filename = "extra_expanded_comments_data.txt"

# 进度条和计数器
lock = Lock()

# 读取文件，解析记录，筛选出没有 comment_analysis 的记录
def load_records_without_comment_analysis():
    records_without_comment_analysis = []
    
    if os.path.exists(expanded_output_filename):
        with open(expanded_output_filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                records = content.split("\n\n")
                for record in records:
                    try:
                        data = json.loads(record)
                        # 筛选没有 'comment_analysis' 属性的记录
                        if 'comment_analysis' not in data:
                            records_without_comment_analysis.append(data)
                    except json.JSONDecodeError:
                        continue
    return records_without_comment_analysis

# 追加新记录到存储文件
def append_record_to_file(record, filename):
    with lock:  # 确保多线程下安全访问文件
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, indent=4))
            f.write("\n\n")  # 使用两个换行符作为记录间隔

# 处理单条记录，重新获取 GPT 结果
def process_record(record):
    # 调用 analyze_evaluation 进行扩展处理
    expanded_record = analyze_evaluation(record)
    
    # 将扩展后的记录追加到 extra_expanded_comments_data.txt 文件中
    append_record_to_file(expanded_record, extra_output_filename)

    # 更新进度条
    with lock:
        pbar.update(1)

# 多线程处理数据
def process_data_multithreaded(records):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_record, record) for record in records]
        for future in as_completed(futures):
            try:
                future.result()  # 获取结果，确保异常被捕获
            except Exception as e:
                print(f"处理记录时出错: {e}")

# 主程序逻辑
def main():
    global pbar

    # 加载没有 comment_analysis 属性的记录
    records_to_process = load_records_without_comment_analysis()

    # 如果没有记录要处理，直接退出
    if not records_to_process:
        print("没有需要重新处理的记录。")
        return

    # 初始化进度条
    pbar = tqdm(total=len(records_to_process), desc="重新处理进度")

    # 开始多线程处理
    process_data_multithreaded(records_to_process)

    pbar.close()

if __name__ == "__main__":
    main()
