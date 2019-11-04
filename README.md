# Note
- https://github.com/nickjj/build-a-saas-app-with-flask/blob/master/docker-compose.yml

- https://mega.nz/#!fu52nACR!J2QytkTQ2Pdb1em9yUDVZnI3LYGz59K5fG-ofYUwHak
- kzPU8mgmyXPzVXiqkTa

# Flask-Angularjs-JSON-Auth
JSON web token authentication with Flask and Angularjs (Satellizer)

Installation

      pip install -r requirements.txt
      vim config.py #Add your database details
      python db.py db init
      python db.py db migrate
      python db.py db upgrade
      vim create_user.py #Add a username password
      python create_user.py
      nohup uwsgi --socket 127.0.0.1:8001 --wsgi-file run.py --callable app --processes 4 --threads 2 --stats   127.0.0.1:9191 &
      vim /etc/nginx/sites-enabled/mysite.conf # Add the below config
          server {
                      listen 80;
                       server_name localhost;

                       location = /favicon.ico { access_log off; log_not_found off; }
                       location / {
                           root /path/to/Flask-Angularjs-JSON-Auth/angularjs-frontend/;
                            }

                      location /api {
       
                        uwsgi_pass 127.0.0.1:8001;
                        include uwsgi_params;
                     }
    }
    
    service nginx start  


For explanation see http://techarena51.com/index.php/json-web-token-authentication-with-flask-and-angularjs/

# Asset
- IBM maximo demo: https://www.ibm.com/support/pages/maximo-asset-management-760-preview-site
- Qualys: https://qualysguard.qg3.apps.qualys.com/
