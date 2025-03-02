import csv
import json
from collections import defaultdict

# 读取CSV文件
def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

# 任务1：生成JSON映射
def generate_api_mapping(rows):
    return {
        int(row['id']): f"{row['class']}#{row['method']}"
        for row in rows
    }

# 任务2：查找重复API
def find_duplicate_apis(rows):
    duplicates = defaultdict(list)
    for row in rows:
        key = (row['class'], row['method'])
        duplicates[key].append(row)
    return {k: v for k, v in duplicates.items() if len(v) > 1}

# 写入重复API到txt
def write_duplicates(duplicates, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'class', 'method', 'enabled', 'tag', 'name', 'description'])
        for group in duplicates.values():
            for row in group:
                writer.writerow([
                    row['id'],
                    row['class'],
                    row['method'],
                    row['enabled'],
                    row['tag'],
                    row['name'],
                    'duplicate api'
                ])

# 主程序
if __name__ == "__main__":
    # 读取数据
    rows = read_csv('hooked_api_list.csv')
    
    # 生成JSON
    api_mapping = generate_api_mapping(rows)
    with open('api_mapping.json', 'w') as f:
        json.dump(api_mapping, f, indent=2)
    
    # 查找并写入重复项
    duplicates = find_duplicate_apis(rows)
    write_duplicates(duplicates, 'duplicate_apis.txt')
