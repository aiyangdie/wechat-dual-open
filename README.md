# 双开微信 (WeChat Dual Open)

Windows 便携版微信双开启动器：C 语言编写，单文件 exe，无需安装。

![icon](assets/icon-preview.png)

## 下载

直接运行（推荐）：

- [releases/双开微信.exe](releases/双开微信.exe) — 约 155 KB，双击即可

或编译目录中的 `WxDual.exe`（与发布版相同）。

## 功能

- 自动查找本机 **Weixin.exe** / **WeChat.exe**
- 间隔 800ms 连续启动两次，尝试双开
- 无控制台黑窗口
- 内置高清多尺寸图标

## 使用方法

1. 下载 `双开微信.exe` 到桌面或任意文件夹
2. 双击运行
3. 若只弹出一个微信窗口：说明当前微信版本已启用互斥锁，脚本无法绕过（非程序 bug）

## 自行编译

### 环境

- Windows 10 / 11
- PowerShell
- Python 3（仅用于生成 ICO，可用 [Hermes](https://github.com/) 自带 venv 或系统 Python）

首次编译会自动下载便携 GCC（[w64devkit](https://github.com/skeeto/w64devkit)），约 60MB，仅编译时需要。

### 步骤

```powershell
cd wechat-dual-open
powershell -ExecutionPolicy Bypass -File build_c.ps1
```

产物：

- `WxDual.exe` — 项目目录内
- 桌面 `双开微信.exe` — 自动复制（若路径编码正常）

### 手动编译

```powershell
python make_user_icon.py
# 需已安装 w64devkit，并将 bin 加入 PATH
windres wx_dual.rc -O coff -o wx_dual.res
gcc -O2 -s -mwindows -municode wx_dual.c wx_dual.res -o WxDual.exe -lshlwapi -lshell32
```

## 项目结构

| 文件 | 说明 |
|------|------|
| `wx_dual.c` | 主程序（查找微信路径、启动两次） |
| `wx_dual.rc` | 图标资源定义 |
| `make_user_icon.py` | 从 PNG 生成多尺寸 `user-dual.ico` |
| `user-dual.ico` | 程序图标（16～256 多档） |
| `build_c.ps1` | 一键编译脚本 |
| `releases/双开微信.exe` | 发布用可执行文件 |

## 查找的微信路径

1. `C:\Program Files\Tencent\Weixin\Weixin.exe`
2. `C:\Program Files (x86)\Tencent\Weixin\Weixin.exe`
3. `C:\Program Files\Tencent\WeChat\WeChat.exe`
4. `C:\Program Files (x86)\Tencent\WeChat\WeChat.exe`
5. `%LOCALAPPDATA%\Programs\Tencent\WeChat\WeChat.exe`

## 技术说明

- 语言：C（Win32 API）
- 链接：`shlwapi`、`shell32`
- 图标：`windres` 嵌入 `user-dual.ico`
- 体积：编译后约 150 KB（含图标资源）

## 免责声明

本工具仅用于在个人电脑上同时启动两个微信客户端实例。请遵守微信用户协议与当地法律法规。作者不对因使用本工具产生的任何问题负责。

## 作者

- GitHub: [@aiyangdie](https://github.com/aiyangdie)

## License

MIT License — 见 [LICENSE](LICENSE)
