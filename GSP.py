import argparse
import json
from gsppy.gsp import GSP
from datetime import datetime


def process_log_file(file_path):
    """Process a single API log file into a transaction sequence."""
    transaction = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
            # Handle potential JSON array formatting
            log_entries = content.split('},{')
            # 除去最后一个entry末尾带的','
            log_entries[-1] = log_entries[-1][:-1]
            
            for entry in log_entries:
                entry = entry.strip()
                if not entry:
                    continue
                
                # Ensure proper JSON formatting
                if not entry.startswith('{'):
                    entry = '{' + entry
                if not entry.endswith('}'):
                    entry += '}'
                
                try:
                    log_entry = json.loads(entry)
                    api = f"{log_entry['class']}#{log_entry['method']}"
                    transaction.append(api)
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error parsing entry in {file_path}: {e}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return transaction

def main():
    parser = argparse.ArgumentParser(description='Mine API sequence patterns using GSP algorithm.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', nargs='+', metavar='TXT_FILE', help='Direct paths to API log files')
    group.add_argument('-f', metavar='FILE_LIST', help='Path to file containing list of API log paths')
    parser.add_argument('-s', '--support', type=float, default=0.3, help='Minimum support threshold (default: 0.3)')
    
    args = parser.parse_args()
    
    # Collect all file paths
    file_paths = []
    if args.m:
        file_paths = args.m
    elif args.f:
        with open(args.f, 'r', encoding='utf-8') as f:
            file_paths = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    # Process all logs into transactions
    transactions = []
    for path in file_paths:
        transaction = process_log_file(path)
        if transaction:  # Skip empty transactions
            transactions.append(transaction)
        else:
            print(f"Warning: No valid data in {path}")
    
    if not transactions:
        print("No valid transactions found. Exiting.")
        return
    
    # Run GSP algorithm
    result = GSP(transactions).search(args.support)
    
    # Generate output file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"gsp_results_{timestamp}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write input file information
        f.write("Input files used for GSP algorithm:\n")
        for path in file_paths:
            f.write(f'"{path}"\n')
        f.write("\n")
        
        # Write GSP results
        f.write("GSP Mining Results:\n")
        for level, patterns in enumerate(result, 1):
            f.write(f"\nSequences of length {level}:\n")
            for pattern, support in patterns.items():
                seq_str = " → ".join(pattern)
                f.write(f"  {seq_str}: Support = {support}\n")
    
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()