import pickle
import datetime
import cw_grades

if __name__ == '__main__':
    try:
        file = open("data", "rb")
        pickle_date = pickle.load(file)

        if (datetime.datetime.today() - pickle_date).days >= 1:
            cw_grades.main()
        else:
            pickle_data = pickle.load(file)
            file.close()
            app = cw_grades.QtWidgets.QApplication(cw_grades.sys.argv)
            cw_grades.OpenMainWindow(pickle_data)
            cw_grades.sys.exit(app.exec_())
    except (FileNotFoundError, EOFError):
        from cw_grades import main
        main()

