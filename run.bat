@echo off

REM Check if lxml is installed
python -c "import lxml" >nul 2>&1
if %errorlevel% neq 0 (
    echo lxml not found. Installing...
    pip install lxml
    echo lxml installed successfully.
)

REM Run the XmlToCsvConvertor.py script
python XmlToCsvConvertor.py %1 %2

