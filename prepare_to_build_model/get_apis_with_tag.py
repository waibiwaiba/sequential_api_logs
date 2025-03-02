import os
import json
import csv

def process_log_file(file_path):
    """Process a single API log file into a transaction sequence."""
    transaction = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.endswith(','):
                content = content[:-1]
            wrapped_content = f'[{content}]'
            try:
                log_entries = json.loads(wrapped_content)
                for entry in log_entries:
                    api = f"{entry['class']}#{entry['method']}"
                    transaction.append(api)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing entries in {file_path}: {e}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return transaction

def main():
    root_dir = r"C:\Users\Administrator\Desktop\TODO\api25"
    categories = ['benign', 'adware', 'banking', 'riskware', 'sms']
    output_csv = os.path.join(root_dir, 'api_counts.csv')

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['count', 'directory'])

        for category in categories:
            category_path = os.path.join(root_dir, category)
            if not os.path.exists(category_path):
                print(f"Category directory not found: {category_path}")
                continue

            tag = 0 if category == 'benign' else 1

            for root_dirpath, _, files in os.walk(category_path):
                if 'mobsf_api_monitor.txt' in files:
                    file_path = os.path.join(root_dirpath, 'mobsf_api_monitor.txt')
                    directory = os.path.dirname(file_path)

                    transaction = process_log_file(file_path)
                    count = len(transaction)

                    writer.writerow([count, directory])

                    output_content = f'({json.dumps(transaction)}, {tag})'
                    output_path = os.path.join(directory, 'apis_with_tag.txt')
                    
                    try:
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(output_content)
                    except Exception as e:
                        print(f"Error writing to {output_path}: {e}")

if __name__ == "__main__":
    main()
