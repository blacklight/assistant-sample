from assistant import Assistant
from assistant.hotword import HotwordService

assistant = Assistant()
service = HotwordService(model='/path/to/your/model/file', assistant=assistant)
service.start()
service.join()
