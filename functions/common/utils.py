import constants


def generate_id_from_url(url):
    return url.replace("/", "_").replace(":", "_")


def get_bearer():
    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient()
    secret_name = client.secret_version_path(constants.PROJECT_ID, constants.BEARER_SECRET_ID, "1")
    secret_response = client.access_secret_version(secret_name)
    return secret_response.payload.data.decode('UTF-8')


def inform_boss_about_an_error(error, function_name):
    import telegram
    from google.cloud import secretmanager

    client = secretmanager.SecretManagerServiceClient()
    secret_name = client.secret_version_path(constants.PROJECT_ID, constants.TELEGRAM_TLDR_BOT_SECRET_ID, "1")
    secret_response = client.access_secret_version(secret_name)
    payload = secret_response.payload.data.decode('UTF-8')
    bot = telegram.Bot(payload)
    bot.send_message(chat_id="@tldrtest",
                     text="error: {} in: {}".format(error, function_name))
