source ./venv/bin/activate
pelican
cp -r -n ./output/* /usr/local/nginx/html/
