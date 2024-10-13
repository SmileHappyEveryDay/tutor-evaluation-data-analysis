import json
from tqdm import tqdm

# 加载映射文件 descrips.json
with open('descrips.json', 'r', encoding='utf-8') as f:
    descrips_mapping = json.load(f)

# 加载中-英的映射字典 descrips_zh2en.json
with open('descrips_zh2en.json', 'r', encoding='utf-8') as f:
    cn_to_en_mapping = json.load(f)


# 加载输入的 merged_comments_data.json
with open('merged_comments_data.json', 'r', encoding='utf-8') as f:
    merged_data = json.load(f)

proceed_data_v0 = merged_data

# 归一化得分到最近的 0.5 倍数
def normalize_score(score):
    return round(score * 2) / 2  # 四舍五入到最近的0.5倍数

# 处理每一条记录
for record in tqdm(proceed_data_v0):
    # 删除 rate 属性
    if 'rate' in record:
        # del record['rate']
        record.pop('rate', None)  # 使用 pop 确保键存在时才删除

    # 修改 gender, province, major 的键名，去掉 (predicted) 后缀
    if 'gender(predicted)' in record:
        record['gender'] = record.pop('gender(predicted)')
    if 'province(predicted)' in record:
        record['province'] = record.pop('province(predicted)')
    if 'major(predicted)' in record:
        record['major'] = record.pop('major(predicted)')

    # 创建一个新的字典，用来存储统一后的 comment_analysis
    unified_comment_analysis = {}

    # 处理 comment_analysis 并进行分类
    if 'comment_analysis' in record:
        comment_analysis = record['comment_analysis']
        total_score = 0
        score_count = 0

        for key, infos in comment_analysis.items():
            if type(infos) == list and len(infos) ==2:
                (score, comment) = infos
            elif type(infos) == int:
                (score, comment) = (infos, "暂无评论")
            else:
                (score, comment) = (-1, "不适用")
            # 查找该属性对应的分类
            category = descrips_mapping.get(key)
            if category:
                # if category not in unified_comment_analysis:
                unified_comment_analysis[category] = [score, comment]
            else:
                raise KeyError(f'{key} not in {descrips_mapping}.')

            # 计算有效得分，排除 -1 的得分
            if score != -1:
                total_score += score
                score_count += 1

        # 计算平均分并归一化到 0.5 的倍数
        if score_count > 0:
            average_score = total_score / score_count
            normalized_average_score = normalize_score(average_score)
            record['average_score'] = normalized_average_score

        # 用统一后的 comment_analysis 替换原有的
        record['comment_analysis'] = unified_comment_analysis

# 输出 proceed_data_v0 的长度
print(f"proceed_data_v0 处理后的记录总数: {len(proceed_data_v0)}")

# 保存处理后的数据到 proceed_comments_data_zh_v0.json
with open('proceed_comments_data_zh_v0.json', 'w', encoding='utf-8') as f:
    json.dump(proceed_data_v0, f, ensure_ascii=False, indent=4)

print("数据处理完成，已保存到 proceed_comments_data_zh.json")

# 处理每一条记录并生成 proceed_comments_data_en.json
proceed_data_v1 = []

for record in tqdm(proceed_data_v0.copy()):
    if 'comment_analysis' in record:
        comment_analysis = record['comment_analysis']
        # 将 comment_analysis 的属性转换为英文并提升到一级属性
        for cn_key, (score, comment) in comment_analysis.items():
            if cn_key in cn_to_en_mapping:
                en_key = cn_to_en_mapping[cn_key]  # 中文属性对应的英文属性
                record[en_key] = [score,comment]
                # {
                #     "score": score,
                #     "comment": comment
                # }

        # 删除原始的 comment_analysis 属性
        # del record['comment_analysis']
        record.pop('comment_analysis', None)  # 确保存在时才删除
    # 添加记录到 proceed_data_v1
    proceed_data_v1.append(record)

# 输出 proceed_data_v1 的长度
print(f"proceed_data_v1 处理后的记录总数: {len(proceed_data_v1)}")

# 将处理后的记录保存到 proceed_comments_data_en_v1.json
with open('proceed_comments_data_en_v1.json', 'w', encoding='utf-8') as f:
    json.dump(proceed_data_v1, f, ensure_ascii=False, indent=4)

proceed_data_v2 = proceed_data_v1.copy()
for record in tqdm(proceed_data_v2):
    for key in record:
        if type(record[key]) == list:
            if type(record[key][0]) == int:
                record[key] = record[key][0]
            else:
                raise KeyError(f"value of {key} is not right in {record[key]}.")

# 将处理后的记录保存到 proceed_comments_data_en_v2.json
with open('proceed_comments_data_en_v2.json', 'w', encoding='utf-8') as f:
    json.dump(proceed_data_v2, f, ensure_ascii=False, indent=4)