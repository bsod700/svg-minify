@echo off
REM Windows Batch Script to Run SVG Minification
REM Automatically detects Python and runs the minifier

echo.
echo ================================================
echo   SVG Minification Script
echo ================================================
echo.

REM Try to find Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found
    echo.
    python minify_svg.py
    goto :end
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found
    echo.
    py minify_svg.py
    goto :end
)

python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found
    echo.
    python3 minify_svg.py
    goto :end
)

echo [ERROR] Python not found!
echo.
echo Please install Python from: https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:end
echo.
pause

