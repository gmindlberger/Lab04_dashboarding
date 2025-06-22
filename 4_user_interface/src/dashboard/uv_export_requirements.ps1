Write-Host "Exporting dependencies to requirements.txt..." -ForegroundColor Cyan
uv export --no-hashes --format requirements-txt > requirements.txt
Write-Host "Export completed successfully." -ForegroundColor Green