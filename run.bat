@echo off

echo =============================================
echo Projet final de synthèse . Pipeline géospatial complet
echo =============================================

set PYTHONIOENCODING=utf-8

REM Chemin vers le python du env
set PYTHON_EXE=geo\Scripts\python.exe

REM Lancer le script principal main

"%PYTHON_EXE%" scripts\main.py


echo.
echo ======================================================
echo Exécution du Pipeline terminé