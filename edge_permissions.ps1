# PowerShell Script to Configure Microsoft Edge Permissions
# WARNING: Run as Administrator
# This script modifies Windows Registry

Write-Host "`n╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Microsoft Edge - Auto Allow Permissions Configuration       ║" -ForegroundColor White
Write-Host "╚══════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  WARNING: This script should be run as Administrator for registry changes." -ForegroundColor Yellow
    Write-Host "   Some settings may not apply without admin rights.`n" -ForegroundColor Yellow
}

Write-Host "⚠️  SECURITY WARNING:" -ForegroundColor Red
Write-Host "   Allowing all permissions reduces browser security!" -ForegroundColor Yellow
Write-Host "   Only proceed if this is for development/testing purposes.`n" -ForegroundColor Yellow

$confirm = Read-Host "Continue? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "`nOperation cancelled." -ForegroundColor Gray
    exit
}

Write-Host "`n🔧 Configuring Edge Permissions...`n" -ForegroundColor Cyan

# Edge policy registry path
$edgePolicyPath = "HKLM:\SOFTWARE\Policies\Microsoft\Edge"

# Create policy path if it doesn't exist
if (-not (Test-Path $edgePolicyPath)) {
    Write-Host "Creating Edge policy registry path..." -ForegroundColor Gray
    New-Item -Path $edgePolicyPath -Force | Out-Null
}

# Sites to auto-allow
$allowedSites = @(
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://consignment-site-2ac0cae70da0.herokuapp.com",
    "[*.]onrender.com"
)

Write-Host "📍 Configuring permissions for:" -ForegroundColor Cyan
foreach ($site in $allowedSites) {
    Write-Host "   • $site" -ForegroundColor Gray
}
Write-Host ""

# Function to set policy
function Set-EdgePolicy {
    param (
        [string]$PolicyName,
        [object]$PolicyValue,
        [string]$Description
    )
    
    try {
        Write-Host "⚙️  Setting: $Description..." -ForegroundColor Gray
        Set-ItemProperty -Path $edgePolicyPath -Name $PolicyName -Value $PolicyValue -Type DWord -Force
        Write-Host "   ✅ Success" -ForegroundColor Green
    }
    catch {
        Write-Host "   ❌ Failed: $_" -ForegroundColor Red
    }
}

# Apply policies
Write-Host "`n🔧 Applying policies...`n" -ForegroundColor Cyan

# JavaScript
Set-EdgePolicy -PolicyName "DefaultJavaScriptSetting" -PolicyValue 1 -Description "JavaScript (Allow)"

# Images
Set-EdgePolicy -PolicyName "DefaultImagesSetting" -PolicyValue 1 -Description "Images (Allow)"

# Pop-ups
Set-EdgePolicy -PolicyName "DefaultPopupsSetting" -PolicyValue 1 -Description "Pop-ups (Allow)"

# Notifications
Set-EdgePolicy -PolicyName "DefaultNotificationsSetting" -PolicyValue 1 -Description "Notifications (Allow)"

# Geolocation
Set-EdgePolicy -PolicyName "DefaultGeolocationSetting" -PolicyValue 1 -Description "Location (Allow)"

# Sensors
Set-EdgePolicy -PolicyName "DefaultSensorsSetting" -PolicyValue 1 -Description "Motion sensors (Allow)"

# USB Devices
Set-EdgePolicy -PolicyName "DefaultWebUsbGuardSetting" -PolicyValue 1 -Description "USB devices (Allow)"

# MIDI
Set-EdgePolicy -PolicyName "DefaultWebBluetoothGuardSetting" -PolicyValue 1 -Description "MIDI/Bluetooth (Allow)"

# Automatic Downloads
Set-EdgePolicy -PolicyName "DefaultDownloadDirectory" -PolicyValue "" -Description "Automatic downloads (Allow)"

Write-Host "`n✅ Policy configuration complete!" -ForegroundColor Green

Write-Host "`n📋 MANUAL STEPS STILL REQUIRED:" -ForegroundColor Yellow
Write-Host "   Open Microsoft Edge and paste these URLs to configure:" -ForegroundColor Gray
Write-Host ""
Write-Host "   1. Camera: edge://settings/content/camera" -ForegroundColor Cyan
Write-Host "   2. Microphone: edge://settings/content/microphone" -ForegroundColor Cyan
Write-Host "   3. Background Sync: edge://settings/content/backgroundSync" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔄 Restart Microsoft Edge for changes to take effect." -ForegroundColor Yellow

Write-Host "`n💡 TIP: For site-specific permissions:" -ForegroundColor Cyan
Write-Host "   1. Visit: http://localhost:8000" -ForegroundColor Gray
Write-Host "   2. Click 🔒 (lock icon) in address bar" -ForegroundColor Gray
Write-Host "   3. Click 'Permissions for this site'" -ForegroundColor Gray
Write-Host "   4. Set each permission to 'Allow'" -ForegroundColor Gray

Write-Host "`n╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  ✅ Edge permissions configured! Restart browser to apply.      ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Open Edge settings
$openSettings = Read-Host "`nOpen Edge settings now? (yes/no)"
if ($openSettings -eq "yes") {
    Start-Process msedge.exe -ArgumentList "edge://settings/content"
}
