# Generate certificates for Pushpin

## instructions

```bash

#############
# 1. prepare centos node
sudo yum install -y git
# # compose
sudo -i
VERSION="1.21.0"
curl -L https://github.com/docker/compose/releases/download/$VERSION/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
exit
# OR
# sudo yum install -y python36-pip
# sudo pip-3.6 install docker-compose==1.21.0
docker-compose --version

# use repo
git clone https://github.com/pdonorio/cert-renewal.git
cd cert-renewal
vi .env

#############
# 2. run certificate generation
docker-compose run --rm letsencrypt

#############
# 3. push certificates to s3 bucket
sudo chown -R $UID ./certificates
docker-compose run --rm pusher

#############
# 4. remove images 
docker-compose down --rmi all --remove-orphans

#############
# 5. restart aws pushpin

## inside host with credentials
bash
echo setup \
    && pip3 install --upgrade -r dev-requirements.txt \
    && set -a && source .env && set +a \
    && echo ready
./scripts/restart.py

#############
# THE END

```
