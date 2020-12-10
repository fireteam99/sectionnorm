@echo off
pushd "%~dp0"
gradlew -q run -PexecArgs="%*" -PrunWorkingDir="%~dp0"
popd
