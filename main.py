import pickle
import datetime
import mainwindow

if __name__ == '__main__':
    try:
        file = open("data", "rb")
        pickle_date = pickle.load(file)

        if (datetime.datetime.today() - pickle_date).days >= 1:
            mainwindow.main()
        else:
            pickle_data = pickle.load(file)
            file.close()
            app = mainwindow.QtWidgets.QApplication(mainwindow.sys.argv)
            mainwindow.OpenMainWindow(pickle_data)
            mainwindow.sys.exit(app.exec_())
    except (FileNotFoundError, EOFError):
        from mainwindow import main
        main()

