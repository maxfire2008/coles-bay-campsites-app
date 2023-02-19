#!/bin/pwsh
git checkout main
git pull
git add .
git commit -a
docker-compose build --no-cache
docker tag ghcr.io/maxfire2008/coles-bay-campsites-app:latest ghcr.io/maxfire2008/coles-bay-campsites-app:$(git describe --tags --always)
docker tag ghcr.io/maxfire2008/coles-bay-campsites-app:latest ghcr.io/maxfire2008/coles-bay-campsites-app:stable
docker push ghcr.io/maxfire2008/coles-bay-campsites-app --all-tags

# please note that the username was created in a moment of madness and that calling it "god" is dumb
ssh -t god@192.168.86.22 "cd ~/coles-bay-campsites-app && ~/coles-bay-campsites-app/reset.sh"
