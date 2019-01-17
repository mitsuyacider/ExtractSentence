import regex
import csv
import os
import re

def getSplitedSentences(txt):
    # txt = '「こんにちは。今日はいい天気ですね」あしたは晴れるといいな？でも美味しいご飯が食べたい。beautiful skyはいい天気という意味です。'
    # sen = regex.split(r'(?<=[。？])(?!$)', txt, flags=regex.VERSION1)
    sen = re.findall(r'[^。]+(?:[。]|$)', txt)
    return sen

def saveSenenceList(sentences, fileName):
    # NOTE: sentences directoryが存在していなければ作成して、
    #       sentences directoryにcsvファイルを保存する
    new_dir_path = 'sentences/'
    os.makedirs(new_dir_path, exist_ok=True)
    saveFile = new_dir_path + fileName + '.csv'

    # NOTE: r	ファイルを読み込み専用として開く。
    #       w	ファイルに書き込みをするために新規作成する。但し、存在するファイル名を指定すると、ファイルの中身が全て消えます。
    #       a	ファイルに書き込みするために開く。
    #       b   「バイナリモードで開く」
    f = open(saveFile, 'w')
    dataWriter = csv.writer(f)

    # NOTE: column(縦）に文章を書き込んでいくため、
    #       2次元配列にする必要がある。
    rowList = []
    for index, item in enumerate(sentences):
        rowList.append([])
        rowList[index].append(item)

    dataWriter.writerows(rowList)
    f.close()
    
def main():
    csv_file = open("datalist.csv", "r")
    #辞書形式
    dataList = csv.DictReader(csv_file)

    for row in dataList:
        #rowはdictionary
        #row["column_name"] or row.get("column_name")で必要な項目を取得することができる
        splitedSentences = getSplitedSentences(row['説明文'])

        # TODO: データが少ないので、現状は「贈呈理由」も文章リストに加える
        reasonSentences = getSplitedSentences(row['贈呈理由'])
        splitedSentences.extend(reasonSentences)

        fileName = row['No.'] + '-sentences'
        saveSenenceList(splitedSentences, fileName)

main()
