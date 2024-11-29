import re

def count_man_hours(filepath):
    """
    ファイルから "tid is null one_message" の行を抜き出し、15桁の数字(工数)をカウントします。

    Args:
        filepath: 読み込むファイルのパス

    Returns:
        15桁の数字(工数)とその出現回数の辞書。エラーが発生した場合はNoneを返します。
    """

    man_hour_counts = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:  # エンコーディングを指定
            for line in f:
                line = line.strip()  # 行頭の空白文字と改行コードを除去
                if "tid is null one_message" in line:
                    match = re.search(r'35\d{13}', line) # 15桁の数字を検索
                    if match:
                        man_hour = match.group(0)
                        print(man_hour)
                        man_hour_counts[man_hour] = man_hour_counts.get(man_hour, 0) + 1
    except FileNotFoundError:
        print(f"Error: ファイル '{filepath}' が見つかりません。")
        return None
    except Exception as e:
        print(f"Error: エラーが発生しました: {e}")
        return None

    return man_hour_counts


if __name__ == "__main__":
    filepath = "dev.log.-2024-08-18"  # 読み込むファイル名を入力してください。
    result = count_man_hours(filepath)

    if result:
        print("工数とその出現回数:")
        for man_hour, count in result.items():
            print(f"{man_hour}: {count}回")