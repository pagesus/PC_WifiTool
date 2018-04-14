/*
Updated Date: 2018/4/8
Updater: Wayne
Label: 001
*/

[文档结构]
Source Code
	--pause.png		资源文件
	--start.png		资源文件
	--wifi.ico		图标文件用于PyInstaller打包文件使用
	--wifi.png      资源文件
	--WifiTool.py   主程序
Release
	--WifiTool.7z	使用PyInstaller打包之后生成的可执行文件
	
[说明]
(1)该文件仅仅为简单的Wifi设置工具，在Win7上测试可行
(2)该工具打包之后由于Python中执行外部批处理命令，会出现cmd执行框的效果，该问题当前不解决，暂时遗留
