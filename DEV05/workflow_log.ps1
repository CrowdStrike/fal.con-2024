#Requires -Version 5.1
using module @{ModuleName='PSFalcon';ModuleVersion='2.2'}
<#
.SYNOPSIS
Pass a string to NGSIEM
.DESCRIPTION
NGSIEM event search: event_type=FusionWorkflowEvent echo=*
.PARAMETER String
Desired string to send to NGSIEM
.EXAMPLE
.\workflow_log.ps1 -String "Hello World!"
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory,Position=1)]
  [string]$String
)
process {
  try {
    if (!$env:FALCON_CLIENT_ID) { throw "Missing 'FALCON_CLIENT_ID' value!" }
    if (!$env:FALCON_CLIENT_SECRET) { throw "Missing 'FALCON_CLIENT_SECRET' value!" }
    Request-FalconToken -ClientId $env:FALCON_CLIENT_ID -ClientSecret $env:FALCON_CLIENT_SECRET
    $Json = @{ echo = $String; direct_log = $true } | ConvertTo-Json -Compress
    if (!$Json) { throw "Failed to create Json for workflow submission." }
    $Execution = Invoke-FalconWorkflow -Name dev05_workflow -Json $Json -Verbose
    if ($Execution) { Write-Host "Started Fusion workflow 'dev05_workflow'. [$Execution]" }
  } catch {
    throw $_
  }
}