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
        POSStopFilter(["名詞,代名詞","名詞,非自立","名詞,数", "名詞,接尾,特殊", "名詞,接尾,一般", "名詞,接尾,形容動詞語幹"]),
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

full_text =  "短編アニメーションという、自由度の高いパーソナルな表現単位を組み合わせて長編に見立てる試みは以前から数多く行われてきた。スタイルや方法論が異なり、バラバラになりがちな各々の作品を繋ぐルールとして日本独自の“連句”を導入したことで、従来とは一線を画する強い必然を持った一本の「長編」を構築したのが本作である。その短さから発表形態に制約を受けがちな短編アニメーションに対する新たな可能性の開拓と、日本独自の文化をアニメーションという表現を用いて発展させたことは、本年度最大の収穫といえよう。そして参加した作家陣の華やかな競演を、普段短編アニメーションに接することのない人たちにこそ観て欲しい。"
words = getWordsByMorphologicalAnalysis(full_text)
# print(words)
# fileName = 'sample'
# directory = 'words/'
# saveDataList(words, fileName, 'words/')
# dumpWord(full_text)