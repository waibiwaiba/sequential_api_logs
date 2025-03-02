import re

def extract_unique_apis(input_file, output_file):
    """
    从GSP结果文件中提取所有唯一的API名称
    :param input_file: 输入的序列文件路径
    :param output_file: 输出的唯一API文件路径
    """
    unique_apis = set()
    sequence_pattern = re.compile(r'^\s*\d+\.\s+(.+?)(?:\s*: Support|$)')

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 匹配序列行（格式如：1. api1 → api2 → api3）
            match = sequence_pattern.match(line.strip())
            if match:
                # 提取并分割API序列
                sequence = match.group(1)
                apis = [api.strip() for api in sequence.split('→')]
                unique_apis.update(apis)

    # 按字母顺序排序并写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for api in sorted(unique_apis):
            f.write(f"{api}\n")

if __name__ == "__main__":
    input_file = "unique_api_sequence_beyond10k_x=3_y=3.txt"
    output_file = "unique_apis.txt"
    extract_unique_apis(input_file, output_file)
    print(f"提取完成！共找到 {len(open(output_file).readlines())} 个唯一API")
