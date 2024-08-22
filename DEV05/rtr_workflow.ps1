#Requires -Version 5.1
using module @{ModuleName='PSFalcon';ModuleVersion='2.2'}
<#
.SYNOPSIS
Pass a string to Write-Output on a remote host using a Fusion Workflow
.DESCRIPTION
NGSIEM event search: event_type=FusionWorkflowEvent device_id=* result=*
.PARAMETER Target
Target hostname
.PARAMETER String
Desired string to send to Write-Output on the target host
.EXAMPLE
.\rtr_workflow.ps1 -Target MY-PC -String "Hello World!"
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
    $Json = Get-FalconHost -Filter "hostname:'$Target'" -Sort 'last_seen.desc' -Limit 1 -Detailed -Verbose |
      Select-Object device_id,platform_name,@{l='echo';e={$String}} | ConvertTo-Json -Compress
    if (!$Json) { throw "Failed to create Json for workflow submission." }
    $Execution = Invoke-FalconWorkflow -Name dev05_workflow -Json $Json -Verbose
    if ($Execution) { Write-Host "Started Fusion workflow 'dev05_workflow'. [$Execution]" }
  } catch {
    throw $_
  }
}