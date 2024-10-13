import json


def extract_first_n_entries(input_filepath, output_filepath, n=1000):
    """
    从输入的JSON文件中提取前n个条目，并保存到新的JSON文件中。

    :param input_filepath: 输入JSON文件的路径
    :param output_filepath: 输出JSON文件的路径
    :param n: 要提取的条目数量，默认为1000
    """
    try:
        # 读取原始JSON文件
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

        # 检查数据是否为列表
        if not isinstance(data, list):
            raise ValueError("JSON文件的顶层结构不是列表。")

        # 提取前n个条目
        first_n = data[:n]

        # 写入新的JSON文件
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            json.dump(first_n, outfile, ensure_ascii=False, indent=4)

        print(f"成功提取前{n}个条目并保存到 '{output_filepath}'。")

    except FileNotFoundError:
        print(f"文件未找到: {input_filepath}")
    except json.JSONDecodeError:
        print(f"文件不是有效的JSON格式: {input_filepath}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    input_file = 'proceed_comments_data_en_v3.json'
    output_file = 'proceed_comments_data_en_v4.json'
    extract_first_n_entries(input_file, output_file, n=1000)
