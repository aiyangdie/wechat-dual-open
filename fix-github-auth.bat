@echo off
chcp 65001 >nul
setlocal
set GIT="C:\Program Files\Git\cmd\git.exe"
echo ========================================
echo   GitHub 凭据修复（无需 GCM 弹窗）
echo ========================================
echo.
echo 1. 打开 https://github.com/settings/tokens
echo 2. Generate new token ^(classic^) - 勾选 repo
echo 3. 复制 token，粘贴到下面（输入时不会显示）
echo.
set /p PAT=请输入 GitHub Token: 
if "%PAT%"=="" (
  echo 未输入 token，已取消。
  exit /b 1
)
(
  echo protocol=https
  echo host=github.com
  echo username=aiyangdie
  echo password=%PAT%
) | %GIT% credential approve
echo.
echo 凭据已保存。正在测试连接...
cd /d "%~dp0"
%GIT% ls-remote origin HEAD >nul 2>&1
if errorlevel 1 (
  echo [失败] token 无效或已过期，请重新生成。
  exit /b 1
)
echo [成功] GitHub 已连通，可以 git push 了。
pause
