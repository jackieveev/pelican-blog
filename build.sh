git pull
source ./venv/bin/activate
rm -rf ./output
pelican
\cp -r ./output/* /usr/local/nginx/html/
