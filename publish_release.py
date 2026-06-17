"""Create GitHub Release and upload 双开微信.exe."""
import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

REPO = "aiyangdie/wechat-dual-open"
TAG = "v1.0.0"
ROOT = Path(__file__).resolve().parent
EXE = ROOT / "releases" / "双开微信.exe"


def get_token() -> str:
    p = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        text=True,
        capture_output=True,
        check=True,
    )
    for line in p.stdout.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1]
    raise RuntimeError("No GitHub token in credential store")


def api(method: str, url: str, token: str, data: bytes | None = None, headers: dict | None = None):
    h = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} -> {e.code}: {body}") from e


def main():
    if not EXE.exists():
        raise FileNotFoundError(f"Missing {EXE}; run build_c.ps1 first")

    token = get_token()
    base = f"https://api.github.com/repos/{REPO}"

    # Reuse existing release or create
    try:
        rel = api("GET", f"{base}/releases/tags/{TAG}", token)
        print(f"Release exists: {rel['html_url']}")
    except RuntimeError:
        payload = json.dumps(
            {
                "tag_name": TAG,
                "name": "v1.0.0 — 双开微信",
                "body": (
                    "## 双开微信\n\n"
                    "Windows 便携版微信双开启动器（C 语言，无需安装）。\n\n"
                    "### 使用\n"
                    "1. 下载 **双开微信.exe**\n"
                    "2. 双击运行\n\n"
                    "### 说明\n"
                    "- 自动查找 Weixin / WeChat 并连续启动两次\n"
                    "- 若只开一个窗口，为微信版本互斥锁限制"
                ),
                "draft": False,
                "prerelease": False,
            }
        ).encode("utf-8")
        rel = api(
            "POST",
            f"{base}/releases",
            token,
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        print(f"Created: {rel['html_url']}")

    upload_url = rel["upload_url"].split("{")[0]
    # GitHub asset API: ASCII name is most reliable; Chinese shown in release title/body
    asset_name = "WxDual.exe"
    exe_bytes = EXE.read_bytes()
    url = f"{upload_url}?name={urllib.parse.quote(asset_name)}"

    # Remove old asset with same name
    for asset in rel.get("assets", []):
        if asset["name"] == asset_name:
            api("DELETE", asset["url"], token)
            print(f"Removed old asset: {asset_name}")

    asset = api(
        "POST",
        url,
        token,
        data=exe_bytes,
        headers={"Content-Type": "application/octet-stream"},
    )
    print(f"Uploaded: {asset['name']} ({asset['size']} bytes)")
    print(f"Download: {asset['browser_download_url']}")


if __name__ == "__main__":
    main()
