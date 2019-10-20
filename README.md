# assistant-sample
Wrapper around Google's pushtotalk.py for assistant interaction without the google-assistant-library

After [Google's sudden deprecation](https://developers.google.com/assistant/sdk/reference/library/python) of the assistant library
users have been left with nearly no choice for interacting with the assistant. The [gRPC interface](https://developers.google.com/assistant/sdk/guides/service/python/)
is embarassingly undocumented and making it work means hammering the extremely hackish and poorly designed [`pushtotalk.py` example](https://github.com/googlesamples/assistant-sdk-python/blob/master/google-assistant-sdk/googlesamples/assistant/grpc/pushtotalk.py).

I have made a lot of dirty work myself and created this repository to provide users with an easy way to get their assistant to
work even without the assistant library. To get it to work:

* Install the Google Assistant SDK and oauthlib:

```bash
pip install 'google-assistant-sdk[samples]' 'google-auth-oauthlib[tool]'
```

* Generate a credentials file:

```bash
google-oauthlib-tool --scope https://www.googleapis.com/auth/assistant-sdk-prototype \
          --save --headless --client-secrets /path/to/client_secret_client-id.json
```

* Clone this repository and run `assistant_sample.py` to test the assistant:

```python
import sys

from assistant import Assistant

assistant = Assistant()

while True:
    print('Press ENTER to start a conversation, Ctrl+C to terminate')

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        print('\nExiting the assistant')
        break

    interactions = assistant.start_conversation()
    print(interactions)
    assistant.stop_conversation()
```

* The gRPC implementation doesn't support hotword detection (no more "OK Google" support). You can however use [Snowboy](https://snowboy.kitt.ai)
as a workaround. Download or train your voice model on the Snowboy website, get the model file and install the Python bindings:

```bash
pip install snowboy
```

* Run the code in `hotword_sample.py` for hotword+assistant support:

```python
from assistant import Assistant
from assistant.hotword import HotwordService

assistant = Assistant()
service = HotwordService(model='/path/to/your/model/file', assistant=assistant)
service.start()
service.join()
```
