import time
s_time = time.time()

from faster_whisper import WhisperModel
from funasr import AutoModel
import os
from langdetect import detect
import requests
from hashlib import md5
import random
import torch
import json

e_time = time.time()
print(f'import time: {e_time-s_time:.2f}s') 

with open('language_baidu.json', 'r', encoding='utf-8') as f:
    language_baidu_dict = json.load(f)
with open('language.json', 'r', encoding='utf-8') as f:
    language_dict = json.load(f)
    
def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None  # 如果未找到匹配的值，则返回None或其他默认值


def check_(lang):
    lang_chinese = get_key_by_value(language_dict, lang)

    # 根据language_baidu_dict中的键值对规则转换lang值
    if lang_chinese:
        lang = language_baidu_dict.get(lang_chinese, lang)
    
    return lang

s_time = time.time()
ASR_MODEL_PATH = 'models/faster-whisper-large-v3'

# 从本地目录加载模型
if torch.cuda.is_available():
    faster_whisper_model = WhisperModel(ASR_MODEL_PATH, device="cuda", compute_type="float16")
else:
    faster_whisper_model = WhisperModel(ASR_MODEL_PATH, device="cpu", compute_type="int8")

funasr_model = AutoModel(model="paraformer-zh", model_revision="v2.0.4",
                vad_model="fsmn-vad", vad_model_revision="v2.0.4",
                punc_model="ct-punc-c", punc_model_revision="v2.0.4",
                # spk_model="cam++", spk_model_revision="v2.0.2",
                )
    
e_time = time.time()
print(f'加载模型 time: {e_time-s_time:.2f}s')  
def translate(query, src_lang, dest_lang, appid, secret_key):    
    # 百度翻译
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path


    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + secret_key)
    
    # 缩写不匹配
    src_lang = check_(src_lang)
    dest_lang = check_(dest_lang)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': src_lang, 'to': dest_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    
    # 获取翻译后的文本
    try:
        translated_text = result['trans_result'][0]['dst']
    except (KeyError, IndexError):
        return "翻译过程中发生错误，请检查输入和API密钥！"
    
    return translated_text
def ASR(audio_path):
    '''
    audio_path为.wav文件
    用fast-whisper（适配非中文）和funasr（适配中文）
    '''
    
    segments, info = faster_whisper_model.transcribe(audio_path, beam_size=5, vad_filter=True)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    
    if info.language in ['zh']:
        ret = funasr_model.generate(input=audio_path, 
                    batch_size_s=300, 
                    )
        res = ret[0]['text']
    else:
        res = ''
        for segment in segments:
            # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            res += f"{segment.text},"
        res = res[:-1]
    
    return res, info.language

def ASR_and_translate(input, input_lang=None, output_lang='zh', appid=None, appsecret=None):
    s_time = time.time()
    if os.path.isfile(input):
        res, lang = ASR(input)
        print('ASR结果:', res)
        print('语种识别结果', lang)
    elif isinstance(input, str):  # 判断是否为文本
        lang = detect(input)  # 自定义函数检测语种
        res = input
    e_time = time.time()
    print(f'ASR time: {e_time-s_time:.2f}s')
    
    if input_lang != 'auto':
        lang = input_lang
    
    if lang == output_lang:
        return res, res
    else:
        s_time = time.time()
        translated_text = translate(res, lang, output_lang, appid, appsecret)  # 翻译成母语
        e_time = time.time()
        print(f'translate time: {e_time-s_time:.2f}s')
        return res, translated_text # type: ignore
    