python ./scripts/merge_pdf.py %1
if %errorlevel% neq 0 (
	pause
	exit /b
)
