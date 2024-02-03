# 微信小程序挂机脚本框架
## 概述
- 程序自动识别小程序窗口位置，控制鼠标点击设定位置
- 使用tkinter生成控制界面，设定自定义按钮并定制对应功能
- 单线程自动控制，防止多个自定义功能抢占鼠标

## base框架介绍
### interface.py
- 设置tkinter控制界面，默认有两个按钮和一个显示文本窗口。其中一个按钮为“刷新小程序窗口位置”，防止启动程序后再次拖动窗口导致定位错误；另一个按钮为“停止[ESC]”，程序运行中可点击此按钮或按[ESC]停止进程。显示窗口可提示进程运行情况，或判断小程序窗口是否位于桌面顶端
- draw_windows函数提供自定义按钮接口，用户以列表形式设置按钮显示文本botton_name和按钮触发函数botton_func
- 用户自定义函数可调用text_write让控制界面显示提示文本

### mouse_control.py
- 使用pyautogui控制鼠标，该框架可由两种方式定位用户想要点击的小程序目标位置：
  1. 对于小程序中位置不变的区域，可直接设定坐标，将小程序拖到屏幕左上角，用微信截图查看点击位置的坐标，并记录使用
  2. 对于小程序中位置可变的区域，可使用opencv模板匹配，微信截图目标区域，调用template_match得到区域实时坐标，并控制鼠标点击
- 调用click函数控制鼠标点击，传入区域相对坐标，程序可自动识别小程序位置并加上偏移量得到全局绝对坐标，从而控制鼠标点击
- move函数只移动不点击

### config.py
- 开始之前使用微信截图截取整个小程序（微信截图有粘附功能，会自动识别小程序窗口），将其保存到'example/自定义文件夹/imgs/2560+1600/full_screen.png'，框架会使用opencv定位小程序顶部标题栏，并将其保存，以后会使用模板匹配得到小程序实时位置
- 参数配置文件，其中img_map字典默认保存小程序和顶部标签栏，用户在继承configBase时可扩展，便于自定义多次调用

## examples
- 存储自定义小程序脚本，个人做了**数独趣味闯关**、**肥鹅健身房**、 **侠客梦**，具体小程序脚本功能描述查看各个文件夹内部README.md


## 打包exe文件步骤
- 完成自定义脚本后可保存为exe文件，方便往后多次调用，省去打开IDE并运行的步骤
1. 创建最小新环境：conda create -n game_script python==3.8
2. 安装必要的包：pip install xxx
3. 安装Pyinstaller：pip install Pyinstaller
4. 进入要打包的python文件目录：cd xxx
5. 生成spec文件（同目录下生成），这里指定程序入口文件：pyi-makespec -F -w xxx.py
6. 在Analysis的第一个元素列表中添加所需的附加python文件，注意有单引号
7. 生成exe文件，exe文件在同级目录dist文件夹内，若需要额外的资源文件，
   需要将exe文件移到原python文件路径下，生成的build文件夹和dist文件夹可删除：
   Pyinstaller xxx.spec
8. 双击exe文件可运行