@echo off
pushd "%~dp0"
python ./normalization/normalize.py %*
popd
