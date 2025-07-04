@echo off
REM LibFake Version Management Tool for Windows
REM Usage: version.bat [command] [options]

setlocal

if "%1"=="" (
    echo LibFake Version Manager
    echo =====================
    echo.
    echo Usage: version.bat [command] [options]
    echo.
    echo Commands:
    echo   show           Show current version
    echo   set X.Y.Z      Set specific version
    echo   bump major     Bump major version
    echo   bump minor     Bump minor version  
    echo   bump patch     Bump patch version
    echo   check          Check version consistency
    echo.
    echo Examples:
    echo   version.bat show
    echo   version.bat set 1.2.3
    echo   version.bat bump patch
    echo   version.bat check
    echo.
    goto :eof
)

if "%1"=="show" (
    python version_manager.py --show
    goto :eof
)

if "%1"=="set" (
    if "%2"=="" (
        echo Error: Version number required
        echo Usage: version.bat set X.Y.Z
        exit /b 1
    )
    python version_manager.py --set %2
    goto :eof
)

if "%1"=="bump" (
    if "%2"=="" (
        echo Error: Component required ^(major, minor, patch^)
        echo Usage: version.bat bump [major^|minor^|patch]
        exit /b 1
    )
    python version_manager.py --bump %2
    goto :eof
)

if "%1"=="check" (
    python version_manager.py --check
    goto :eof
)

echo Error: Unknown command '%1'
echo Use 'version.bat' without arguments to see help
exit /b 1
