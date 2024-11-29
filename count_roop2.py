import re
import glob
import os

def count_numbers_in_logs(start_date, end_date):
    """
    指定された期間のログファイルから特定の文字列と数字を抽出し、カウントする関数。

    Args:
        start_date: 集計開始日 (YYYY-MM-DD形式)
        end_date: 集計終了日 (YYYY-MM-DD形式)

    Returns:
        None. 結果をファイルに出力する。
    """

    start_year, start_month, start_day = map(int, start_date.split('-'))
    end_year, end_month, end_day = map(int, end_date.split('-'))

    output_filename = f"{start_date}_{end_date}_count.txt"
    number_counts = {}  # 15桁の数字とその出現回数を保存する辞書

    try:
        with open(output_filename, 'w') as outfile:
            outfile.write(f"集計期間: {start_date} - {end_date}\n\n")

            for year in range(start_year, end_year + 1):
                for month in range(1, 13):
                    for day in range(1, 32):
                        if year == start_year and month < start_month:
                            continue
                        if year == start_year and month == start_month and day < start_day:
                            continue
                        if year == end_year and month > end_month:
                            continue
                        if year == end_year and month == end_month and day > end_day:
                            continue

                        date_str = f"{year:04d}-{month:02d}-{day:02d}"
                        filepath = f"dev.log.-{date_str}"

                        try:
                            with open(filepath, 'r', encoding='utf-8') as infile:  # エンコーディングを指定
                                for line in infile:
                                    if "tid is null one_message" in line:
                                        match = re.search(r"3\d{14}", line)  # 3で始まる15桁の数字を検索
                                        if match:
                                            number = match.group(0)
                                            number_counts[number] = number_counts.get(number, 0) + 1

                        except FileNotFoundError:
                            print(f"ファイルが見つかりません: {filepath}")
                            continue  # ファイルがない場合は次のファイルへ
                        except Exception as e:
                            print(f"エラーが発生しました: {filepath}, エラー内容: {e}")
                            continue # エラーが発生したら次のファイルへ


            for number, count in number_counts.items():
                outfile.write(f"{number}: {count}\n")

    except Exception as e:
        print(f"ファイル出力中にエラーが発生しました: {e}")


if __name__ == "__main__":
    start_date = "2024-08-18"
    end_date = "2024-11-24"
    count_numbers_in_logs(start_date, end_date)