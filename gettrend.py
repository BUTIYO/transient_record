# -*- coding: utf-8 -*-
import MeCab
import jaconv
import re, regex
from pykakasi import kakasi
from pytrends.request import TrendReq
import pandas, numpy, random, requests

#MeCab設定
tagger_neolog = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
tagger = MeCab.Tagger("-Ochasen")

#kakasi設定
kakasi = kakasi()
kakasi.setMode('J', 'H')  # J(Kanji) to H(Hiragana)
conv = kakasi.getConverter()

#使用可能文字列の正規表現
p = re.compile('[0-9a-zA-Zあ-んー\u30A1-\u30F4]+')


pytrends = TrendReq(hl='ja-JP', tz=360)
trends = pytrends.trending_searches(pn='japan')
trends = trends.values.tolist()

trendList = []
# print("-----Googleトレンド上位20語-----")
for t in trends:
    # print(t[0])
    if p.fullmatch(t[0]):
        #トレンドが正規表現にマッチ
        trendList.append(t[0])
    else:
        #トレンドが正規表現にマッチせず
        ans = ""
        words = []
        result = tagger.parse(t[0]).split("\n")
        for res in result:
            words.append(tagger.parse(res).split("\t"))
        for word in words:
            if len(word) > 1 and word[0] != "EOS":
                if regex.findall(r'\p{Han}+',word[0]):
                    if not regex.findall(r'\p{Han}+',word[1]):
                        ans += jaconv.kata2hira(word[1])
                    else:
                        ans += conv.do(word[1])
                else:
                    ans += word[0]
        trendList.append(ans)

# print("-----漢字をひらがなに変換-----")
# print(trendList)
word = random.choice(trendList)
# print("-----ランダムに1語抽出-----")
# print(word)

# print("-----ドット列を取得-----")
for ch in word:
    print(ch)
    res = requests.get("https://arcane-bayou-55620.herokuapp.com/getArray/"+ch)
    print(res.text)
