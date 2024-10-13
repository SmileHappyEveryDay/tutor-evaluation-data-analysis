import json

# 读取 JSON 数据文件
with open('proceed_comments_data_en_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建一个集合存储唯一的 province 值
unique_provinces = set()

# 遍历每条记录，提取 province 字段
for record in data:
    if 'province' in record:
        unique_provinces.add(record['province'])

# 输出不重复的 province 集合
print(unique_provinces)
