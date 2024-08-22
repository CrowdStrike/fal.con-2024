#Requires -Version 5.1
using module @{ModuleName='PSFalcon';ModuleVersion='2.2'}
<#
.SYNOPSIS
Pass a string to Write-Output on a remote host using Real-time Response
.PARAMETER Target
Target hostname
.PARAMETER String
Desired string to send to Write-Output on the target host
.EXAMPLE
.\rtr_direct.ps1 -Target MY-PC -String "Hello World!"
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory,Position=1)]
  [string]$Target,
  [Parameter(Mandatory,Position=2)]
  [string]$String
)
process {
  try {
    if (!$env:FALCON_CLIENT_ID) { throw "Missing 'FALCON_CLIENT_ID' value!" }
    if (!$env:FALCON_CLIENT_SECRET) { throw "Missing 'FALCON_CLIENT_SECRET' value!" }
    Request-FalconToken -ClientId $env:FALCON_CLIENT_ID -ClientSecret $env:FALCON_CLIENT_SECRET
    $DeviceId = Get-FalconHost -Filter "hostname:'$Target'" -Sort 'last_seen.desc' -Limit 1 -Verbose
    if (!$DeviceId) { throw "Failed to retrieve target device_id for '$Target'." }
    $Splat = @{
      Command = 'runscript'
      Argument = "-CloudFile='dev05_rtr_echo_script' -CommandLine='$String'"
      HostId = $DeviceId
      Verbose = $true
    }
    Invoke-FalconRtr @Splat
  } catch {
    throw $_
  }
}