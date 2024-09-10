#Requires -Version 5.1
using module @{ModuleName='PSFalcon';ModuleVersion='2.2'}
<#
.SYNOPSIS
Perform a pre-defined Event Search for a target device using a Fusion workflow
.PARAMETER Target
Target hostname
.EXAMPLE
.\workflow_search.ps1 -Target MY-PC
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory,Position=1)]
  [string]$Target
)
process {
  try {
    if (!$env:FALCON_CLIENT_ID) { throw "Missing 'FALCON_CLIENT_ID' value!" }
    if (!$env:FALCON_CLIENT_SECRET) { throw "Missing 'FALCON_CLIENT_SECRET' value!" }
    Request-FalconToken -ClientId $env:FALCON_CLIENT_ID -ClientSecret $env:FALCON_CLIENT_SECRET
    $Json = Get-FalconHost -Filter "hostname:'$Target'" -Sort 'last_seen.desc' -Limit 1 -Verbose |
      Select-Object @{l='device_id';e={$_}},@{l='search';e={$true}} | ConvertTo-Json -Compress
    if (!$Json) { throw "Failed to create Json for workflow submission." }
    $Id = Invoke-FalconWorkflow -Name dev05_workflow -Json $Json -Verbose
    if ($Id) {
      Write-Host "Started Fusion workflow 'dev05_workflow'. [$Id]"
      Write-Host "Waiting for results..."
    }
    do {
      if ($Execution) { Write-Host "Trying again..." }
      Start-Sleep -Seconds 10
      $Execution = Get-FalconWorkflow -Id $Id -Execution -Verbose
    } until ($Execution.status -eq 'Completed' -and $Execution.activities.status -contains 'Completed')
    $Output = $Execution.activities.Where({$_.status -eq 'Completed'}).result.results
    if (!$Output) { Write-Host "Workflow completed but 'AssociateIndicator' search produced no results." }
    $Output
  } catch {
    throw $_
  }
}