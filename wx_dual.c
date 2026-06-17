/*
 * wx_dual.c — portable WeChat / Weixin dual-instance launcher (Windows)
 * Compile: see build_c.ps1
 */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shellapi.h>
#include <shlwapi.h>

#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "shell32.lib")

static const wchar_t *SEARCH_PATHS[] = {
    L"C:\\Program Files\\Tencent\\Weixin\\Weixin.exe",
    L"C:\\Program Files (x86)\\Tencent\\Weixin\\Weixin.exe",
    L"C:\\Program Files\\Tencent\\WeChat\\WeChat.exe",
    L"C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe",
    NULL,
};

static const wchar_t *find_wechat(void)
{
    static wchar_t local_path[MAX_PATH];

    for (int i = 0; SEARCH_PATHS[i]; i++) {
        if (PathFileExistsW(SEARCH_PATHS[i]))
            return SEARCH_PATHS[i];
    }

    if (ExpandEnvironmentStringsW(
            L"%LOCALAPPDATA%\\Programs\\Tencent\\WeChat\\WeChat.exe",
            local_path, MAX_PATH) > 0 && PathFileExistsW(local_path))
        return local_path;

    return NULL;
}

static BOOL launch_wechat(const wchar_t *exe)
{
    wchar_t dir[MAX_PATH];
    wcscpy_s(dir, MAX_PATH, exe);
    PathRemoveFileSpecW(dir);

    HINSTANCE r = ShellExecuteW(NULL, L"open", exe, NULL, dir, SW_SHOWNORMAL);
    return (INT_PTR)r > 32;
}

int WINAPI wWinMain(
    HINSTANCE hInstance,
    HINSTANCE hPrevInstance,
    LPWSTR lpCmdLine,
    int nShowCmd)
{
    (void)hInstance;
    (void)hPrevInstance;
    (void)lpCmdLine;
    (void)nShowCmd;

    const wchar_t *wx = find_wechat();
    if (!wx) {
        MessageBoxW(
            NULL,
            L"未找到微信。\n请确认已安装 Weixin / WeChat。",
            L"双开微信",
            MB_OK | MB_ICONERROR);
        return 1;
    }

    if (!launch_wechat(wx)) {
        MessageBoxW(
            NULL,
            L"第一次启动失败。",
            L"双开微信",
            MB_OK | MB_ICONERROR);
        return 1;
    }

    Sleep(800);

    if (!launch_wechat(wx)) {
        MessageBoxW(
            NULL,
            L"第二次启动失败。",
            L"双开微信",
            MB_OK | MB_ICONERROR);
        return 1;
    }

    return 0;
}
