import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import matplotlib
from matplotlib import font_manager
import os

# 使用非交互式后端避免GUI冲突
matplotlib.use('Agg')

# 设置中文字体以防止乱码
# 设置 Windows 系统字体路径，调整为系统中的有效字体路径
font_path = 'C:\Windows\Fonts\msyh.ttc'  # 微软雅黑字体
if os.path.exists(font_path):
    prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
    prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False

# 加载数据
with open('proceed_comments_data_en_v3.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 转换为DataFrame
df = pd.DataFrame(data)

# 数据预处理 - 处理评分缺失值，去除无效评分
df.replace({-1: None}, inplace=True)
df.dropna(subset=['average_score'], inplace=True)

# 创建保存图表的文件夹
os.makedirs('./figs', exist_ok=True)

# # 分析 1: 导师综合评分分布
# plt.figure(figsize=(10, 6))
# sns.histplot(df['average_score'], kde=True, bins=20)
# plt.xlabel('Average Score')
# plt.ylabel('Frequency')
# plt.title('Distribution of Mentor Average Scores')
# plt.savefig('./figs/mentor_average_score_distribution.png')
# plt.close()

# # 分析 2: 师生关系评分和其他因素的关系
# # 转换变量为数字类型以便绘图
# df['Teacher-Student Relationship'] = pd.to_numeric(df['Teacher-Student Relationship'], errors='coerce')
# df['Student Allowance'] = pd.to_numeric(df['Student Allowance'], errors='coerce')
#
# # 删除缺失值
# df.dropna(subset=['Teacher-Student Relationship', 'Student Allowance'], inplace=True)
#
# plt.figure(figsize=(10, 6))
# sns.boxplot(x='Teacher-Student Relationship', y='Student Allowance', data=df)
# plt.xlabel('Teacher-Student Relationship')
# plt.ylabel('Student Allowance')
# plt.title('Teacher-Student Relationship vs Student Allowance')
# plt.savefig('./figs/teacher_student_relationship_vs_allowance.png')
# plt.close()

# # 分析 3: 按省份分组的平均评分
# province_translation = {
#     '山西省': 'Shanxi', '内蒙古自治区': 'Inner Mongolia', '浙江省': 'Zhejiang', '山东省': 'Shandong',
#     '福建省': 'Fujian', '广东省': 'Guangdong', '河北省': 'Hebei', '河南省': 'Henan',
#     '上海市': 'Shanghai', '湖南省': 'Hunan', '江西省': 'Jiangxi', '重庆市': 'Chongqing',
#     '陕西省': 'Shaanxi', '江苏省': 'Jiangsu', '安徽省': 'Anhui', '北京市': 'Beijing',
#     '甘肃省': 'Gansu', '黑龙江省': 'Heilongjiang', '天津市': 'Tianjin', '四川省': 'Sichuan',
#     '辽宁省': 'Liaoning', '吉林省': 'Jilin', '新疆维吾尔自治区': 'Xinjiang', '云南省': 'Yunnan',
#     '青海省': 'Qinghai', '宁夏回族自治区': 'Ningxia', '广西壮族自治区': 'Guangxi', '贵州省': 'Guizhou', "澳门特别行政区": "Macao", "台湾省": "Taiwan"
# }
# df['province_en'] = df['province'].map(province_translation)
# df_province = df.groupby('province_en')['average_score'].mean().sort_values()
# plt.figure(figsize=(14, 7))
# df_province.plot(kind='bar', color='skyblue')
# plt.xlabel('Province', fontsize=10)
# plt.ylabel('Average Score')
# plt.title('Average Score by Province')
# plt.xticks(rotation=45, fontsize=8)
# plt.ylim(2.5, 4.2)  # 调整纵坐标范围以便更好地展示差异
# plt.savefig('./figs/average_score_by_province.png')
# plt.close()

#
# 分析 4: 性别对评分的影响
# 归类性别并去掉不需要的类别
import pandas as pd
import matplotlib.pyplot as plt

# 归类性别并去掉不需要的类别
df['gender'] = df['gender'].replace({'女': 'female', '女性': 'female', '男': 'male'})
df = df[df['gender'].isin(['female', 'male'])]

# 计算每个维度下的 female 和 male 平均分数
aspects = ['average_score', 'Teacher-Student Relationship', 'Student Prospects', 'Student Allowance',
           "Supervisor's Professional Ability", "Supervisor's Project Attitude", "Supervisor's Lifestyle"]

# 创建一个字典来存储每个维度下的男女平均分数
average_scores_by_gender = {}

for aspect in aspects:
    average_scores_by_gender[aspect] = {
        'female': df[df['gender'] == 'female'][aspect].mean(),
        'male': df[df['gender'] == 'male'][aspect].mean()
    }

# 打印出每个维度下的男女平均分数
for aspect, scores in average_scores_by_gender.items():
    print(f"{aspect}: Female Average Score = {scores['female']}, Male Average Score = {scores['male']}")

# 绘制每个维度下的男女平均分数的柱状图
data_for_plot = []
labels = []

for aspect, scores in average_scores_by_gender.items():
    labels.extend([f"female - {aspect}", f"male - {aspect}"])
    data_for_plot.extend([scores['female'], scores['male']])

# 绘制柱状图
plt.figure(figsize=(16, 8))
plt.bar(labels, data_for_plot, color=['lightskyblue', 'lightcoral'] * len(aspects))
plt.ylabel('Average Score', fontsize=12)
plt.title('Comparison of Average Scores by Gender across Different Aspects', fontsize=14)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()

import numpy as np
plt.figure(figsize=(16, 8))

# 设置颜色和间隔
colors = ['#6a5acd', '#ff6347']  # 更加好看的颜色：slateblue 和 tomato
bar_width = 0.35
bar_spacing = 0.1  # 每组柱子之间的间隔

# 定义位置
indices = np.arange(len(aspects))

# 绘制柱状图
for i, aspect in enumerate(aspects):
    plt.bar(indices[i] - bar_width / 2, average_scores_by_gender[aspect]['female'], width=bar_width, color=colors[0], label='Female' if i == 0 else "")
    plt.bar(indices[i] + bar_width / 2, average_scores_by_gender[aspect]['male'], width=bar_width, color=colors[1], label='Male' if i == 0 else "")

plt.ylabel('Average Score', fontsize=12)
plt.ylim(2.0, None)  # 设置纵坐标的起始值为 2.0
plt.title('Comparison of Average Scores by Gender across Different Aspects', fontsize=14)
plt.xticks(indices, aspects, rotation=45, fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=12)
plt.tight_layout()

# 保存图像
plt.savefig('./figs/average_score_by_gender_aspects_comparison_fixed.png')
plt.close()

# average_score: Female Average Score = 2.7646947288585513, Male Average Score = 2.912828114831152
# Teacher-Student Relationship: Female Average Score = 2.7604562737642584, Male Average Score = 2.8649941995359627
# Student Prospects: Female Average Score = 2.8925549915397633, Male Average Score = 3.0867277799920285
# Student Allowance: Female Average Score = 2.7410772225827387, Male Average Score = 2.8987112819353382
# Supervisor's Professional Ability: Female Average Score = 3.035033086804204, Male Average Score = 3.2866671607500186
# Supervisor's Project Attitude: Female Average Score = 2.7260458839406208, Male Average Score = 2.8296212843400643
# Supervisor's Lifestyle: Female Average Score = 2.903345724907063, Male Average Score = 2.9482813242515444

#
# # 分析 5: 科研经费与学生前途的关系
# plt.figure(figsize=(10, 6))
# sns.boxplot(x='Student Prospects', y='average_score', data=df)
# plt.xlabel('Student Prospects')
# plt.ylabel('Average Score')
# plt.title('Student Prospects vs Average Score')
# plt.savefig('./figs/student_prospects_vs_average_score.png')
# plt.close()
#
# # 分析 6: 文本分析 - 生成导师描述的词云
# import re
# from collections import Counter
#
# # 清理描述文本中的噪音词
# descriptions = ' '.join(df['description'].dropna())
# noise_words = ['amp', '导师辨识特征', '自证认识导师','利益相关','导师能力']
# for word in noise_words:
#     descriptions = re.sub(r'\b' + re.escape(word) + r'\b', '', descriptions)
#
# # 删除包含 'br' 子串的词汇
# descriptions = ' '.join([word for word in descriptions.split() if 'br' not in word])
#
# # 获取词频并打印前20个词汇
# words = descriptions.split()
# word_counts = Counter(words)
# most_common_words = word_counts.most_common(20)
#
# print("Top 20 words:")
# deleted_words = []
# for word, count in most_common_words:
#     deleted_words.append(word)
#
# # 生成词云，保留所有未被删除的词汇
# filtered_descriptions = ' '.join([word for word in words if word not in deleted_words])
# # wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white').generate(filtered_descriptions)
# wordcloud = WordCloud(font_path=font_path, width=1200, height=600, background_color='white', max_font_size=100, min_font_size=5).generate(filtered_descriptions)
# plt.figure(figsize=(10, 6))
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.title('Word Cloud of Mentor Descriptions')
# plt.savefig('./figs/mentor_descriptions_wordcloud.png')
# plt.close()


# # 保存处理后的数据到文件
# df.to_csv('/mnt/data/processed_mentor_data.csv', index=False)