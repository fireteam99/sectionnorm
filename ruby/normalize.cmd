@echo off
pushd "%~dp0"
ruby normalize.rb %*
popd
