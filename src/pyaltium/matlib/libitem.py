import uuid
from datetime import datetime


class MatLibItem:
    id: uuid.UUID
    type_id: uuid.UUID
    revision_id: uuid.UUID
    revision_date: datetime

    def dump(self):
        raise NotImplementedError
    def load(self):
        raise NotImplementedError

class SolderMask(MatLibItem):
    type_id = uuid.UUID("968469a9-c799-46e2-bc61-c05b2553ab48")
