chcp 65001
cd ..\src
set /p input='BV号:'
echo %input%
python enterPoint.py --download %input%