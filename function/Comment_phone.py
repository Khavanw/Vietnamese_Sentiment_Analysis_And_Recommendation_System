class CommentPhone:
    def __init__(self,id_phone=None,id_comment=None):
        self._id_phone=id_phone
        self._id_comment=id_comment
    @property
    def getIdPhone(self):
        return self._id_phone
    @property
    def getIdComment(self):
        return self._id_comment
