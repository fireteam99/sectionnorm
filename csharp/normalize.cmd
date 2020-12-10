@echo off
pushd "%~dp0"
dotnet run -- %*
popd
