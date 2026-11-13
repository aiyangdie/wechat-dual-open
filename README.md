<p align="center"><img src="assets/covers/06-wechat-dual-open.jpg" alt="微信双开 项目封面" width="100%"></p>

<h1 align="center">双开微信 · WeChat Dual Open</h1>

<p align="center">C 语言编写的 Windows 便携版双开启动器，单文件 exe，约 155 KB</p>

<p align="center">
  <a href="https://github.com/aiyangdie/wechat-dual-open/releases/latest">下载 WxDual.exe</a> ·
  <a href="LICENSE">MIT 许可</a>
</p>

## 简介

面向 Windows 的微信双开小工具，主程序是纯 Win32 的 C 代码（`wx_dual.c`），编译后约 150 KB。仓库里另有编译脚本和图标生成脚本，属于辅助文件，不参与运行。

## 功能

- 自动查找本机 `Weixin.exe` / `WeChat.exe`
- 间隔 800 ms 连续启动两次，尝试双开
- `-mwindows` 编译，运行时无控制台黑窗
- 内置 16–256 多尺寸高清图标

## 使用

1. 下载 `WxDual.exe` 放到桌面或任意目录
2. 双击运行
3. 若只弹出一个窗口，说明当前微信版本已启用互斥锁，脚本无法绕过，这不是程序缺陷

## 自行编译

环境：Windows 10/11 + PowerShell；生成图标需要 Python 3。首次编译会自动下载便携 GCC（[w64devkit](https://github.com/skeeto/w64devkit)，约 60 MB）。

```powershell
powershell -ExecutionPolicy Bypass -File build_c.ps1
```

手动编译：

```powershell
python make_user_icon.py
windres wx_dual.rc -O coff -o wx_dual.res
gcc -O2 -s -mwindows -municode wx_dual.c wx_dual.res -o WxDual.exe -lshlwapi -lshell32
```

## 项目结构

```
wx_dual.c               主程序（C / Win32）
wx_dual.rc              图标资源定义
assets/icon-source.png  图标原图
assets/user-dual.ico    程序图标
build_c.ps1             一键编译
make_user_icon.py       图标生成
releases/双开微信.exe    发布用可执行文件
```

## 查找的微信路径

1. `C:\Program Files\Tencent\Weixin\Weixin.exe`
2. `C:\Program Files (x86)\Tencent\Weixin\Weixin.exe`
3. `C:\Program Files\Tencent\WeChat\WeChat.exe`
4. `C:\Program Files (x86)\Tencent\WeChat\WeChat.exe`
5. `%LOCALAPPDATA%\Programs\Tencent\WeChat\WeChat.exe`

## 免责声明

仅用于在个人电脑上同时启动两个微信客户端实例。请遵守微信用户协议与当地法律法规，作者不对使用后果负责。

## 许可证

[MIT](LICENSE) ｜ [aiyangdie](https://github.com/aiyangdie)
