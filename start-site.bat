@echo off
cd /d %~dp0site
hugo server --buildDrafts --noHTTPCache -p 1313
