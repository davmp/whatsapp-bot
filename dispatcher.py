from messages import Replies
class ResponseType:
        GRAPE = 1
        TROLL = 2
        STRAW = 3

class MessageHandler:
    def __init__(self, lang='br') -> None:
          self.lang = lang

    def format_response(self, response):
        text, media = response
        print(text, media)
        r = {'body': text, 'media': media}
        return r

    def handle(self, message):
        if message == "ola":
            return self.format_response(Replies.SAUDATION)
        elif message == "grape":
            return self.format_response(Replies.GRAPE)
        elif message == "troll":
            return self.format_response(Replies.TROLL)
        elif message == "straw":
            return self.format_response(Replies.STRAW)
        else:
            return self.format_response(Replies.REQUIRES_IDENTITY)