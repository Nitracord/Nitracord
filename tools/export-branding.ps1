param()

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$brandRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../assets/branding'))
$githubRoot = Join-Path $brandRoot 'github'
New-Item -ItemType Directory -Path $githubRoot -Force | Out-Null

$exports = @(
    @{ Name = 'nitracord-icon.png'; Width = 512; Height = 512 },
    @{ Name = 'nitracord-banner.png'; Width = 1536; Height = 512 },
    @{ Name = 'nitracord-social-banner.png'; Width = 1280; Height = 640 }
)

foreach ($export in $exports) {
    $source = [System.Drawing.Image]::FromFile((Join-Path $brandRoot $export.Name))
    $destination = Join-Path $githubRoot $export.Name
    $width = $export.Width
    $height = $export.Height
    try {
        do {
            $bitmap = New-Object System.Drawing.Bitmap($width, $height, ([System.Drawing.Imaging.PixelFormat]::Format24bppRgb))
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            try {
                $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
                $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
                $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
                $graphics.DrawImage($source, 0, 0, $width, $height)
                $bitmap.Save($destination, [System.Drawing.Imaging.ImageFormat]::Png)
            } finally {
                $graphics.Dispose()
                $bitmap.Dispose()
            }
            $bytes = (Get-Item -LiteralPath $destination).Length
            if ($bytes -ge 1000000) {
                $width = [Math]::Max(1, [int][Math]::Floor($width * 0.9))
                $height = [Math]::Max(1, [int][Math]::Floor($height * 0.9))
            }
        } while ($bytes -ge 1000000)
        Write-Output "$($export.Name): $bytes bytes"
    } finally {
        $source.Dispose()
    }
}
