import re
import glob
import os
from datetime import datetime, timedelta

"write by google ai studio"
"date:2024-11-29"
"与えた命令"
'''pythonのプログラムの作成で、ファイルから、tid is null one_message という文字列の行だけ抜き出し、
その行の中の35からはじまる15桁の数字の行数をそれぞれカウントし、その際ファイルパスはdev.log.-yyyy-mm-ddというファイルパスで、
2024-08-18から開始し、終了日の2024-11-24までの集計を記録し、一つのファイルに出力する。その際に、日付の厳密なチェックを行い、
存在しない日付はスキップする。出力ファイル名は、開始日+終了日_count.txtとする 例外処理を随所に入れる'''

def count_numbers_in_logs(start_date_str, end_date_str):
    """
    指定された期間のログファイルから特定の文字列と数字を抽出し、カウントする関数。
    日付の妥当性チェックを行い、存在しない日付はスキップする。

    Args:
        start_date_str: 集計開始日 (YYYY-MM-DD形式)
        end_date_str: 集計終了日 (YYYY-MM-DD形式)

    Returns:
        None. 結果をファイルに出力する。
    """

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        print("日付の形式が不正です。YYYY-MM-DD形式で入力してください。")
        return

    output_filename = f"{start_date_str}_{end_date_str}_count.txt"
    number_counts = {}

    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(f"集計期間: {start_date_str} - {end_date_str}\n\n")

            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                filepath = f"dev.log.-{date_str}"

                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        for line in infile:
                            if "tid is null one_message" in line:
                                match = re.search(r"3\d{14}", line)
                                if match:
                                    number = match.group(0)
                                    number_counts[number] = number_counts.get(number, 0) + 1
                except FileNotFoundError:
                    print(f"ファイルが見つかりません: {filepath}")
                except Exception as e:
                    print(f"エラーが発生しました: {filepath}, エラー内容: {e}")

                current_date += timedelta(days=1)

            for number, count in number_counts.items():
                outfile.write(f"{number}: {count}\n")

    except Exception as e:
        print(f"ファイル出力中にエラーが発生しました: {e}")


if __name__ == "__main__":
    start_date = "2024-08-18"
    end_date = "2024-11-24"
    count_numbers_in_logs(start_date, end_date)