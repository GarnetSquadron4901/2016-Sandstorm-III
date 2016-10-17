echo off
setlocal
C:
call :GotoFolder C:\WA\GarnetSquadron
call :UpdateSvnRepo https://github.com/GarnetSquadron4901/ 2016-Sandstorm-III.git
call :UpdateSvnRepo https://github.com/GarnetSquadron4901/ GarnetSquadronThings.git
call :UpdateSvnRepo https://github.com/GarnetSquadron4901/ Operator-Interface-Control-Board.git
call :UpdateSvnRepo https://github.com/juchong/ ADIS16448-RoboRIO-Driver.git
pause
endlocal
goto done

:GotoFolder
    IF NOT EXIST %~1 (
        echo Creating: %~1
        mkdir %~1
    )
    echo Changing directory to: %~1
    cd %~1
    goto :eof

:UpdateSvnRepo
    IF NOT EXIST .\%~2 (
        echo on
        svn co %~1%~2
        echo off
    ) ELSE (
        echo on
        svn up .\%~2
        echo off
    )
    goto :eof

:done

