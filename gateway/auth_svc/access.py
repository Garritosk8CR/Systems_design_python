import os, requests
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def login(request):
    logging.info("login called from gateway")
    auth = request.authorization

    if not auth:
        return None, ('Missing credentials in gateway', 401)

    basicAuth = (auth.username, auth.password)
    logging.info("Auth svc address: " + os.environ.get('AUTH_SVC_ADDRESS'))
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", 
        auth=basicAuth
    )

    logging.info("response from auth: " + str(response.text))

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)