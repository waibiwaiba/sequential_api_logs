import os
import csv
from collections import defaultdict

def select_samples(csv_path):
    categories = ['benign', 'adware', 'banking', 'riskware', 'sms']
    targets = {
        'benign': 500000,
        'adware': 150000,
        'banking': 150000,
        'riskware': 150000,
        'sms': 150000
    }

    # 读取并预处理数据
    data = defaultdict(list)
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            count = int(row['count'])
            directory = row['directory']
            if count <= 10000:
                continue
            
            for cat in categories:
                if f'\\{cat}\\' in directory:
                    data[cat].append((count, directory))
                    break

    # 修改关键点：按API数量升序排列
    selected = defaultdict(list)
    for cat in categories:
        sorted_data = sorted(data[cat], key=lambda x: x[0])  # 改为升序排列
        total = 0
        
        for count, path in sorted_data:
            if total >= targets[cat]:
                break
            selected[cat].append((count, path))
            total += count

        # 如果未达目标，继续添加剩余文件
        if total < targets[cat]:
            print(f"Warning: {cat} only reached {total}/{targets[cat]}")

    # 生成输出文件（与原脚本相同）
    output_dir = os.path.dirname(csv_path)
    report_path = os.path.join(output_dir, 'api_file_chosen.txt')
    train_data_path = os.path.join(output_dir, 'apis_with_tags_for_train.txt')
    
    with open(report_path, 'w', encoding='utf-8') as report, \
         open(train_data_path, 'w', encoding='utf-8') as train_data:
        
        total_apis = sum(sum(c for c, _ in selected[cat]) for cat in categories)
        report.write(f"total api count: {total_apis}\n\n")
        
        report.write("category,total chosen apis,chosen api files number,avg api count per chosen file\n")
        for cat in categories:
            entries = selected[cat]
            cat_total = sum(c for c, _ in entries)
            file_count = len(entries)
            avg = cat_total / file_count if file_count > 0 else 0
            report.write(f"{cat},{cat_total},{file_count},{round(avg, 2)}\n")
        
        for cat in categories:
            report.write(f"\napi files chosen for {cat}:\n")
            for count, path in selected[cat]:
                report.write(f'"{count}","{path}"\n')
            
            for _, path in selected[cat]:
                tag_file = os.path.join(path, 'apis_with_tag.txt')
                try:
                    with open(tag_file, 'r', encoding='utf-8') as f:
                        train_data.write(f.read().strip() + '\n')
                except Exception as e:
                    print(f"Error reading {tag_file}: {e}")

if __name__ == "__main__":
    csv_path = r"C:\Users\Administrator\Desktop\TODO\api25\api_counts.csv"
    select_samples(csv_path)
