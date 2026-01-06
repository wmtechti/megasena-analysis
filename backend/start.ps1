# Script para iniciar o backend FastAPI
# Uso: .\start.ps1

Write-Host "Iniciando Backend LoteriaTech..." -ForegroundColor Green

# Garantir que esta na pasta backend
Set-Location $PSScriptRoot

# Verificar se o Docker esta rodando
$dockerRunning = docker ps 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker nao esta rodando. Iniciando containers..." -ForegroundColor Yellow
    docker-compose up -d
    Start-Sleep -Seconds 5
} else {
    # Verificar se o container do PostgreSQL existe
    $postgresContainer = docker ps --filter "name=loteriatech_db" --format "{{.Names}}"
    if (-not $postgresContainer) {
        Write-Host "Container do PostgreSQL nao encontrado. Iniciando containers..." -ForegroundColor Yellow
        docker-compose up -d
        Start-Sleep -Seconds 5
    }
}

# Verificar se o PostgreSQL esta pronto
Write-Host "Aguardando PostgreSQL ficar pronto..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
while ($attempt -lt $maxAttempts) {
    $isReady = docker exec loteriatech_db pg_isready -U postgres 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "PostgreSQL esta pronto!" -ForegroundColor Green
        break
    }
    $attempt++
    Start-Sleep -Seconds 1
}

if ($attempt -eq $maxAttempts) {
    Write-Host "PostgreSQL nao iniciou a tempo. Verifique os logs com 'docker logs loteriatech_db'" -ForegroundColor Red
    exit 1
}

# Iniciar o servidor
Write-Host "Iniciando servidor FastAPI em http://localhost:8005" -ForegroundColor Cyan
Write-Host "Documentacao disponivel em http://localhost:8005/docs" -ForegroundColor Cyan
Write-Host ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8005
