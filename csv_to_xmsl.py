import openpyxl
import csv
import os
from openpyxl.utils.exceptions import InvalidFileException
from datetime import datetime

'''
write by google ai studio 
date:2024-11-30
与えた文字列
pythonのプログラムの作成において、openpyxlモジュールを使用して、ディレクトリ web1,web2,app1,app2,db1,db2,test の各ディレクトリ内の
 cpu_YYYYMM.csv, memory_YYYYMM.csv,swap_YYYYMM.csv,disk_YYYYMM.csv の各ディレクトリ毎のcsvファイル(shift-jis)を読み込み、
 エクセルファイルを作成し、シート名を読み込みファイル名の拡張子無しとし、csvファイル毎にシートにcsvファイルを挿入する、
 その際数値は数値型とする、すべてのシートを一つのエクセルファイルに挿入し出力する
'''

def csv_to_excel_sheet(csv_filepath, worksheet, sheet_name):
    """CSVデータを指定したワークシートに追加します。数値は数値型に変換します。"""
    try:
        with open(csv_filepath, 'r', encoding='shift_jis') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # 数値型への変換処理を追加
                numeric_row = []
                for cell in row:
                    try:
                        numeric_row.append(int(cell))  #整数型に変換を試みる
                    except ValueError:
                        try:
                            numeric_row.append(float(cell)) #小数型に変換を試みる
                        except ValueError:
                            numeric_row.append(cell) #変換できない場合は文字列のまま
                worksheet.append(numeric_row)
    except FileNotFoundError:
        print(f"CSVファイルが見つかりません: {csv_filepath}")
    except Exception as e:
        print(f"エラーが発生しました: {csv_filepath}, エラー内容: {e}")



def process_directories(directories, year_month, output_filename="output.xlsx"):
    """
    指定されたディレクトリ内のCSVファイルを読み込み、一つのExcelファイルにまとめます。
    """
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Summary"

    for directory in directories:
        if not os.path.exists(directory):
            print(f"ディレクトリが存在しません: {directory}")
            continue

        csv_files = {
            "cpu": f"cpu_{year_month}.csv",
            "memory": f"memory_{year_month}.csv",
            "swap": f"swap_{year_month}.csv",
            "disk": f"disk_{year_month}.csv",
        }

        for filename, csv_name in csv_files.items():
            csv_filepath = os.path.join(directory, csv_name)
            try:
                sheet = workbook.create_sheet(f"{directory}_{filename}")
                csv_to_excel_sheet(csv_filepath, sheet, f"{directory}_{filename}")
            except Exception as e:
                print(f"ファイル{csv_filepath}の処理中にエラーが発生しました: {e}")


    try:
        workbook.save(output_filename)
        print(f"Excelファイルが作成されました: {output_filename}")
    except Exception as e:
        print(f"Excelファイルの保存中にエラーが発生しました: {e}")


if __name__ == "__main__":
    year_month = "202411"
    directories = ["web1", "web2", "app1", "app2", "db1", "db2", "test"]
    process_directories(directories, year_month)