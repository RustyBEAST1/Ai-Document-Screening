param(
    [Parameter(Mandatory=$true)][string]$ImagePath
)

$ErrorActionPreference = 'Stop'

try {
    [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
    [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
    [Windows.Storage.StorageFile, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null

    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $asTaskGeneric = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { 
        $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' 
    } | Select-Object -First 1

    function Await-WinRt($WinRtTask, $ResultType) {
        $netTask = $asTaskGeneric.MakeGenericMethod($ResultType).Invoke($null, @($WinRtTask))
        $netTask.Wait(-1) | Out-Null
        return $netTask.Result
    }

    $fullPath = [System.IO.Path]::GetFullPath($ImagePath)
    if (-not (Test-Path $fullPath)) {
        Write-Output '{"success": false, "error": "File not found"}'
        exit 0
    }

    $file = Await-WinRt ([Windows.Storage.StorageFile]::GetFileFromPathAsync($fullPath)) ([Windows.Storage.StorageFile])
    $stream = Await-WinRt ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Await-WinRt ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Await-WinRt ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])

    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    if (-not $engine) {
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new("en-US"))
    }

    $ocrResult = Await-WinRt ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    
    $lines = @()
    foreach ($l in $ocrResult.Lines) {
        $lines += $l.Text
    }

    $res = @{
        success = $true
        text = $ocrResult.Text
        lines = $lines
    }
    $res | ConvertTo-Json -Compress
}
catch {
    $err = @{
        success = $false
        error = $_.Exception.Message
        text = ""
        lines = @()
    }
    $err | ConvertTo-Json -Compress
}
