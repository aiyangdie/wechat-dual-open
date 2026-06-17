# GitHub 登录问题修复说明

## 现象

`git-credential-manager.exe` 报错 **「字符串绑定无效」**，无法弹出 GitHub 登录窗口。

## 已做的修复

1. 清除了 Windows 里损坏的 GitHub 凭据
2. 重新写入了有效凭据
3. 为 GitHub 单独配置了 **凭据文件**（不再走 GCM 弹窗）：
   - 文件：`%USERPROFILE%\.git-credentials`
   - 配置：`credential.https://github.com.helper = store`

## 以后 token 过期了怎么办

双击运行 **`fix-github-auth.bat`**，按提示粘贴新 token 即可。

或手动：

1. https://github.com/settings/tokens → Generate new token (classic) → 勾选 **repo**
2. CMD 执行（替换 TOKEN）：

```cmd
(echo protocol=https& echo host=github.com& echo username=aiyangdie& echo password=TOKEN) | "C:\Program Files\Git\cmd\git.exe" credential approve
```

## 安全建议

- 不要把 token 发给任何人或贴在聊天里
- 若 token 曾泄露，请到 GitHub **Revoke** 后重新生成

## 常用命令

```cmd
cd C:\Users\aike1\Downloads\wechat-export\wechat-dual-open
git push
python publish_release.py
```
