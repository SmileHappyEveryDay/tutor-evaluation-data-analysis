import json

# 读取proceed_comments_data_en_v2.json
with open('proceed_comments_data_en_v2.json', 'r', encoding='utf-8') as f:
    data_v2 = json.load(f)

print(f'原有 {len(data_v2)} 条记录.')

# 读取duplicate_provinces_mapping.json
with open('duplicate_provinces_mapping.json', 'r', encoding='utf-8') as f:
    province_mapping = json.load(f)

# 创建新的列表用于存储v3的记录
data_v3 = []

# 遍历v2数据，检查province字段
for record in data_v2:
    province = record.get('province')
    
    # 检查province是否在province_mapping中
    if province in province_mapping:
        # 如果在字典中，进行映射并替换province字段
        record['province'] = province_mapping[province]
        # 将更新后的记录添加到v3列表中
        data_v3.append(record)

# 将新的v3数据保存到proceed_comments_data_en_v3.json
with open('proceed_comments_data_en_v3.json', 'w', encoding='utf-8') as f:
    json.dump(data_v3, f, ensure_ascii=False, indent=4)

print(f"成功生成 proceed_comments_data_en_v3.json，共处理 {len(data_v3)} 条记录。")

# 原有 17273 条记录.
# 成功生成 proceed_comments_data_en_v3.json，共处理 16484 条记录。