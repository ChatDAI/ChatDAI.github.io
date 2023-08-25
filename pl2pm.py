import requests
from pypinyin import lazy_pinyin
from Pinyin2Hanzi import DefaultDagParams, dag

def pinyin_2_hanzi(pinyinList):   
    dagParams = DefaultDagParams()
    result = dag(dagParams, pinyinList, path_num=1, log=True)
    for item in result:
        res = item.path 
        res_word = ''
        for word in res:
            res_word += word
        return res_word
    
base_url = "http://olime.baidu.com/py"

def getPrimitive(punchline):
    lists = lazy_pinyin(punchline)
    pinyin = ""
    for l in lists:
        if l.encode('utf-8').isalpha():
            pinyin+=l+"'"
    pinyin_2 = pinyin[:len(pinyin) - 1]
    pinyin = pinyin.replace("'","")
    params = {
        "py": pinyin,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json() 
        try:
            return data['0'][0][0][0]
        except:
            try:
                return requests.get(base_url, params={"py": pinyin_2,}).json()['0'][0][0][0]
            except:
                return pinyin_2_hanzi(lists)
    else:
        return pinyin_2_hanzi(lists)