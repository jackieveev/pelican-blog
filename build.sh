git pull
source ./venv/bin/activate
rm -rf ./output
pelican
/bin/cp -r ./output/* /usr/local/nginx/html/
