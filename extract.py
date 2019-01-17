import regex
import csv
import os
import re

from collections import Counter
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import *
from MorphologicalAnalysis import getWordsByMorphologicalAnalysis

def getSplitedSentences(txt):
    # sen = regex.split(r'(?<=[。？])(?!$)', txt, flags=regex.VERSION1)
    sen = re.findall(r'[^。]+(?:[。]|$)', txt)
    return sen

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

def createSentenceData(sentences):
    # NOTE: column(縦）に文章を書き込んでいくため、
    #       2次元配列にする必要がある。
    rowList = []
    for index, item in enumerate(sentences):
        rowList.append([])
        rowList[index].append(item)
    
    return rowList

# NOTE: rowデータから形態素解析様の文章を作成する
def prepareSentenceForAnalyzing(row):
    sentences = row['説明文']
    sentences += row['贈呈理由']

    return sentences

# NOTE: 必要であれば、作家名や作品タイトルなどを加える
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
        splitedSentences = getSplitedSentences(row['説明文'])

        # TODO: データが少ないので、現状は「贈呈理由」も文章リストに加える
        reasonSentences = getSplitedSentences(row['贈呈理由'])
        splitedSentences.extend(reasonSentences)
        
        # 文章リストをcsv形式で保存する
        saveSentences = createSentenceData(splitedSentences)
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
