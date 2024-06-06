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
    time.sleep(1)
    # 构造API请求参数
    url = 'http://openapi.youdao.com/api'
    app_key = '674bb63810a75fd5'
    app_secret = 'Zn6XoiTWKlOhjlZrYQS9kHNinISqMTuN'
    api_version = '1.1'
    from_lang = 'zh-CHS'
    to_lang = 'EN'
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

    # 尝试查找起始和结束位置
    try:
        start = tokens.index(words[0])
        end = start + len(words) - 1

        # 检查结束位置是否超出 tokens 的范围
        if end >= len(tokens):
            raise IndexError

    except (ValueError, IndexError):
        # 如果找不到起始位置或结束位置超出范围，返回 None
        return None

    return [start, end]

def process_data(data):
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


    if not translated_text_with_markers or not translated_h_name or not translated_t_name:
        print("Error: one or more translations are empty\n")
        return None

    # 在翻译后的句子中定位姓名
    h_pos_start = translated_text_with_markers.find(marker_h)
    t_pos_start = translated_text_with_markers.find(marker_t)

    # 替换标记为翻译后的姓名
    translated_text = translated_text_with_markers.replace(marker_h, ' '+translated_h_name+' ').replace(marker_t,' '+ translated_t_name+' ')

    import re
    tokens = re.findall(r'\b\w+\b|\S', translated_text)

   
    # 计算新的位置
    h_pos_end = locate_entity_in_tokens(translated_h_name, tokens)
    t_pos_end = locate_entity_in_tokens(translated_t_name, tokens)

    if not h_pos_end or not t_pos_end:
        print("Error\n")
        return None
    
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
    return new_data

with open('change2.txt', 'r', encoding='utf-8') as f_in, open('ok.txt', 'w', encoding='utf-8') as f_out:
    for line in f_in:
        data = json.loads(line.strip())
        new_data = process_data(data)
        if not new_data:
            continue  # 忽略空的 new_data，进入下一个循环

        f_out.write(json.dumps(new_data, ensure_ascii=False))
        f_out.write('\n')
        f_out.flush()  # 刷新缓冲区内容到文件