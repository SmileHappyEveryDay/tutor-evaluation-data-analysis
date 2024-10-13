import json
import os

# 存储文件路径
expanded_output_filename = "expanded_comments_data.txt"
extra_output_filename = "extra_expanded_comments_data.txt"
final_output_filename = "merged_comments_data.json"

# 读取 txt 文件，并解析为字典，以 (university, supervisor) 作为唯一键
def load_records_from_file(filename):
    records_dict = {}
    
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                records = content.split("\n\n")
                for record in records:
                    try:
                        data = json.loads(record)
                        key = (data["university"], data["supervisor"])
                        records_dict[key] = data
                    except json.JSONDecodeError:
                        continue
    return records_dict

# 融合两个文件中的记录
def merge_records(expanded_records, extra_records):

    # 覆盖 expanded_records 中的未完成记录
    for key, extra_record in extra_records.items():
        expanded_records[key] = extra_record  # 用 extra 中的记录覆盖 expanded 中的记录

    # 统计
    print(f"共有 {len(extra_records)} 条记录从 extra 覆盖或添加到 expanded。")
    print(f"融合后的总记录数量为 {len(expanded_records)}。")

    return expanded_records

# 将记录字典转换为列表并保存为 JSON 文件
def save_to_json(records_dict, output_filename):
    records_list = list(records_dict.values())
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(records_list, f, ensure_ascii=False, indent=4)

# 主程序逻辑
def main():
    # 读取 expanded_comments_data.txt 中的记录
    expanded_records = load_records_from_file(expanded_output_filename)
    
    # 读取 extra_expanded_comments_data.txt 中的记录
    extra_records = load_records_from_file(extra_output_filename)
    
    # 融合两个文件的记录
    merged_records = merge_records(expanded_records, extra_records)
    
    # 将融合后的记录保存为 JSON 文件
    save_to_json(merged_records, final_output_filename)

    print(f"所有记录已融合，并保存为 {final_output_filename}")

if __name__ == "__main__":
    main()


# 共有 17 条记录从 extra 覆盖或添加到 expanded。
# 融合后的总记录数量为 17273。
# 所有记录已融合，并保存为 merged_comments_data.json