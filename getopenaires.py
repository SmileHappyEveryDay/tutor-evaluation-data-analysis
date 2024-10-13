import openai
import json

# 设置OpenAI API的密钥和API base地址
openai.api_key = "sk-4HmIu1msph13JUMZ1fCf8082B9084927B88e6bEf3e9467Ac"
openai.api_base = "https://api.gpts.vin/v1"

def ask_gpt_for_json_oldv0(content):
    """请求GPT并检查返回是否为JSON格式，直到获得有效的JSON格式"""
    try_num = 0
    while True:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个帮助进行学生对高校导师评价分析的助手。所有分析内容必须返回合法的JSON格式，且全程不要英文作答。"},
                {"role": "user", "content": content}
            ]
        )
        result = response['choices'][0]['message']['content']
        
        # 尝试将结果解析为JSON
        try:
            json_result = json.loads(result)
            return json_result
        except json.JSONDecodeError:
            # 如果解析失败，重新向GPT请求，直到返回有效的JSON
            if try_num < 3:
                # print(result)
                print("收到的内容不是有效的JSON格式，重新请求中...")
                try_num+=1
                continue
            else:
                print("尝试次数过多，无法解析为JSON格式。")
                return None
            
def ask_gpt_for_json(content):
    """请求GPT并检查返回是否为JSON格式，直到获得有效的JSON格式"""
    try_num = 0
    messages = [
        {"role": "system", "content": "你是一个帮助进行学生对高校导师评价分析的助手。所有分析内容必须返回合法的JSON格式，且全程不要英文作答。"},
        {"role": "user", "content": content}
    ]

    while True:
        # 请求GPT并得到响应
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        result = response['choices'][0]['message']['content']

        # 尝试将结果解析为JSON
        try:
            json_result = json.loads(result)
            return json_result  # 如果成功解析为JSON则返回
        except json.JSONDecodeError:
            # 如果解析失败，再次请求GPT输出纯JSON格式
            if try_num < 3:
                print(result)  # 打印收到的错误内容
                print("收到的内容不是有效的JSON格式，重新请求中...")

                # 增加新的消息到上下文，明确要求只返回合法的JSON格式
                messages.append({"role": "assistant", "content": result})  # 添加上一次模型生成的回复
                messages.append({"role": "user", "content": "你上次的回复无法解析为合法的JSON格式。请确保只返回纯JSON格式的回复，其他任何多余内容都不要输出。"})

                try_num += 1
                continue  # 继续循环，再次请求GPT
            else:
                print("尝试次数过多，无法解析为JSON格式。")
                return None

def analyze_evaluation(data):
    # 构造请求内容（中文）
    message_content = f"""
    描述内容: {data['description']}

    请根据以上信息完成分析任务：
    1. 通过supervisor姓名 '{data['supervisor']}' 预测性别（男或女）。
    2. 根据所在大学名称 '{data['university']}' 预测该学校属于中国的哪个省或直辖市，如果不在中国，则填"海外"。
    3. 根据所在专业 '{data['department']}' ，给定学科大类：
    [
        "Engineering",
        "Information Technology",
        "Medicine & Life Sciences",
        "Natural Sciences",
        "Social Sciences & Humanities",
        "Agriculture & Environmental Sciences",
        "Business & Management",
        "Law & Public Affairs",
        "Art & Design",
        "Education"
    ]
    ，预测'{data['department']}'是其中的哪个类别。
    4. 对描述中的评价进行分析，包括以下几个方面：
       - 师生关系
       - 学生前途
       - 学生补助
       - 老师的专业水平
       - 老师是否强迫学生做项目
       - 老师的生活作风
    请为每个方面给出一个0到5的评分，其中0代表极差，1代表差，2代表有点差，3代表一般，4代表有点好，5代表很好，若没有对应的评价，则填-1，代表不适用。并且根据描述给出简短的评价。确保结果为JSON格式。
    """+ """
    举个例子，我希望你返回的JSON格式如下:
    {
        "gender(predicted)": "男",
        "province(predicted)": "北京市",
        "major(predicted)": "Engineering",
        "comment_analysis": {
            "师生关系": [4,"该老师对学生很好，很关心学生的生活。"],
            "学生前途": [3,"学生都去读博了"],
            "学生补助": [5,"补助非常多"],
            "老师的专业水平": [2,"老师专业水平一般"],
            "老师是否强迫学生做项目": [0,"老师没有强迫学生做项目，而是鼓励学生自己选择项目。"],
            "老师的生活作风": [4,"老师生活作风很好，经常组织学生参加各种活动。"],
        }
    }

    请你思考后，一定要返回符合上述格式的完整json数据。也就是说，你的回复一定要是以{开头，而且是以}结尾。
    """

    # 获取GPT分析的结果
    json_result = ask_gpt_for_json(message_content)

    # 将GPT生成的JSON结果更新到原始数据中
    if json_result is None:
        pass
    else:
        data.update({
            "gender(predicted)": json_result.get("gender(predicted)", None),
            "province(predicted)": json_result.get("province(predicted)", None),
            "major(predicted)": json_result.get("major(predicted)", None),  # 默认预测为工程类
            "comment_analysis": json_result.get("comment_analysis", {})
        })

    return data

if __name__ == "__main__":
    # 输入字典示例
    input_data = {
        "school_cate": "985",
        "university": "天津大学",
        "department": "电气自动化与信息工程学院",
        "supervisor": "肖夏",
        "description": "学术水平：有一定的水平，但是教书育人的水平几乎为零，在学术水平上太自大<br><br>科研经费：还可以<br><br>学生补助：看他自己是不是喜欢<br><br>师生关系：很差，天天狐假虎威，逼迫学生做事<br><br>工作时间：每天过得就像是要即将答辩的前几天是的，熬夜太常见了，估计大家都会在这几年多多少少烙下病根，比如失眠<br><br>学生前途：看不见光明"
    }

    # 调用函数分析
    result = analyze_evaluation(input_data)
    print(json.dumps(result, ensure_ascii=False, indent=4))


# {
#     "gender(predicted)": "男",
#     "province(predicted)": "天津市",
#     "major(predicted)": "Engineering",
#     "comment_analysis": {
#         "师生关系": [0, "师生关系很差，存在狐假虎威逼迫学生做事的情况。"],
#         "学生前途": [0, "学生前途看不见光明。"],
#         "学生补助": [3, "学生补助取决于学生个人情况，不确定性较大。"],
#         "老师的专业水平": [3, "老师的学术水平有一定水平，但自大，教学水平差。"],
#         "老师是否强迫学生做项目": [0, "老师存在逼迫学生做事的情况。"],
#         "老师的生活作风": [1, "老师工作时间过于辛苦，存在熬夜过度的情况。"],
#     }
# }
# 收到的内容不是有效的JSON格式，重新请求中...
# {
#     "school_cate": "985",
#     "university": "天津大学",
#     "department": "电气自动化与信息工程学院",
#     "supervisor": "肖夏",
#     "description": "学术水平：有一定的水平，但是教书育人的水平几乎为零，在学术水平上太自大<br><br>科研经费：还可以<br><br>学生补助：看他自己是不是喜欢<br><br>师生关系：很差，天天狐假虎威，逼迫学生做事<br><br>工作时间：每天过得就像是要即将答辩的前几天是的，熬夜太常见了，估计大家都会在这几年多多少少烙下病根，比如失眠<br><br>学生前途：看不见光明",
#     "gender(predicted)": "女",
#     "province(predicted)": "天津市",
#     "major(predicted)": "Engineering",
#     "comment_analysis": {
#         "师生关系": [
#             0,
#             "师生关系很差，老师逼迫学生做事"
#         ],
#         "学生前途": [
#             0,
#             "学生前途看不见光明"
#         ],
#         "学生补助": [
#             2,
#             "学生补助视学生自己喜好而定"
#         ],
#         "老师的专业水平": [
#             3,
#             "老师在学术水平上有一定水平"
#         ],
#         "老师是否强迫学生做项目": [
#             0,
#             "老师逼迫学生做项目"
#         ],
#         "老师的生活作风": [
#             1,
#             "老师工作时间过长，生活作风有问题"
#         ]
#     }
# }