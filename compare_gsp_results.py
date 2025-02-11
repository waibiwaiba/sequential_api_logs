import argparse
from collections import defaultdict

def parse_gsp_results(file_path, min_length):
    """解析GSP结果文件，返回按长度分组的序列字典"""
    sequences = defaultdict(set)
    current_length = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 检测序列长度段落
            if line.startswith("Sequences of length"):
                current_length = int(line.split(" ")[3].replace(":", ""))
                continue
                
            # 只处理满足最小长度的序列
            if current_length >= min_length and "→" in line:
                # 提取序列部分(去掉支持度信息)
                sequence = line.split(": Support")[0].strip()
                sequences[current_length].add(sequence)
    
    return sequences

def find_common_and_unique_sequences(file1, file2, min_length, unique_length, output_file):
    """查找并保存共有序列和特有序列，按长度分组输出"""
    # 解析两个文件
    seq1 = parse_gsp_results(file1, min_length)
    seq2 = parse_gsp_results(file2, min_length)
    
    # 找交集并按长度分组
    common_sequences = defaultdict(list)
    for length in set(seq1.keys()) | set(seq2.keys()):
        if length >= min_length:
            common = seq1.get(length, set()) & seq2.get(length, set())
            if common:
                common_sequences[length] = sorted(common)
    
    # 找特有序列（仅在file1或file2中出现）
    unique_seq1 = defaultdict(list)
    unique_seq2 = defaultdict(list)
    if unique_length > 0:
        for length in set(seq1.keys()) | set(seq2.keys()):
            if length >= unique_length:
                unique1 = seq1.get(length, set()) - seq2.get(length, set())
                unique2 = seq2.get(length, set()) - seq1.get(length, set())
                if unique1:
                    unique_seq1[length] = sorted(unique1)
                if unique2:
                    unique_seq2[length] = sorted(unique2)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入共有序列
        f.write(f"Common sequences (length >= {min_length}):\n\n")
        for length in sorted(common_sequences.keys()):
            f.write(f"Sequences of length {length}:\n")
            for idx, seq in enumerate(common_sequences[length], 1):
                f.write(f"  {idx}. {seq}\n")
            f.write("\n")
        
        # 写入特有序列（如果启用了-y参数）
        if unique_length > 0:
            f.write(f"\nUnique sequences in {file1} (length >= {unique_length}):\n\n")
            for length in sorted(unique_seq1.keys()):
                f.write(f"Sequences of length {length}:\n")
                for idx, seq in enumerate(unique_seq1[length], 1):
                    f.write(f"  {idx}. {seq}\n")
                f.write("\n")
            
            f.write(f"\nUnique sequences in {file2} (length >= {unique_length}):\n\n")
            for length in sorted(unique_seq2.keys()):
                f.write(f"Sequences of length {length}:\n")
                for idx, seq in enumerate(unique_seq2[length], 1):
                    f.write(f"  {idx}. {seq}\n")
                f.write("\n")
    
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare two GSP result files')
    parser.add_argument('file1', help='First GSP result file')
    parser.add_argument('file2', help='Second GSP result file')
    parser.add_argument('-x', '--min-length', type=int, required=True,
                        help='Minimum sequence length to compare for common sequences')
    parser.add_argument('-y', '--unique-length', type=int, default=0,
                        help='Minimum sequence length to compare for unique sequences (0 to disable)')
    parser.add_argument('-o', '--output', default='common_sequences.txt',
                        help='Output file name (default: common_sequences.txt)')
    
    args = parser.parse_args()
    
    find_common_and_unique_sequences(
        args.file1,
        args.file2,
        args.min_length,
        args.unique_length,
        args.output
    )