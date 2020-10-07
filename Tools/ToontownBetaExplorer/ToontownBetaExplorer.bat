:: =============================================================================
:: Toontown Beta Explorer
:: Author: Joey Ziolkowski
:: Date: 10/7/2020
::
:: Drag and drop any Bam or DNA files from Toontown Online Beta (v1.0.5) onto
:: this batch file for easy viewing.
:: =============================================================================

@echo off
cd /d "%~dp0"

:: If you moved the 1.0.5-install directory or downloaded it separately,
:: update this variable with the correct location on your computer.
set BETA_INSTALL_PATH="..\..\Releases\ToontownBeta\1.0.5-install"

:: Open a new explorer window for each file
for %%x in (%*) do (
    start cmd /c %BETA_INSTALL_PATH%\python.exe -O ToontownBetaExplorer.py %%x ^& pause
)
