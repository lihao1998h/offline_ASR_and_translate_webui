
print('程序已启动，请耐心等待')
import gradio as gr
import json
from offline_ASR_and_translate import *

with open('language.json', 'r', encoding='utf-8') as f:
    language_dict = json.load(f)

with open('language_baidu.json', 'r', encoding='utf-8') as f:
    language_baidu_dict = json.load(f)
def process_input(appid, appsecret, input_chinese_name, output_chinese_name, text_input, record):
    if output_chinese_name in language_baidu_dict:
        output_lang = language_baidu_dict[output_chinese_name]
    else:
        raise ValueError("output_lang未找到该语言")
        
    if input_chinese_name in language_dict:
        input_lang = language_dict[input_chinese_name]
    else:
        raise ValueError("input_lang未找到该语言")
    
    
    if text_input and not record:
        print('识别文本')
        ori_text, translated_text = ASR_and_translate(text_input, input_lang, output_lang, appid, appsecret)
    elif record and not text_input:
        print('识别音频或麦克风输入文件')
        ori_text, translated_text = ASR_and_translate(record, input_lang, output_lang, appid, appsecret)
    else:
        raise ValueError("输入格式错误")    
    
    return ori_text, translated_text


# 定义Gradio界面
title = "离线语音识别与翻译"
description = """支持三种输入形式:\n
                1.上传.wav文件 2.输入文本 3.录音输入\n
                接着选择输入语言和目标语言，点击Submit获取翻译结果。\n
                注意不要同时输入文本以及上传音频
                """
inputs = [
    gr.Textbox(label="百度翻译appid"),
    gr.Textbox(label="百度翻译secret_key"),
    gr.Dropdown(choices=list(language_dict.keys()), label="输入语言", value="自动检测"),
    gr.Dropdown(choices=list(language_baidu_dict.keys())[1:], label="目标语言", value="中文"),
    
    gr.Textbox(label="直接输入文本或wav文件路径"),
    gr.Audio(sources=["upload", "microphone"], type="filepath", label="上传文件/麦克风输入"),
]

outputs = [
    gr.Textbox(label="源文本或语音识别结果"),
    gr.Textbox(label="翻译结果"),
]

# 定义处理函数，包括对音频文件的预处理
demo = gr.Interface(
    fn=process_input,
    inputs=inputs,
    outputs=outputs,
    title=title,
    description=description,
    allow_flagging=False,  # 防止用户标记结果
)

demo.launch(share=False, server_name='127.0.0.1', server_port=7861, quiet=True)

time.sleep(5)
