#!/bin/pwsh
$pwd=(Get-Location).Path

docker run -p 5000:4193 --env-file=.env -it --rm $(docker build -q .)
