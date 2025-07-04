@echo off
echo Installing LibFake...
echo ===================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Install the package
echo Installing package in development mode...
pip install -e .

if errorlevel 1 (
    echo Error: Installation failed
    pause
    exit /b 1
)

echo.
echo Testing installation...
python -c "import libfake; print('LibFake imported successfully!')"

if errorlevel 1 (
    echo Error: Import test failed
    pause
    exit /b 1
)

echo.
echo Testing CLI...
libfake --help >nul 2>&1
if errorlevel 1 (
    echo CLI command not found, testing module method...
    python -m libfake --help >nul 2>&1
    if errorlevel 1 (
        echo Error: CLI test failed
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo LibFake installed successfully!
echo ========================================
echo.
echo Try these commands:
echo   libfake --generate
echo   libfake --firstname --count 5
echo   libfake --help
echo.
pause
