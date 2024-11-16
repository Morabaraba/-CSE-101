@echo off 

if exist F:\ (
        del F:\*.py
        copy *.py F:\
        echo Copied to drive
) else (
        echo Drive not reacheable
)

