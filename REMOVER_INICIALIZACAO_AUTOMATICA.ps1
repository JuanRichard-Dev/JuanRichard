param(
    [string]$TaskName = "Dashboard Servico Medico CGR"
)

$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($null -eq $task) {
    Write-Host "A tarefa nao existe: $TaskName"
    exit 0
}

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "Tarefa removida: $TaskName" -ForegroundColor Green
