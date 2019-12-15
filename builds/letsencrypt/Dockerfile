ARG CERTBOT_RELEASE
FROM certbot/certbot:v${CERTBOT_RELEASE}
ARG ACMESH_RELEASE
RUN echo hello $ACMESH_RELEASE
RUN test $ACMESH_RELEASE

ENV \
  DOMAINS="" \
  RSA_ENABLED=1 \
  ECDSA_ENABLED=1 \
  ECDSA_KEY_LENGTH=ec-256 \
  RSA_KEY_LENGTH=2048 \
  CHALLENGE_MODE=standalone \
  STAGING=1 \
  FORCE_RENEWAL=0 \
  SSL_GROUP_ID=1337 \
  MUST_STAPLE=0 \
  VERBOSE=0 \
  ACMESH_GITHUB_REPO="Neilpang/acme.sh"

# internal variables not intended for override
ENV \
  PATH="${PATH}:/root/.acme.sh" \
  CERT_HOME=/etc/acme \
  LE_CONFIG_HOME=/etc/acme \
  ACMESH_GITHUB_URL=https://raw.githubusercontent.com/$ACMESH_GITHUB_REPO/$ACMESH_RELEASE/acme.sh

# Install acme.sh client
# TODO: improve with git
RUN apk add --update curl openssl socat bash \
  && curl -s $ACMESH_GITHUB_URL | INSTALLONLINE=1 sh \
  && rm -rf /var/cache/apk/*

COPY scripts /le-certgen/scripts
COPY entrypoint.sh /le-certgen/entrypoint.sh

VOLUME /var/ssl
VOLUME /var/acme_challenge_webroot
VOLUME /etc/letsencrypt
VOLUME /etc/acme

EXPOSE 80

ENTRYPOINT ["/le-certgen/entrypoint.sh"]
