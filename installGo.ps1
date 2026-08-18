# Install the current Go release
param(
    [string]$w='c:\go',
    [string]$v='1.26.6'
)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
$OutputVariable = (go version) | Out-String
if ($?) {
    Write-Host 'Go Installed Already ...' $OutputVariable
    exit 0
}
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$env:GOPATH = 'C:\go'
$newPath = ('{0}\bin;C:\Program Files\Go\bin;{1}' -f $env:GOPATH, $env:PATH)
Write-Host ('Updating PATH: {0}' -f $newPath)
[Environment]::SetEnvironmentVariable('PATH', $newPath, [EnvironmentVariableTarget]::User)
$url = "https://dl.google.com/go/go$v.windows-amd64.zip"
Write-Host ('Downloading {0} ...' -f $url)
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -Uri $url -OutFile 'go.zip'
Write-Host 'Expanding ...'
Expand-Archive go.zip -DestinationPath C:\
Write-Host 'Moving ...'
Move-Item -Path C:\go -Destination 'C:\Program Files\Go'
Write-Host 'Removing ...'
Remove-Item go.zip -Force
Write-Host 'Verifying install ("go version") ...'
go version
Write-Host 'Complete.'
