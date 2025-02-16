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

def find_common_and_unique_sequences(file_paths, min_length, unique_length, output_file):
    """处理多个文件的共有和特有序列"""
    # 解析所有文件
    all_sequences = [parse_gsp_results(fp, min_length) for fp in file_paths]
    
    # 计算共有序列（所有文件的交集）
    common_sequences = defaultdict(list)
    all_lengths = set()
    for seq in all_sequences:
        all_lengths.update(seq.keys())
    
    for length in sorted(all_lengths):
        if length < min_length:
            continue
        # 收集各文件的序列集合
        seq_sets = [seq.get(length, set()) for seq in all_sequences]
        common = set.intersection(*seq_sets)
        if common:
            common_sequences[length] = sorted(common)
    
    # 计算特有序列（每个文件独有的序列）
    unique_seqs_per_file = []
    if unique_length > 0:
        for i, seq_dict in enumerate(all_sequences):
            unique_seqs = defaultdict(list)
            for length in seq_dict:
                if length < unique_length:
                    continue
                # 合并其他文件的序列
                other_sequences = set()
                for j, other_seq in enumerate(all_sequences):
                    if j != i:
                        other_sequences.update(other_seq.get(length, set()))
                # 计算当前文件的特有序列
                current = seq_dict[length] - other_sequences
                if current:
                    unique_seqs[length] = sorted(current)
            unique_seqs_per_file.append(unique_seqs)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入共有序列
        f.write(f"Common sequences across all files (length >= {min_length}):\n\n")
        for length in sorted(common_sequences.keys()):
            f.write(f"Sequences of length {length}:\n")
            for idx, seq in enumerate(common_sequences[length], 1):
                f.write(f"  {idx}. {seq}\n")
            f.write("\n")
        
        # 写入特有序列
        if unique_length > 0:
            for i, (file_path, unique_seqs) in enumerate(zip(file_paths, unique_seqs_per_file)):
                f.write(f"\nUnique sequences in {file_path} (length >= {unique_length}):\n\n")
                for length in sorted(unique_seqs.keys()):
                    f.write(f"Sequences of length {length}:\n")
                    for idx, seq in enumerate(unique_seqs[length], 1):
                        f.write(f"  {idx}. {seq}\n")
                    f.write("\n")
    
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare two or more GSP result files')
    parser.add_argument('-m', '--multi-file', help='Path to a file containing list of GSP result files')
    parser.add_argument('files', nargs='*', help='GSP result files to compare (specify two files if not using -m)')
    parser.add_argument('-x', '--min-length', type=int, required=True,
                        help='Minimum sequence length to compare for common sequences')
    parser.add_argument('-y', '--unique-length', type=int, default=0,
                        help='Minimum sequence length to compare for unique sequences (0 to disable)')
    parser.add_argument('-o', '--output', default='common_sequences.txt',
                        help='Output file name (default: common_sequences.txt)')
    
    args = parser.parse_args()
    
    # 处理文件路径
    if args.multi_file:
        # 从列表文件读取路径
        with open(args.multi_file, 'r') as f:
            file_paths = [line.strip() for line in f if line.strip()]
    else:
        # 直接使用命令行参数中的文件
        if len(args.files) < 2:
            parser.error("At least two files are required when not using -m")
        file_paths = args.files
    
    find_common_and_unique_sequences(
        file_paths,
        args.min_length,
        args.unique_length,
        args.output
    )