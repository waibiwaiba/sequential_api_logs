import os
import glob
import itertools
import subprocess

def main():
    # 设置输入目录和输出目录
    input_dir = r"D:\Code\sequential_api_logs\gsp_results_of_malware_log_example"
    output_dir = os.path.join(input_dir, "compare_results")
    
    # 获取所有.txt文件
    txt_files = glob.glob(os.path.join(input_dir, "*.txt"))
    
    # 生成所有两两组合
    file_combinations = itertools.combinations(txt_files, 2)
    
    # 遍历所有组合并调用对比脚本
    for file1, file2 in file_combinations:
        # 提取文件名前缀（去除_gsp_results后的部分）
        prefix1 = os.path.basename(file1).split("_gsp_results")[0]
        prefix2 = os.path.basename(file2).split("_gsp_results")[0]
        
        # 构建输出文件名和路径
        output_filename = f"[{prefix1}]+[{prefix2}].txt"
        output_path = os.path.join(output_dir, output_filename)
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 调用对比脚本
        subprocess.run([
            "python",
            "compare_gsp_results.py",
            file1,
            file2,
            "-x", "3",
            "-y", "5",
            "-o", output_path
        ])

if __name__ == "__main__":
    main()