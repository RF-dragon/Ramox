# Ramox

（简体中文 | [English](README.en.md)）

### 介绍
本程序为基于Flask开发的微信自动回复机器人。本程序使用了由Daen开发的[DaenWxHook.dll](DaenWxHook/DaenWxHook.dll)用于读取微信内的活动并将活动信息发送到本地端口，详情请见其[接口文档](https://www.apifox.cn/apidoc/project-1222856/)。本程序仅提供自动回复功能框架，具体回复内容和信息处理算法请自行实现。

### 安装
1. 将仓库克隆或下载到本地。
2. 安装Python。请确保在安装过程中将Python添加到PATH。
3. 使用以下命令安装Flask：
```shell
python -m pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple -U
```

### 运行
1. 安装[微信3.6.0.18](WeChatSetup3.6.0.18.exe)。程序仅支持此版本微信。
2. 在[ramox.py](ramox.py)中实现“respond”函数。函数参数的相关信息已在注释中说明。
3. 运行[server.py](server.py)。
4. 运行[Daen注入器](DaenWxHook/Daen%E6%B3%A8%E5%85%A5%E5%99%A8.exe)。该程序会启动微信并将DaenWxHook.dll注入微信进程。其中，文件目录请填写微信所在的文件夹，DLL路径请填写[DaenWxHook.dll](DaenWxHook/DaenWxHook.dll)的文件路径，进程参数请填写callBackUrl=http://localhost:8089/wechat&port=8055&decryptImg=1。

您也可以自行修改[server.py](server.py)和[ramox.py](ramox.py)的代码，以实现更多功能。
请注意，对本程序的滥用可能违反[腾讯微信软件许可及服务协议](https://weixin.qq.com/agreement)，请遵循协议使用。本人不承担由于使用本程序而违反[腾讯微信软件许可及服务协议](https://weixin.qq.com/agreement)所带来的法律责任。

### 参考文献
Daen. (2022). _WeChat HOOK HTTP_. https://www.apifox.cn/apidoc/project-1222856
