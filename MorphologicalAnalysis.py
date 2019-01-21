# reference from:
# http://mocobeta.github.io/janome/#id11
# http://eneprog.blogspot.com/2018/06/pythonjanome.html
# https://akamist.com/blog/archives/2659

import csv
import os
from collections import Counter
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import *

def dumpWord(sentences):
    # ワードと品詞リストをダンプ
    t = Tokenizer()
    for token in t.tokenize(sentences):
        print(token)

def getWordsByMorphologicalAnalysis(sentences):
    # NOTE: 
    #       POSKeepFilter       名詞のみフィルタ
    #       POSStopFilter       指定された品詞タグにマッチするトークンを除去
    #       TokenCountFilter    入力文字列中の単語出現頻度を数える
    token_filters = [
        POSKeepFilter("名詞"),
        POSStopFilter(["名詞,代名詞","名詞,非自立","名詞,数", "名詞,接尾,特殊", "名詞,接尾,一般", "名詞,接尾,形容動詞語幹", "名詞,接尾,サ変接続", "名詞,サ変接続"]),
        TokenCountFilter()]

    analyzer = Analyzer(token_filters=token_filters)
    
    # NOTE: column(縦）に文章を書き込んでいくため、
    #       2次元配列にする必要がある。
    words = []
    analyzedData = analyzer.analyze(sentences)
    for index, item in enumerate(analyzedData):
        words.append([])
        words[index].append(item[0])
        words[index].append(item[1])

    return words

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

# NOTE: Test code here. Comment out following all codes.
# full_text =  "皆が寝静まったころ、宙に浮いたようなベルトコンベアが静かに稼働している。そこは「D」「R」「E」「A」「M」という文字がつくられる工場。NHK教育テレビで放映している番組「Eテレ2355」のおやすみソングとして制作、放送されたアニメーション。でき上がった「DREAM」は、「おやすみなさい」と各国のことばで書かれた箱に詰められる。(3分46秒)"
# words = getWordsByMorphologicalAnalysis(full_text)
# print(words)
# fileName = 'sample'
# directory = 'words/'
# saveDataList(words, fileName, 'words/')
# dumpWord(full_text)