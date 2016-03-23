setlocal
C:
call :GotoFolder C:\WA
call :GotoFolder C:\WA\GarnetSquadron
call :UpdateSvnRepo https://github.com/GarnetSquardon4901/ 2016-Sand-Storm-III.git
call :UpdateSvnRepo https://github.com/GarnetSquardon4901/ GarnetSquadronThings.git
call :UpdateSvnRepo https://github.com/GarnetSquardon4901/ Operator-Interface-Control-Board.git
call :UpdateSvnRepo https://github.com/juchong/ ADIS16448-RoboRIO-Driver.git
pause
endlocal
goto done

:GotoFolder
    echo Going to folder %~1
    IF NOT EXIST %~1 (
        mkdir %~1
    )
    cd %~1
    goto :eof

:UpdateSvnRepo
    IF NOT EXIST .\%~2 (
        echo Checking out %~1%~2
        svn co %~1%~2
    ) ELSE (
        echo Updating %~2
        svn up .\%~2
    )
    goto :eof

:done

