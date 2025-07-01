class User:
    def __init__(self, uid, name: str = ""):
        self.uid = uid
        self.name: str = name
        self.isReady: bool = False
        self.room_request: str = ""

    def setRoomRequest(self, rq: str):
        self.room_request = rq

    def __repr__(self):
        return "uid: {}, room: {},name: {}\n".format(
            self.uid, self.room_request, self.name
        )
