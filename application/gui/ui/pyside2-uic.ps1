Get-ChildItem ".\" -Filter *.ui |
Foreach-Object {
    pyside2-uic $_.FullName | Set-Content -Encoding UTF8 -Path ('..\generated\' + $_.BaseName + '.py')
    if($LASTEXITCODE -eq 1) {
        Pause
    }
}
exit