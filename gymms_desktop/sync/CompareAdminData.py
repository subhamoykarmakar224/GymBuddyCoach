import sync.SQLAutoSync as SQLAutoSync


class CompareAdminData:
    def __init__(self, data):
        self.data = data
        self.sql = SQLAutoSync.SQLAutoSync()

    def compareData(self):
        pass

