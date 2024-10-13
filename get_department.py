import json
# 假设原始的JSON文件路径是merged_comments_data.json
input_filename = "./merged_comments_data.json"

# 读取原始JSON文件
with open(input_filename, "r", encoding="utf-8") as f:
    input_data = json.load(f)

# 提取所有记录中的department字段，并创建一个不重复的set集合
departments = {record["department"] for record in input_data}

# 创建输出字典
output_data = {"unique_departments": list(departments)}

# 将结果保存为新的JSON文件
output_filename = "./unique_departments.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

output_filename
