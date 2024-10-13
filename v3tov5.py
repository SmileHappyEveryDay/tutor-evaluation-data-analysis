# {
#     "school_cate": "985",
#     "university": "大连理工大学",
#     "department": "信息与通信工程学院",
#     "supervisor": "解永平",
#     "description": "自证认识导师：黑楼3楼，左手边<br><br>学术水平：毕业靠自己，有要求不指导<br><br>科研经费：横向课题<br><br>学生补助：这个不错<br><br>师生关系：较融洽<br><br>工作时间：要求一般<br><br>学生前途：技术老旧\n利益相关：黑楼3楼，左手边 导师能力：毕业靠自己，有要求不指导 经费发放：横向课题 学生补助：这个不错 与学生关系：较融洽 工作时间：要求一般 学生毕业去向：技术老旧",
#     "gender": "男",
#     "province": "辽宁省",
#     "major": "Engineering",
#     "average_score": 2.5,
#     "Teacher-Student Relationship": 4,
#     "Student Prospects": -1,
#     "Student Allowance": 4,
#     "Supervisor's Professional Ability": 1,
#     "Supervisor's Project Attitude": 0,
#     "Supervisor's Lifestyle": 3
# },

import json

# Load JSON data from the file
file_path = 'proceed_comments_data_en_v3.json'

# Read and modify the data
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Remove 'description' field from each record in the list
for record in data:
    if 'description' in record:
        del record['description']

# Save the updated data to a new JSON file
new_file_path = 'proceed_comments_data_en_v5.json'
with open(new_file_path, 'w', encoding='utf-8') as f_out:
    json.dump(data, f_out, ensure_ascii=False, indent=4)

print(f"Updated JSON saved as {new_file_path}")

