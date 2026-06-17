# Build C wx_dual.exe with user-provided icon -> Desktop 双开微信.exe (no shortcut)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = "C:\Users\aike1\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
if (-not (Test-Path $python)) { $python = "python" }

& $python (Join-Path $here "make_user_icon.py")

function Resolve-W64Devkit {
    param([string]$Base)
    $candidates = @(
        (Join-Path $Base "bin\gcc.exe"),
        (Join-Path $Base "w64devkit\bin\gcc.exe")
    )
    foreach ($g in $candidates) {
        if (Test-Path $g) {
            $bin = Split-Path $g -Parent
            return @{
                Gcc = $g
                Windres = Join-Path $bin "windres.exe"
            }
        }
    }
    return $null
}

$kitRoot = Join-Path $here "w64devkit"
$tools = Resolve-W64Devkit $kitRoot

if (-not $tools) {
    $dl = Join-Path $here "w64devkit-installer.exe"
    Write-Host "Downloading w64devkit (portable GCC)..."
    Invoke-WebRequest -Uri "https://github.com/skeeto/w64devkit/releases/download/v2.8.0/w64devkit-x64-2.8.0.7z.exe" `
        -OutFile $dl -UseBasicParsing
    New-Item -ItemType Directory -Force -Path $kitRoot | Out-Null
    Start-Process -FilePath $dl -ArgumentList "-o$kitRoot","-y" -Wait -NoNewWindow
    $tools = Resolve-W64Devkit $kitRoot
    if (-not $tools) { throw "w64devkit install failed" }
}

$gcc = $tools.Gcc
$windres = $tools.Windres
$env:PATH = (Split-Path $gcc -Parent) + ";" + $env:PATH

Push-Location $here
& $windres wx_dual.rc -O coff -o wx_dual.res
& $gcc -O2 -s -mwindows -municode wx_dual.c wx_dual.res -o WxDual.exe -lshlwapi -lshell32
$ec = $LASTEXITCODE
Pop-Location
if ($ec -ne 0) { throw "gcc build failed" }

$deployScript = @'
from pathlib import Path
import shutil
root = Path(__file__).resolve().parent
src = root / "WxDual.exe"
dst = Path.home() / "Desktop" / "双开微信.exe"
shutil.copy2(src, dst)
lnk = Path.home() / "Desktop" / "双开微信.lnk"
if lnk.exists():
    lnk.unlink()
print("deployed", dst.stat().st_size)
'@
$tmp = Join-Path $here "_deploy.py"
[System.IO.File]::WriteAllText($tmp, $deployScript, [System.Text.UTF8Encoding]::new($false))
& $python $tmp
Remove-Item $tmp -Force

Write-Host "OK: $(Join-Path $here 'WxDual.exe')"
