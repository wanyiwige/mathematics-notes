Add-Type -AssemblyName System.Drawing
$projectRoot = 'C:\Users\WANYIWIGE\Desktop\我的笔记\常微分方程'
$plan = @(
    @{ Chapter=7; Source='0014.png'; Bias=0.50 },
    @{ Chapter=8; Source='0066.png'; Bias=0.15 },
    @{ Chapter=9; Source='0161.png'; Bias=1.00 },
    @{ Chapter=10; Source='0228.png'; Bias=0.50 },
    @{ Chapter=11; Source='0286.png'; Bias=0.90 },
    @{ Chapter=12; Source='0303.png'; Bias=0.50 },
    @{ Chapter=13; Source='0305.png'; Bias=0.60 },
    @{ Chapter=14; Source='0358.png'; Bias=0.50 },
    @{ Chapter=15; Source='0473.png'; Bias=0.50 }
)
$encoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$parameters = [System.Drawing.Imaging.EncoderParameters]::new(1)
$parameters.Param[0] = [System.Drawing.Imaging.EncoderParameter]::new([System.Drawing.Imaging.Encoder]::Quality,[long]95)
$records = @()
foreach ($item in $plan) {
    $sourcePath = Join-Path $projectRoot ('figure\' + $item.Source)
    $outputPath = Join-Path $projectRoot ('figure\Chapter' + $item.Chapter + '封面图.jpg')
    if (Test-Path -LiteralPath $outputPath) { throw ('不覆盖已有封面: ' + $outputPath) }
    $sourceImage = [System.Drawing.Image]::FromFile($sourcePath)
    # 38:25 = 1.52:1，以整像素裁切；不拉伸原图。
    $scaleUnit = [Math]::Floor([Math]::Min($sourceImage.Width / 38, $sourceImage.Height / 25))
    $cropWidth = [int](38 * $scaleUnit)
    $cropHeight = [int](25 * $scaleUnit)
    $cropLeft = [int][Math]::Round(($sourceImage.Width - $cropWidth) * $item.Bias)
    $cropTop = [int][Math]::Round(($sourceImage.Height - $cropHeight) / 2)
    $resultImage = [System.Drawing.Bitmap]::new(2280,1500,[System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $graphics = [System.Drawing.Graphics]::FromImage($resultImage)
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $graphics.DrawImage($sourceImage,[System.Drawing.Rectangle]::new(0,0,2280,1500),[System.Drawing.Rectangle]::new($cropLeft,$cropTop,$cropWidth,$cropHeight),[System.Drawing.GraphicsUnit]::Pixel)
    $resultImage.Save($outputPath,$encoder,$parameters)
    $records += [PSCustomObject]@{Chapter=$item.Chapter;Source=$item.Source;Output=[System.IO.Path]::GetFileName($outputPath);Crop=@($cropLeft,$cropTop,$cropWidth,$cropHeight);Width=2280;Height=1500;Ratio=1.52}
    $graphics.Dispose(); $resultImage.Dispose(); $sourceImage.Dispose()
}
$records | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $projectRoot '教材对照\工作材料\新增章节封面记录.json') -Encoding utf8
$parameters.Dispose()
$records | Format-Table Chapter,Source,Output,Width,Height,Ratio
