#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


class ClientSecrets:
    '''
    The structure of this class follows Google convention for `client_secrets.json`:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    Bitbucket does not emit this structure so it must be manually constructed.
    '''
    client_id = "9FVKRtLkHUgMQpb8zU"
    client_secret = "RQ3qH3LyvPBtGZPJpyZBfNLNmTCwAjLu"
    redirect_uris = [
      "https://localhost"  # Used for testing.
    ]
    auth_uri = "https://bitbucket.org/site/oauth2/authorize"
    token_uri = "https://bitbucket.org/site/oauth2/access_token"
    server_base_uri = "https://api.bitbucket.org/"


def main():
    c = ClientSecrets()
    # Fetch a request token
    bitbucket = OAuth2Session(c.client_id)
    # Redirect user to Bitbucket for authorization
    authorization_url = bitbucket.authorization_url(c.auth_uri)
    print("Please go here and authorize: {}".format(authorization_url[0]))
    # Get the authorization verifier code from the callback url
    redirect_response = input("Paste the full redirect URL here:")
    # Fetch the access token
    bitbucket.fetch_token(
      c.token_uri,
      authorization_response=redirect_response,
      username=c.client_id,
      password=c.client_secret)
    # Fetch a protected resource, i.e. user profile
    r = bitbucket.get(c.server_base_uri + "1.0/user")
    print(r.content)

def main1():
    client_id = "9FVKRtLkHUgMQpb8zU"
    client_secret = "RQ3qH3LyvPBtGZPJpyZBfNLNmTCwAjLu"
    auth_uri = "https://bitbucket.org/site/oauth2/authorize"
    token_uri = "https://bitbucket.org/site/oauth2/access_token"
    server_base_uri = "https://api.bitbucket.org/"

    company_name='whirlsoftware'
    repo_name='whirl_quality_gate'

    client = BackendApplicationClient(client_id=client_id)
    bitbucket = OAuth2Session(client=client)
    token = bitbucket.fetch_token(token_url='{}'.format(token_uri), client_id=client_id,
        client_secret=client_secret)
    print(token)
    r = bitbucket.get(server_base_uri + "2.0/repositories/{}/{}/pullrequests".format(company_name, repo_name))
    print(r.content)

if __name__ == "__main__":
#    main()
     main1()
