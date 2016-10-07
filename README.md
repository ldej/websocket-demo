virtualenv -ppython3 .env

./env/bin/activate

pip install -r requirements.txt

python ./websocket-server.py

open index.html in one or more browsers/tabs.
