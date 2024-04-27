

# 1 一键安装包
全语种语音识别和翻译一键安装包：

下载地址1：
链接：https://www.123pan.com/s/m7g3Td-qYPxH.html 
提取码：sJN1
下载地址2：
链接：https://pan.baidu.com/s/1Nc7m0FnuH0YQeZEijWmKEg?pwd=dk5w 
提取码：dk5w 

注意：
1. 自动检测语种可能会有识别错误
2. 请参考2.2配置百度翻译api key
3. 目前仅支持近30种语言
4. 模型加载时间较长，请耐心等待




# 2 给开发者的
## 2.1 环境
有conda环境可以通过以下代码启动
```bash
conda env create -f ASR_trans.yaml --name ASR_trans
```

接着上网去 https://huggingface.co/Systran/faster-whisper-large-v3

下载模型文件，存到models/faster-whisper-large-v3路径下，当然你也可以在offline_ASR_and_translate.py中自己更改路径。

## 2.2 配置

我目前的翻译功能用的是百度翻译api：http://api.fanyi.baidu.com

以下是配置步骤
1. 首先打开网址
![step1](images/step1.png)
2. 接着注册登录百度开发者
![step2](images/step2.png)

3. 确定
![step3](images/step3.png)

4. 回到首页打开开发者信息
![step4](images/step4.png)

5. 请在webui中设置自己的appid和secret_key
![step5](images/step5.png)


## 2.3 使用
```bash
python offline_ASR_and_translate_webui
```
即可启动webui，启动后通常在http://127.0.0.1:7861使用。
