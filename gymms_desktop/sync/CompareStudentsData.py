import sync.SQLAutoSync as SQLAutoSync
import Configuration as cfg


class CompareStudentsData:
    def __init__(self, data):
        self.data = data
        self.sql = SQLAutoSync.SQLAutoSync()

    def compareData(self):
        firstInstall = self.sql.getFirstInstallStatus()
        if firstInstall == 0:
            self.case1()
        else:
            self.case2()
        return

    def case1(self):
        if len(self.data) == 0:
            return

        res = self.sql.insertStudents(self.data)
        if res == 0:
            self.sql.updateSoftwareFirstInstallFlag(cfg.CONST_SOFTWARE_FLAG_FIRST_INSTALL_STUDENTS, 1)
        return

    def case2(self):
        localStudentCount = self.sql.getStudentsCount()
        actions = self.sql.getLocalActionStudentModule()
        if len(actions) == 0:
            return

        print(actions)

