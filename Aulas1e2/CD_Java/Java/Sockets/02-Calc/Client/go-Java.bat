@echo off
echo off

set JAVA_HOME=C:\Users\dfvva\.jdks\ms-21.0.10

rem call mvn exec:java

call mvn exec:java -Dexec.args="localhost 12345"

pause