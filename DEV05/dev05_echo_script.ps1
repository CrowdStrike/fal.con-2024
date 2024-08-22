try {
  $Json = $args | ConvertFrom-Json
  if (!$Json.echo) { throw "Missing required property 'echo'." }
  @{ result = Write-Output $Json.echo } | ConvertTo-Json -Compress
} catch {
  throw $_
}