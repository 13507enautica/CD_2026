@echo off
echo off

rem
rem r = 1 / x, where x the amount of time between frames
rem
rem r = 1     => 1 frame every second
rem r = 0.5   => 1 frame every two (2) seconds
rem r = 0.2   => 1 frame every five (5) seconds
rem r = 0.1   => 1 frame every ten (10) seconds

FOR /F "delims=" %%i IN ('cd') DO SET BaseDirectory=%%i

set Rate=%1%
set FileName=%2%

set OutputDirectory=%BaseDirectory%\static\Thumbs\Sprites\temp

echo Request rate: %Rate%
echo Input file name: %FileName%
echo Output directory: %OutputDirectory%

echo Deleting existing thumb files...

del %OutputDirectory%\*.jpg

%BaseDirectory%\private\ffmpeg.exe -i %FileName% -r %Rate% -s 80*80 -f image2 %OutputDirectory%\thumb-%%03d.jpg

EXIT /B %ERRORLEVEL%
