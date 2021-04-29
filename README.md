# cs411-demo

## Setting up Environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Setting up GCP
Create a `app.yaml` file in the root folder with the following content:
```yaml
runtime: python38 # or another supported version

instance_class: F1

env_variables:
  MYSQL_USER: <user_name> # please put in your credentials
  MYSQL_PASSWORD: <user_pw> # please put in your credentials
  MYSQL_DB: <database_name> # please put in your credentials
  MYSQL_HOST: <database_ip> # please put in your credentials
```

Setting up the deployment
```bash
curl https://sdk.cloud.google.com | bash # or download cloud sdk directly from the website
gcloud components install app-engine-python
gcloud config set project leafy-chariot-308602 
gcloud auth login #要用学姐邮箱登陆！
gcloud app deploy
```