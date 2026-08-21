param(
  [Parameter(Mandatory = $true)]
  [string]$Remote,
  [int]$RemotePort = 47921,
  [int]$LocalPort = 47921
)

$ErrorActionPreference = "Stop"

$ssh = Get-Command ssh -ErrorAction SilentlyContinue
if (-not $ssh) { throw "OpenSSH client was not found" }
if (-not $env:AGENT_TOOLKIT_TOKEN) {
  throw "Set AGENT_TOOLKIT_TOKEN before opening a tunnel"
}

$forward = "127.0.0.1:{0}:127.0.0.1:{1}" -f $RemotePort, $LocalPort
Write-Host "Opening reverse tunnel: remote 127.0.0.1:$RemotePort -> local 127.0.0.1:$LocalPort"
Write-Host "The tunnel is not public by itself; expose it only through an authenticated remote proxy."

& $ssh.Source `
  -o ExitOnForwardFailure=yes `
  -o ServerAliveInterval=30 `
  -o ServerAliveCountMax=3 `
  -N `
  -R $forward `
  $Remote
