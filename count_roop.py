import re
import os
import glob
from datetime import datetime, timedelta


def process_log_files(start_date, end_date, log_pattern="dev.log.-*"):
    """
    指定された日付範囲のログファイルから工数をカウントし、結果をファイルに出力します。

    Args:
        start_date: 処理開始日 (YYYY-MM-DD形式の文字列)
        end_date: 処理終了日 (YYYY-MM-DD形式の文字列)
        log_pattern: ログファイルのパターン (globパターン)

    Returns:
        処理が成功したファイルの数
    """

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    processed_files = 0

    for i in range((end - start).days + 1):
        current_date = start + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        filepath = log_pattern.replace("*", date_str)
        
        if process_single_log_file(filepath):
            processed_files += 1

    return processed_files


def process_single_log_file(filepath):
    """
    1つのログファイルから工数をカウントし、結果をファイルに出力します。

    Args:
        filepath: ログファイルのパス

    Returns:
        処理が成功した場合はTrue、失敗した場合はFalseを返します。
    """
    man_hour_counts = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if "tid is null one_message" in line:
                    match = re.search(r'35\d{13}', line)
                    if match:
                        man_hour = match.group(0)
                        man_hour_counts[man_hour] = man_hour_counts.get(man_hour, 0) + 1

        output_filepath = filepath + "_count.txt"
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            for man_hour, count in man_hour_counts.items():
                outfile.write(f"{man_hour}: {count}\n")

        return True

    except FileNotFoundError:
        print(f"Warning: ファイル '{filepath}' が見つかりません。")  # ファイルが見つからない場合は警告を表示する
        return False
    except Exception as e:
        print(f"Error: ファイル '{filepath}' の処理中にエラーが発生しました: {e}")
        return False


if __name__ == "__main__":
    start_date = "2024-08-18"
    end_date = "2024-11-24"
    processed_count = process_log_files(start_date, end_date)
    print(f"{processed_count} 個のファイルが処理されました。")