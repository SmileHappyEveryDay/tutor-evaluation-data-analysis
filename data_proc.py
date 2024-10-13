import json
import pandas as pd

# 读取 985211.json 文件
with open('985211.json', 'r', encoding='utf-8') as f:
    school_categories = json.load(f)

# 提取 985 和 211 学校名单
schools_985 = set(school_categories['985'])
schools_211 = set(school_categories['211'])

# 为 Excel 数据添加 'school_cate' 列，并根据 985 和 211 分类进行填充
def categorize_school(university_name):
    if university_name in schools_985:
        return '985'
    elif university_name in schools_211:
        return '211'
    else:
        return '其他'

# 读取 JSON 文件
with open('comments_data.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 读取 Excel 文件
excel_path = './导师评价20240229更新.xlsx'  # Excel 文件路径
excel_data = pd.read_excel(excel_path)

# 选取 Excel 中需要的列并重命名与 JSON 结构一致
excel_data_filtered = excel_data[['学校', '专业', '姓名', '评价', 'SnowNLP的情感打分(0-1)仅供参考']]
excel_data_filtered.columns = ['university', 'department', 'supervisor', 'description', 'rate']

# # 添加一个 'school_cate' 列，Excel 数据暂时设为空
# excel_data_filtered['school_cate'] = ''
# 应用分类规则
excel_data_filtered['school_cate'] = excel_data_filtered['university'].apply(categorize_school)

# 转换为字典格式以便合并
excel_dict = excel_data_filtered.to_dict(orient='records')

# 记录初始数量
excel_record_count = len(excel_dict)
json_record_count = len(json_data)

# 合并两个数据集
combined_data = json_data + excel_dict

# 创建一个新字典，以学校和导师姓名为 key，合并重复评价
merged_data = {}
merged_record_count = 0  # 用于统计合并记录的数量

for item in combined_data:
    key = (item['university'], item['supervisor'])  # 学校名和导师名作为唯一键
    if key not in merged_data:
        merged_data[key] = {
            'school_cate': item['school_cate'],
            'university': item['university'],
            'department': item['department'],
            'supervisor': item['supervisor'],
            'rate': item['rate'],
            'description': item['description'] if item['description'] else '',
        }
    else:
        # 如果有重复的导师记录，整合评价和评分
        # merged_data[key]['description'] += "\n" + item['description']
        merged_data[key]['description'] = str(merged_data[key]['description']) + "\n" + str(item['description'] if item['description'] else '')
        merged_data[key]['rate'] = (merged_data[key]['rate'] + item['rate']) / 2  # 简单平均评分
        merged_record_count += 1  # 记录合并操作

# 将合并后的数据转换为列表
final_data = list(merged_data.values())

# 保存为新的 JSON 文件
with open('merged_comments_data.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

# 记录整合后的数据数量
final_record_count = len(final_data)

# 输出统计信息
print(f"原 Excel 记录数量: {excel_record_count}")
print(f"原 JSON 记录数量: {json_record_count}")
print(f"整合后的记录数量: {final_record_count}")
print(f"合并了的记录数量: {merged_record_count}")

print("合并完成并保存为 merged_comments_data.json")


# 原 Excel 记录数量: 26608
# 原 JSON 记录数量: 28612
# 55220
# 整合后的记录数量: 17333
# 合并了的记录数量: 37887
# 合并完成并保存为 merged_comments_data.json