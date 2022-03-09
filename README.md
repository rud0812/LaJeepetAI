[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
 [![Npm package version](https://badgen.net/npm/v/express)](https://npmjs.com/package/express)
 
Check our website! [lajeepetai.com](http://lajeepetai.com)

# LaJeepetAI

## How to execute the project in your local machine

In a UNIX based terminal in the root of the project, execute these commands:

### Installation of Node dependencies
```
npm i
```

### Set up and activation of Python Virtual Environment
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt => (if it fails, pip install --upgrade pip)
touch .env
echo "FLASK_APP=server.app:app" > .env
```

### Deploying the web app locally
```
npm run build
npm start
```

If this last command fails, run the following:
```
sudo apt-get install gunicorn
npm start
```

### Accessing the web app
Generally, you will find the web deployed in localhost:8080 in your browser. In any case, the terminal should show you where the web was deployed.


### Redeploying after changes
If you changed your project's code and want to check its behavior after having already done the whole process.

1. In case of **front-end changes**, delete the dist folder inside of `client` and run both `npm run build` and `npm start`.
2. In case of **back-end changes**, run `npm start`
3. In case of **Python requirement changes**, re-generate all the environment related files and folders and run everything except for `npm i`.
4. In case of **VueJS requirement changes**, delete `node_modules` folder and run `npm i` and `npm start`

## Deploying the web online

Access the server 167.71.32.177 through the `ssh` command. Follow this tutorial: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04-es

Remember that you may have to kill some processes under: `ps ax|grep gunicorn`

To deploy a gunicorn service unlinked to nginx server, run: `gunicorn --bind 0.0.0.0:8000 wsgi:app`

