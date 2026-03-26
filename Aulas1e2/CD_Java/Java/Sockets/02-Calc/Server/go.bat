@echo off
echo off

set JAVA_HOME=C:\Users\dfvva\.jdks\ms-21.0.10

call mvn exec:java

rem call mvn exec:java -Dexec.args="12346"

pause