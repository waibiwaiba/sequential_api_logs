import sys

def analyze_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # 跳过标题行
            data = lines[1:]
            
            # 初始化统计变量
            count = 0
            total_api_calls = 0
            
            for line in data:
                # 分割每一行的数据
                parts = line.strip().split(',')
                
                # 获取API总调用数
                api_calls = int(parts[4])
                
                # 判断API总调用数是否超过100
                if api_calls > 100:
                    count += 1
                    total_api_calls += api_calls
            
            # 计算平均值
            if count > 0:
                average_api_calls = total_api_calls / count
            else:
                average_api_calls = 0
            
            # 输出结果
            print(f"API总调用条目超过100的记录的个数为: {count}")
            print(f"满足条件的记录的API总调用数的平均值为: {average_api_calls:.2f}")
    
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("请提供.txt文件的绝对路径作为参数。")
    else:
        file_path = sys.argv[1]
        analyze_file(file_path)