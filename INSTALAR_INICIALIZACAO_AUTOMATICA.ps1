param(
    [string]$TaskName = "Dashboard Servico Medico CGR"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$StartScript = Join-Path $ProjectRoot "INICIAR_REDE_INTERNA.bat"

if (-not (Test-Path $StartScript)) {
    throw "INICIAR_REDE_INTERNA.bat nao encontrado."
}

$UserId = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$Action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c `"$StartScript`"" `
    -WorkingDirectory $ProjectRoot

$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $UserId
$Principal = New-ScheduledTaskPrincipal `
    -UserId $UserId `
    -LogonType Interactive `
    -RunLevel Limited

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Settings $Settings `
    -Description "Inicia o dashboard interno do Servico Medico apos o logon." `
    -Force | Out-Null

Write-Host "Tarefa agendada instalada: $TaskName" -ForegroundColor Green
Write-Host "Ela sera executada no logon desta conta."
Write-Warning "Para funcionar sem usuario conectado, solicite ao TI uma conta de servico e configuracao corporativa."
