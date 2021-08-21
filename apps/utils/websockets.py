import requests
from django.conf import settings


def broadcast(channel, event, payload):
    """
    Sends WS event via socket.io microservice

    :param channel: Channel to broadcast
    :type channel: str
    :param event: Event name
    :type event: str
    :param payload: something serializable to send
    :return:
    """
    requests.post(settings.WEBSOCKETS_BROADCAST_URL, json={
        'channel': channel,
        'event': event,
        'data': payload,
    })
