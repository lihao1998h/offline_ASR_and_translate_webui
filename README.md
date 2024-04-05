
# 准备
## 环境
有conda环境可以通过以下代码启动
```bash
conda create -n ASR_trans python=3.10.13 -y
conda activate ASR_trans
pip install -r requirements.txt

```

接着上网去 https://huggingface.co/Systran/faster-whisper-large-v3

下载模型文件，存到models/faster-whisper-large-v3路径下，当然你也可以在offline_ASR_and_translate.py中自己更改路径。

## 配置文件

我目前的翻译功能用的是百度翻译api：http://api.fanyi.baidu.com

请在offline_ASR_and_translate.py文件中设置自己的appid和secret_key

# 使用
```bash
python offline_ASR_and_translate_webui
```
即可启动webui，启动后通常在http://127.0.0.1:7861使用。