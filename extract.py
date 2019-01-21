import regex
import csv
import os
import re

from collections import Counter
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import *
from MorphologicalAnalysis import getWordsByMorphologicalAnalysis

# NOTE: 文章を1文ずつ分解する
# ref: https://teratail.com/questions/108738
def getSplitedSentences(txt):
    sen = re.findall(r'[^。]+(?:[。]|$)', txt)
    return sen

# NOTE: 配列をcsv形式で保存する（既存データも上書き）
#       @param dataList: 保存用データ
#       @param fileName: 保存ファイル名(拡張なし)
#       @param dataList: 保存用directory(current directoryからの相対パス)
def saveDataList(dataList, fileName, directory):
    # NOTE: sentences directoryが存在していなければ作成して、
    #       sentences directoryにcsvファイルを保存する
    new_dir_path = directory
    os.makedirs(new_dir_path, exist_ok=True)
    saveFile = new_dir_path + fileName + '.csv'

    # NOTE: r	ファイルを読み込み専用として開く。
    #       w	ファイルに書き込みをするために新規作成する。但し、存在するファイル名を指定すると、ファイルの中身が全て消えます。
    #       a	ファイルに書き込みするために開く。
    #       b   「バイナリモードで開く」
    f = open(saveFile, 'w')
    dataWriter = csv.writer(f)
    dataWriter.writerows(dataList)
    f.close()

# NOTE: 文章をリストにする
#       @param sentences: フルテキスト
def createSentenceData(sentences):
    # NOTE: column(縦）に文章を書き込んでいくため、
    #       2次元配列にする必要がある。
    rowList = []
    for index, item in enumerate(sentences):
        rowList.append([])
        rowList[index].append(item)
    
    return rowList

# NOTE: rowデータから形態素解析様の文章を作成する
#       @param row: csvのrowデータ
def prepareSentenceForAnalyzing(row):
    sentences = row['本文']

    return sentences

# NOTE: 必要であれば、作家名や作品タイトルなどを加える
#       @param row: csvのrowデータ
def getExtraWords(row):
    words = []
    
    # NOTE: 作者を追加
    words.append([])
    words[0].append(row['作者'])
    words[0].append(2)

    return words
    
def main():
    csv_file = open("datalist.csv", "r")
    # NOTE: 辞書形式
    dataList = csv.DictReader(csv_file)

    for row in dataList:
        splitedSentences = getSplitedSentences(row['本文'])

        # TODO: データが少ないので、現状は「作品名」も文章リストに加える
        reasonSentences = getSplitedSentences(row['作品名'])

        # NOTE: 文章リストをcsv形式で保存する
        saveSentences = createSentenceData(splitedSentences)
        
        # NOTE: 単語リストを作成する
        fileName = row['No.'] + '-sentences'
        saveDataList(saveSentences, fileName, 'sentences/')
        
        preparedWords = prepareSentenceForAnalyzing(row)
        saveWords = getWordsByMorphologicalAnalysis(preparedWords)

        # NOTE: 必要であれば、作家名や作品タイトルなどを加える
        # extraWords = getExtraWords(row)
        # saveWords.extend(extraWords)

        fileName = row['No.'] + '-words'
        saveDataList(saveWords, fileName, 'words/')

main()
