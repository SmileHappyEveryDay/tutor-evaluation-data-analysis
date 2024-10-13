# 分析 6: 文本分析 - 生成导师描述的词云
import matplotlib.pyplot as plt
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

# 使用已翻译的英文单词生成词云
english_words = [
    'Funding Allocation', 'Student Prospects', 'Working Hours', 'Student Allowance', 'Student Graduation Path',
    'Teacher-Student Relationship', 'Academic Level', 'Research Funding', 'No Overtime', 'Mentor Ability',
    'Conflict of Interest', 'Research Support', 'Academic Guidance', 'Research Project', 'Student Development',
    'Time Arrangement', 'Project Support', 'Team Collaboration', 'Research Interests', 'Career Development',
    'Academic Resources', 'Mentoring Ability', 'Communication', 'Learning Opportunities', 'Project Management',
    'Academic Achievements', 'Supervising Teacher', 'Collaborative Research', 'Research Outcomes', 'Mentor Attitude',
    'Project Progress', 'Student Satisfaction', 'Research Collaboration', 'Mentor Feedback', 'Student Experience',
    'Supervisor Feedback', 'Skill Development', 'Academic Consultation', 'Educational Resources', 'Professional Growth',
    'Teaching Assistance', 'Conference Participation', 'Grant Writing', 'Publication Record', 'Training Opportunities',
    'Student Engagement', 'Knowledge Sharing', 'Performance Evaluation', 'Thesis Guidance', 'Independent Research',
    'Academic Conferences', 'Leadership Development', 'Research Skills', 'Work-Life Balance', 'Student Guidance',
    'Collaborative Environment', 'Research Proposal', 'Educational Growth', 'Personal Development', 'Peer Feedback',
    'Scholarship Opportunities', 'Faculty Collaboration', 'Progress Tracking', 'Course Development', 'Professional Networking',
    'Internship Opportunities', 'Technical Support', 'Data Analysis', 'Critical Thinking', 'Innovation Support',
    'Publication Opportunities', 'Proposal Writing', 'Research Facilities', 'Academic Coaching', 'Industry Collaboration',
    'Student Workshop', 'Research Contributions', 'Team Development', 'Project Execution', 'Academic Consulting',
    'Student Advocacy', 'Educational Programs', 'Strategic Planning', 'Innovation Projects', 'Continuous Improvement',
    'Research Dissemination', 'Faculty Mentorship', 'Student Empowerment', 'Goal Setting', 'Performance Metrics',
    'Research Evaluation', 'Community Engagement', 'Career Pathway', 'Academic Policies', 'Funding Resources',
    'Mentor Review', 'Development Workshops', 'Progress Evaluation', 'Collaborative Meetings', 'Feedback Sessions'
]


# 生成词云
descriptions = ' '.join(english_words)
wordcloud = WordCloud(font_path=font_path, width=800, height=400, background_color='white', max_font_size=50, min_font_size=10).generate(descriptions)
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Mentor Descriptions (English)')
plt.savefig('./figs/mentor_descriptions_wordcloud_en.png')
plt.close()

# # 保存处理后的数据到文件
# df.to_csv('/mnt/data/processed_mentor_data.csv', index=False)