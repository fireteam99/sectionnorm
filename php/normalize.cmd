@echo off
pushd "%~dp0"
php normalize.php %*
popd
