git pull
source ./venv/bin/activate
rm -rf ./output
pelican
rm -rf /usr/local/nginx/html/*
cp -r -n ./output/* /usr/local/nginx/html/
