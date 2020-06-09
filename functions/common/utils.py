import constants


def get_bearer():
    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient()
    secret_name = client.secret_version_path(constants.PROJECT_ID, constants.BEARER_SECRET_ID, "1")
    secret_response = client.access_secret_version(secret_name)
    return secret_response.payload.data.decode('UTF-8')
