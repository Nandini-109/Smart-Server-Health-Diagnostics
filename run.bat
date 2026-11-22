@echo off
echo Starting Smart Server Health Diagnostics API...
python -m uvicorn app.main:app --reload
pause
