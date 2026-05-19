# Railway Deployment Script
# Run this in PowerShell from your project directory

Write-Host "`n🚂 Railway Deployment Starting...`n" -ForegroundColor Cyan

# Step 1: Login
Write-Host "STEP 1: Logging into Railway..." -ForegroundColor Yellow
railway login
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Login failed. Please try again." -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Logged in successfully!`n" -ForegroundColor Green

# Step 2: Initialize project
Write-Host "STEP 2: Initializing Railway project..." -ForegroundColor Yellow
railway init
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Init failed. Please try again." -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Project initialized!`n" -ForegroundColor Green

# Step 3: Set environment variables
Write-Host "STEP 3: Setting environment variables..." -ForegroundColor Yellow
Write-Host "(You'll need to update DATABASE_URL with your Neon DB connection string)`n" -ForegroundColor Gray

# Prompt for Neon DB URL
$neonUrl = Read-Host "Enter your Neon PostgreSQL connection string"

if ([string]::IsNullOrWhiteSpace($neonUrl)) {
    Write-Host "⚠️  No DATABASE_URL provided. You'll need to set it manually." -ForegroundColor Yellow
} else {
    railway variables set DATABASE_URL="$neonUrl"
}

# Set other variables
railway variables set SECRET_KEY="django-insecure-x7k9m2p4q8r1s5t3u6v0w9y2z4a7b1c3d5e8f0g2h4j6"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="*.railway.app"
railway variables set PYTHONUNBUFFERED="1"

Write-Host "`n✅ Environment variables set!`n" -ForegroundColor Green

# Step 4: Deploy
Write-Host "STEP 4: Deploying to Railway..." -ForegroundColor Yellow
railway up

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed. Check logs with: railway logs" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Deployment complete!`n" -ForegroundColor Green

# Step 5: Show status and URL
Write-Host "STEP 5: Checking deployment status..." -ForegroundColor Yellow
railway status

Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "`n🎉 Deployment Complete!`n" -ForegroundColor Green
Write-Host "Your app is now live!" -ForegroundColor Cyan
Write-Host "`nRun 'railway open' to view your site in browser.`n" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

# Optional: Open in browser
$openBrowser = Read-Host "`nOpen site in browser now? (Y/n)"
if ($openBrowser -ne "n" -and $openBrowser -ne "N") {
    railway open
}
