import pickle
import datetime
import cw_grades
import sys

if __name__ == '__main__':
    try:
        file = open(cw_grades.path("data"), "rb")
        pickle_date = pickle.load(file)

        if (datetime.datetime.today() - pickle_date).days >= 1:
            cw_grades.main()
        else:
            pickle_data = pickle.load(file)
            file.close()
            app = cw_grades.QtWidgets.QApplication(sys.argv)
            cw_grades.open_main_window(pickle_data)
            cw_grades.sys.exit(app.exec_())
    except (FileNotFoundError, EOFError):
        cw_grades.main()
