import json
from translate import Translator
import urllib.parse
import requests
import time
import hashlib
# def translate_to_english(text):
#     translator = Translator(to_lang="en")
#     translation = translator.translate(text)
#     return translation


def translate_to_english(content):

    # 构造API请求参数
    url = 'http://openapi.youdao.com/api'
    app_key = '674bb63810a75fd5'
    app_secret = 'Zn6XoiTWKlOhjlZrYQS9kHNinISqMTuN'
    api_version = '1.1'
    from_lang = 'zh-CHS'
    to_lang = 'EN'
    text = '你好，世界！'
    salt = str(int(time.time() * 1000))
    sign = hashlib.md5((app_key + content + salt + app_secret).encode('utf-8')).hexdigest()

    # 构造请求头部信息
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'q': content, 'from': from_lang, 'to': to_lang, 'sign': sign, 'salt': salt, 'appKey': app_key}

    # 发送API请求
    response = requests.post(url, data=data, headers=headers)

    # 解析API返回的JSON数据
    result = json.loads(response.text)

    # 提取翻译结果
    translation = result['translation'][0]
    return translation


def locate_word_in_text(word, text):
    # 定位词语在文本中的位置
    start = text.find(word)
    end = start + len(word)
    # 位置调整为单词级别的位置计算
    adjusted_start = len(text[:start].split())
    adjusted_end = len(text[:end].split()) - 1  # -1 because words are 0-indexed
    return adjusted_start, adjusted_end


# 定位实体名称在tokens中的位置
def locate_entity_in_tokens(entity_name, tokens):
    words = entity_name.split()
    start = tokens.index(words[0])
    end = start + len(words) - 1
    return [start, end]

data = {"token": ["2018年7月7日凌晨，被告人杨某某来到**市**区凤山街道南城中央广场**号楼，武隆**证券公司，将被害人窦某某放在大厅前台的一部苹果6手机盗走，经**市**区价格认证中心认定，被盗手机价值760元人民币。"], "h": {"name": "窦某某", "pos": [54, 57]}, "t": {"name": "一部苹果6手机", "pos": [64, 71]}, "relation": "posses"}


# 用于标记姓名的特殊标记
marker_h = "H_NAME"
marker_t = "T_NAME"

# 在原始句子中标记姓名
token_with_markers = data['token'][0].replace(data['h']['name'], marker_h).replace(data['t']['name'], marker_t)

# 翻译整个句子
translated_text_with_markers = translate_to_english(token_with_markers)


# 单独翻译姓名
translated_h_name = translate_to_english(data['h']['name'])
translated_t_name = translate_to_english(data['t']['name'])

# 在翻译后的句子中定位姓名
h_pos_start = translated_text_with_markers.find(marker_h)
t_pos_start = translated_text_with_markers.find(marker_t)

# 替换标记为翻译后的姓名
translated_text = translated_text_with_markers.replace(marker_h, translated_h_name).replace(marker_t, translated_t_name)

tokens = translated_text.split()

# 计算新的位置
h_pos_end = locate_entity_in_tokens(translated_h_name, tokens)
t_pos_end = locate_entity_in_tokens(translated_t_name, tokens)

# 创建新的数据结构
new_data = {
    "token": tokens,
    "h": {
        "name": translated_h_name,
        "pos": h_pos_end
    },
    "t": {
        "name": translated_t_name,
        "pos": t_pos_end
    },
    "relation": translate_to_english(data['relation'])
}

# 输出结果
print(json.dumps(new_data, ensure_ascii=False, indent=2))