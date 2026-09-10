# 把两个桌面程序打包成单文件 exe，产物输出到仓库根目录的 dist\
#
#   pip install pyinstaller
#   .\scripts\build.ps1
#
# 网页程序 apps\vector-basics\app.py 是 Dash 服务，直接 python 运行即可，不在此打包。

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Error "未找到 pyinstaller，请先运行: pip install pyinstaller"
}

$targets = @(
    @{ Name = 'derivative_visualizer'; Script = 'apps\derivative-definition\derivative_visualizer.py' },
    @{ Name = 'integral_visualizer';   Script = 'apps\definite-integral\integral_visualizer.py' }
)

foreach ($t in $targets) {
    Write-Host "==> 正在打包 $($t.Name) ..." -ForegroundColor Cyan
    pyinstaller --noconfirm --onefile --windowed `
        --name $t.Name `
        --distpath "$root\dist" `
        --workpath "$root\build" `
        --specpath "$root\build" `
        $t.Script
    if ($LASTEXITCODE -ne 0) { Write-Error "$($t.Name) 打包失败" }
}

Write-Host "`n打包完成，产物位于 $root\dist" -ForegroundColor Green
Get-ChildItem "$root\dist" -Filter *.exe | Select-Object Name, @{ N = 'Size(MB)'; E = { [math]::Round($_.Length / 1MB, 1) } }
