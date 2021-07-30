import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pandas
import csv

sample_dict = {
    '1': [1, 3, 95, 'A', 'I', "3'", 'NM'], '2': [2, 1, 2, 'B', 'O', "3'", 'M'],
    '3': [3, 3, 4, 'C', 'I', "5'", 'NM'], '4': [19, 99, 95, 'T', 'O', "5'", 'M'],
    '5': [22, 11, 66, 'I', 'I', "5'", 'NM'], '6': [63, 17, 94, 'J', 'I', "5'", 'M'],
    '7': [91, 93, 84, 'D', 'O', "3'", 'NM'], '8': [92, 80, 88, 'K', 'O', "3'", 'M']
}
# for z in range(1, len(sample_list) + 1):
#     sample_dict[str(z)] = sample_list[z - 1]
oligo_dict = {
    "A": "AAAAAAAAAAAAAAA",
    "B": "GGGGGGGGGGGGGGG",
    "C": "CCCCCCCCCCCCCCC",
    "D": "TTTTTTTTTTTTTTT",
    "T": "HIIIIIIIIIIIIII",
    "I": "BYEEEEEEEEEEEEE",
    "J": "AWWWWWWWWWWWWWW",
    "K": "GTCAGTCAGTCAGTC"
}
letter_add = []
staple_display = []
track = []
mod_staple = {}
mod_dict = {"modifier": "strand"}
modified_oligo_dict = {"letter": "modified_strand"}
range_ys = ['']
range_zs = ['']
oligo_ids = ['']
directions = ['']
primes = ['']
mods = ['']
myFont = QFont()
myFont.setBold(True)
clear = True


def plotgraph(instance, x_cords, y_cords, shape, color, mod=0, name=None):
    '''
    this method plots points using pyqtgraph

    inputs:
    x and y coordinates in lists [x], [y]
    shape, ex: "s"
    color, ex (255, 255, 255)
    width, ex 2
    name (applies only to legend)
    '''
    global point
    point = instance.plot(x_cords, y_cords, name=name, pen=None, symbol=shape,
                          symbolPen=pg.mkPen(color=(0, 0, 0), width=mod),
                          symbolBrush=pg.mkBrush(color), symbolSize=20)


def checklist(input_list, user_y='', user_z='', user_oligo='',
              user_direc='', user_prime='', user_mod=''):
    '''
    this method compares the staple data (input_list) to the user filters

    inputs:
    input list, the staple data ex: [91, 93, 84, 'D', 'O', "3'", 'NM']
    y range, ex: 1-2
    z range, ex: 1-2
    oligo Ids, ex: A, B
    direction, ex: U (up)
    prime, ex: 5'
    mod, ex: Y (yes)

    returns true if meets all user filters
    '''
    t1 = False
    t2 = False
    t3 = False
    t4 = False
    t5 = False
    t6 = False
    range_y = user_y.split("-")
    range_z = user_z.split("-")
    multiple_cut = user_oligo.split(",")
    user_oligo_list = [x.replace(" ", "") for x in multiple_cut]

    if user_y == '':
        t1 = True
    else:
        for x in range(int(range_y[0]), int(range_y[1]) + 1):
            if input_list[1] == x:
                t1 = True
                continue
    if user_z == '':
        t2 = True
    else:
        for x in range(int(range_z[0]), int(range_z[1]) + 1):
            if input_list[2] == x:
                t2 = True
                continue
    if user_oligo == '':
        t3 = True
    else:
        for x in user_oligo_list:
            if input_list[3] == x:
                t3 = True
                continue
    if user_direc == '':
        t4 = True
    else:
        if user_direc == "U" or user_direc == "u":
            user_direc = "I"
        elif user_direc == "D" or user_direc == "d":
            user_direc = "O"
        if user_direc == input_list[4]:
            t4 = True
    if user_prime == '':
        t5 = True
    else:
        if input_list[5] == user_prime:
            t5 = True
    if user_mod == '':
        t6 = True
    else:
        if user_mod == "Y" or user_mod == "y":
            user_mod = "M"
        elif user_mod == "N" or user_mod == "n":
            user_mod = "NM"
        if input_list[6] == user_mod:
            t6 = True

    if t1 and t2 and t3 and t4 and t5 and t6:
        return True


def message(title, text, error=False):
    '''
    this method displays a popup messagebox

    inputs:
    title, the message title
    text, the message text
    error, displays error icon
    '''
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    if error:
        msg.setIcon(QMessageBox.Critical)
    msg.exec_()


class GraphWindow(QMainWindow):
    '''
    this class constructs the graph displayed
    '''
    def __init__(self):
        '''
        setup of graph
        graph itself is the self.graphWidget
        '''
        super().__init__()
        global sample_dict, range_ys, range_zs, \
            oligo_ids, directions, primes, mods
        self.texts = []
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.graphWidget.setBackground((255, 255, 255))
        self.graphWidget.setXRange(0, 100)
        self.graphWidget.setYRange(0, 140)
        self.graphWidget.setLabel('left', 'z coords (nm)')
        self.graphWidget.setLabel('bottom', 'y coords (nm)')
        self.graphWidget.showGrid(x=True, y=True)
        self.graph()
        # --------------LEGEND------------------------
        self.legend = self.graphWidget.addLegend()
        plotgraph(self.graphWidget, [-500], [0], 't1', (255, 165, 0, 255), name="3' up")
        plotgraph(self.graphWidget, [-500], [0], 't1', (0, 255, 255, 255), name="3' down")
        plotgraph(self.graphWidget, [-500], [0], 's', (255, 165, 0, 255), name="5' up")
        plotgraph(self.graphWidget, [-500], [0], 's', (0, 255, 255, 255), name="5' down")

    def graph(self):
        '''
        this method given the data, plots the points on the graph
        '''
        global sample_dict, point
        for x, y in sample_dict.items():
            x_coord = y[1]
            y_coord = y[2]
            digit = pg.TextItem(text=str(x), color=(0, 0, 0), anchor=(.5, .5))
            if checklist(y, range_ys[-1], range_zs[-1], oligo_ids[-1],
                         directions[-1], primes[-1], mods[-1]):
                mod = 0
                if y[6] == 'M':
                    mod = 3
                if y[4] == "O" and y[5] == "3'":
                    plotgraph(self.graphWidget, [x_coord], [y_coord], 't1', (0, 255, 255, 255), mod=mod)
                elif y[4] == "O" and y[5] == "5'":
                    plotgraph(self.graphWidget, [x_coord], [y_coord], 's', (0, 255, 255, 255), mod=mod)
                elif y[4] == "I" and y[5] == "5'":
                    plotgraph(self.graphWidget, [x_coord], [y_coord], 's', (255, 165, 0, 255), mod=mod)
                elif y[4] == "I" and y[5] == "3'":
                    plotgraph(self.graphWidget, [x_coord], [y_coord], 't1', (255, 165, 0, 255), mod=mod)
                digit.setPos(y[1], y[2])
                self.graphWidget.addItem(digit)
                self.texts.append(point)
                self.texts.append(digit)

    def update(self):
        '''
        this method wipes the graph and redraws it
        '''
        for x in self.texts:
            self.graphWidget.removeItem(x)
        self.graph()


class MenuWindow(QMainWindow):
    '''
    this class constructs the menu displayed
    '''

    def __init__(self):
        '''
        setup of menu
        mainMenu is the bar on display
        '''
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        Filter = mainMenu.addMenu("View")
        modify = mainMenu.addMenu("Modify")

        saveL = QMenu("Save", self)
        fileMenu.addMenu(saveL)

        loadL = QMenu("Load", self)
        fileMenu.addMenu(loadL)

        emods = QAction("Mods", self)
        emods.triggered.connect(self.editMods)
        modify.addAction(emods)

        estaples = QAction("Staples", self)
        estaples.triggered.connect(self.editStaples)
        modify.addAction(estaples)

        loadMod = QAction("Load modifications", self)
        loadMod.triggered.connect(self.loadModifications)
        loadL.addAction(loadMod)

        loadDict = QAction("Load modified oligo things", self)
        loadDict.triggered.connect(self.loadMDictionary)
        loadL.addAction(loadDict)

        saveMod = QAction("Save modifications", self)
        saveMod.triggered.connect(self.saveModifications)
        saveL.addAction(saveMod)

        saveDict = QAction("Save modified oligo things", self)
        saveDict.triggered.connect(self.saveMDictionary)
        saveL.addAction(saveDict)

        addFilters = QAction("Add filters", self)
        addFilters.triggered.connect(self.add_f)
        Filter.addAction(addFilters)

        removeFilters = QAction("Remove filters", self)
        removeFilters.triggered.connect(self.remove_f)
        Filter.addAction(removeFilters)

        viewLegend = QAction("View legend", self)
        viewLegend.triggered.connect(self.legend)
        Filter.addAction(viewLegend)

    def loadModifications(self):
        '''
        this method loads the modifications
        '''
        global mod_dict, mod_staple
        file = QInputDialog.getText(
            self, "FILE NAME", "Name of file to load:")
        if len(file) != 0:
            try:
                mod_data = pandas.read_csv(f"{file[0]}.csv").to_dict()
                mod_df = pandas.DataFrame(mod_data)
                for (index, row) in mod_df.iterrows():
                    mod_dict[row.modifier] = row.strand
                    mod_staple[row.modifier] = []
            except FileNotFoundError:
                message("Warning", "No records of previously saved files.", error=True)
            except AttributeError:
                message("Warning", "Error loading, try another file.", error=True)
            else:
                message("SUCCESS", "Successfully loaded.")

    def loadMDictionary(self):
        '''
        this method loads the modified oligo dict
        '''
        global modified_oligo_dict
        file = QInputDialog.getText(
            self, "FILE NAME", "Name of file to load:")
        if len(file) > 0:
            try:
                mod_data = pandas.read_csv(f"{file[0]}.csv").to_dict()
                mod_df = pandas.DataFrame(mod_data)
                for (index, row) in mod_df.iterrows():
                    modified_oligo_dict[row.letter] = row.modified_strand
            except FileNotFoundError:
                message("Error", "No records of previously saved files.", error=True)
            except AttributeError:
                message("Error", "Error loading, try another file.", error=True)
            else:
                message("Success", "Successfully loaded.")

    def saveModifications(self):
        '''
        this method loads the modifications
        '''
        global mod_dict
        file = QInputDialog.getText(
            self, "FILE NAME", "Name of file to save:")

        if len(file) > 0:
            with open(f"{file[0]}.csv", "w") as file:
                writer = csv.writer(file)
                for key, value in mod_dict.items():
                    writer.writerow([key, value])

            message("Success", "Successfully saved.")

    def saveMDictionary(self):
        '''
        this method saves modified oligo dict
        note: requires ".txt" or ".csv" specified in input
        '''
        global modified_oligo_dict
        file = QInputDialog.getText(
            self, "FILE NAME", "Name of file to save:")
        if len(file) > 0:
            if ".csv" in file:
                with open(file, "w") as file:
                    writer = csv.writer(file)
                    for key, value in modified_oligo_dict.items():
                        writer.writerow([key, value])
                message("Success", "Successfully saved.")

            elif ".txt" in file:
                with open(file, "w") as file:
                    for key, value in modified_oligo_dict.items():
                        file.write(key + ":" + value)
                        file.write("\n")
                message("Success", "Successfully saved.")

    def add_f(self):
        '''
        this method calls the filter window
        '''
        self.filters = FilterWindow()
        self.filters.show()

    def remove_f(self):
        '''
        this method wipes all filters
        '''
        global range_ys, range_zs, oligo_ids, directions, primes, mods, iii
        if len(range_ys + range_zs + oligo_ids + directions + primes + mods) <= 6:
            message("WARNING", "No current filters.", error=True)
        else:
            range_ys = ['']
            range_zs = ['']
            oligo_ids = ['']
            directions = ['']
            primes = ['']
            mods = ['']
            message("SUCCESS", "Successfully removed.")
        iii.update()

    def legend(self):
        '''
        this method calls the unusable legend
        '''
        self.exe3 = Legend()
        self.exe3.show()

    def editMods(self):
        '''
        this method calls the modifications window
        '''
        self.exe1 = ModifyWindow()
        self.exe1.show()

    def editStaples(self):
        '''
        this method calls the staples window
        '''
        self.exe2 = StapleWindow()
        self.exe2.show()


class FilterWindow(QMainWindow):
    '''
    class that constructs filter window
    '''
    def __init__(self):
        super().__init__()
        '''
        setup of class
        '''
        self.container = QWidget()
        self.setLayout(QVBoxLayout())
        self.main_screen()

    def main_screen(self):
        '''
        setup of window
        '''
        self.container.setLayout(QGridLayout())
        menu_label = QLabel("FILTERS")
        self.y_min = QLineEdit()
        self.z_min = QLineEdit()
        self.y_max = QLineEdit()
        self.z_max = QLineEdit()
        self.oligoids = QLineEdit()
        self.y_min.setPlaceholderText("Y min")
        self.y_max.setPlaceholderText("Y max")
        self.z_min.setPlaceholderText("Z min")
        self.z_max.setPlaceholderText("Z max")
        self.oligoids.setPlaceholderText("Oligo IDs")
        self.up_btn = QPushButton("Up", clicked=lambda: self.up())
        self.down_btn = QPushButton("Down", clicked=lambda: self.down())
        self.prime3_btn = QPushButton("3'", clicked=lambda: self.prime3())
        self.prime5_btn = QPushButton("5'", clicked=lambda: self.prime5())
        self.mod_btn = QPushButton("Modified", clicked=lambda: self.modified())
        self.confirm = QPushButton("Apply", clicked=lambda: self.confirmation())
        self.container.layout().addWidget(menu_label, 0, 0)
        self.container.layout().addWidget(self.y_min, 1, 0)
        self.container.layout().addWidget(self.y_max, 1, 1)
        self.container.layout().addWidget(self.z_min, 2, 0)
        self.container.layout().addWidget(self.z_max, 2, 1)
        self.container.layout().addWidget(self.oligoids, 3, 0)
        self.container.layout().addWidget(self.up_btn, 4, 0)
        self.container.layout().addWidget(self.down_btn, 4, 1)
        self.container.layout().addWidget(self.prime3_btn, 5, 0)
        self.container.layout().addWidget(self.prime5_btn, 5, 1)
        self.container.layout().addWidget(self.mod_btn, 6, 0)
        self.container.layout().addWidget(self.confirm, 6, 1)
        self.layout().addWidget(self.container)
        self.setCentralWidget(self.container)

    def up(self):
        '''
        the method adds filter inside
        '''
        global directions
        self.up_btn.setStyleSheet("background-color : green")
        self.down_btn.setStyleSheet("default")
        directions.append("I")

    def down(self):
        '''
        the method adds filter outside
        '''
        global directions
        self.down_btn.setStyleSheet("background-color : green")
        self.up_btn.setStyleSheet("default")
        directions.append("O")

    def prime3(self):
        '''
        the method adds filter 3'
        '''
        global primes
        self.prime3_btn.setStyleSheet("background-color : green")
        self.prime5_btn.setStyleSheet("default")
        primes.append("3'")

    def prime5(self):
        '''
        the method adds filter 5'
        '''
        global primes
        self.prime5_btn.setStyleSheet("background-color : green")
        self.prime3_btn.setStyleSheet("default")
        primes.append("5'")

    def modified(self):
        '''
        the method adds filter modified
        '''
        global mods
        self.mod_btn.setStyleSheet("background-color: green")
        mods.append("Y")

    def yFilter(self):
        '''
        the method adds filter y range
        requires min/max
        '''
        range_ys.append(f"{self.y_min.text()}-{self.y_max.text()}")

    def zFilter(self):
        '''
        the method adds filter z range
        requires min/max
        '''
        range_zs.append(f"{self.z_min.text()}-{self.z_max.text()}")

    def oligo(self):
        '''
        the method adds filter oligo IDs
        '''
        oligo_ids.append(self.oligoids.text())

    def confirmation(self):
        '''
        the method applies the filters
        graph auto-updates
        '''
        if len(self.y_min.text()+self.y_max.text()) > 1:
            self.yFilter()
        if len(self.z_min.text()+self.z_max.text()) > 1:
            self.zFilter()
        if len(self.oligoids.text()) > 0:
            self.oligo()
        global iii
        iii.update()


class Legend(QMainWindow):
    '''
    this class generates the legend not displayed
    '''

    def __init__(self):
        '''
        legend set up
        '''
        super().__init__()
        self.graphWidget = pg.PlotWidget()
        self.container = QWidget()
        self.setLayout(QVBoxLayout())
        self.container.setLayout(QGridLayout())
        self.vb = pg.ViewBox()
        self.legend = self.graphWidget.addLegend()
        plotgraph(self.graphWidget, [-500], [0], 't1', (255, 165, 0, 255), name="3' up")
        plotgraph(self.graphWidget, [-500], [0], 't1', (0, 255, 255, 255), name="3' down")
        plotgraph(self.graphWidget, [-500], [0], 's', (255, 165, 0, 255), name="5' up")
        plotgraph(self.graphWidget, [-500], [0], 's', (0, 255, 255, 255), name="5' down")
        self.legend.setParent(self.vb)
        self.layout().addWidget(self.container)
        self.setCentralWidget(self.vb)


class ModifyWindow(QMainWindow):
    '''
    class constructs the modify window
    '''
    def __init__(self):
        '''
        sets up window
        '''
        super().__init__()
        self.tracker = []
        self.container = QWidget()
        self.setLayout(QVBoxLayout())
        self.main_screen()
        self.displayUpdate()

    def main_screen(self):
        '''
        display set up
        '''
        self.container.setLayout(QGridLayout())
        e = QLabel("Display:")
        z = QLabel("Entries:")
        e.setFont(myFont)
        z.setFont(myFont)
        self.modname = QLineEdit()
        self.modseq = QLineEdit()
        self.modname.setPlaceholderText("Reference name")
        self.modseq.setPlaceholderText("Sequence (5'->3')")
        modadd = QPushButton("Add", clicked=lambda: self.modAdd())
        moddel = QPushButton("Delete", clicked=lambda: self.modRemove())
        self.container.layout().addWidget(e, 0, 0, 1, 2)
        self.container.layout().addWidget(z, 0, 2, 1, 2)
        self.container.layout().addWidget(self.modname, 1, 2, 1, 2)
        self.container.layout().addWidget(self.modseq, 2, 2, 1, 2)
        self.container.layout().addWidget(modadd, 3, 2)
        self.container.layout().addWidget(moddel, 3, 3)
        self.container.layout().setColumnStretch(0, 1)
        self.container.layout().setColumnStretch(2, 3)
        self.container.resize(640, 480)
        self.layout().addWidget(self.container)
        self.setCentralWidget(self.container)

    def modAdd(self):
        '''
        this method adds modification(s)
        '''
        global mod_dict, mod_staple
        if self.modname.text() in mod_dict:
            message("ERROR", "MOD ALREADY ADDED", error=True)
        elif self.modname.text() == '':
            self.modname.setStyleSheet("border: 1px solid red")
            message("ERROR", "Reference name required.", error=True)
        elif self.modseq.text() == '':
            self.modseq.setStyleSheet("border: 1px solid red")
            message("ERROR", "Sequence required.", error=True)
        else:
            mod_dict[self.modname.text()] = self.modseq.text()
            mod_staple[self.modname.text()] = []
            self.modname.setStyleSheet("default")
            self.modseq.setStyleSheet("default")
        self.displayUpdate()

    def modRemove(self):
        '''
        this method removes modification(s)
        '''
        global mod_dict, sample_dict, staple_display, letter_add, modified_oligo_dict
        if self.modname.text() == "":
            self.modname.setStyleSheet("border: 1px solid red")
            message("ERROR", "Reference name(s) required.", error=True)
        else:
            delete_split = self.modname.text().split(",")
            delete_list = [x.replace(" ", "") for x in delete_split]
            try:
                for modification in delete_list:
                    for staple, info in sample_dict.items():
                        for staples in mod_staple.values():
                            if staple in staples:
                                staple_display.remove(staple)
                                letter_add.remove((sample_dict[staple][3], sample_dict[staple][5]))
                                del modified_oligo_dict[sample_dict[staple][3]]
                                info[6] = "NM"
                    del mod_dict[modification]
                    del mod_staple[modification]
            except KeyError:
                message("Error", "Selection does not exist.", error=True)
            finally:
                self.modname.setStyleSheet("default")
                self.modseq.setStyleSheet("default")
        self.displayUpdate()

    def displayUpdate(self):
        '''
        this method updates the display
        '''
        global mod_dict
        for x in self.tracker:
            self.container.layout().removeWidget(x)
        self.tracker.clear()
        for x, y in mod_dict.items():
            if x != "modifier":
                label = QLabel(f"{x}: {y}")
                self.tracker.append(label)
        for x in range(len(self.tracker)):
            self.container.layout().addWidget(self.tracker[x], x + 1, 0)
        self.modname.clear()
        self.modseq.clear()


class StapleWindow(QMainWindow):
    '''
    class constructs staple window
    '''
    def __init__(self):
        '''
        sets up window
        '''
        super().__init__()
        self.p5V = False
        self.p3V = False
        self.container = QWidget()
        self.setLayout(QVBoxLayout())
        self.mainScreen()
        self.displayUpdate()

    def mainScreen(self):
        '''
        sets up display
        '''
        self.container.setLayout(QGridLayout())
        e = QLabel("Display:")
        z = QLabel("Entries:")
        e.setFont(myFont)
        z.setFont(myFont)
        self.modifications = QLineEdit()
        self.staplenums = QLineEdit()
        self.modifications.setPlaceholderText("Modification")
        self.staplenums.setPlaceholderText("Staples | Ex: (1, 2)/(1-2)")
        self.prime5 = QPushButton("5'", clicked=lambda: self.selected_p5())
        self.prime3 = QPushButton("3'", clicked=lambda: self.p3())
        self.finish = QPushButton("Modify", clicked=lambda: self.modify())
        self.container.layout().addWidget(e, 0, 0)
        self.container.layout().addWidget(z, 0, 2, 1, 2)
        self.container.layout().addWidget(self.modifications, 1, 2, 1, 2)
        self.container.layout().addWidget(self.prime5, 2, 2)
        self.container.layout().addWidget(self.prime3, 2, 3)
        self.container.layout().addWidget(self.staplenums, 3, 2, 1, 2)
        self.container.layout().addWidget(self.finish, 4, 2)
        self.layout().addWidget(self.container)
        self.setCentralWidget(self.container)

    def selected_p5(self):
        '''
        this method sets end to 5'
        '''
        self.p5V = True
        self.prime5.setStyleSheet("background-color : green")
        if self.p3V:
            self.prime3.setStyleSheet("background-color : white")
            self.p3V = False

    def p3(self):
        '''
        this method sets end to 3'
        '''
        self.p3V = True
        self.prime3.setStyleSheet("background-color : green")
        if self.p5V:
            self.prime5.setStyleSheet("background-color : white")
            self.p5V = False

    def modify(self):
        '''
        this method handles if lack of inputs
        '''
        if len(self.modifications.text()) > 0:
            self.modifications.setStyleSheet("default")
            if self.p3V or self.p5V:
                self.prime3.setStyleSheet("default")
                self.prime5.setStyleSheet("default")
                if len(self.staplenums.text()) > 0:
                    self.staplenums.setStyleSheet("default")
                    self.comb()
                    self.displayUpdate()
                    self.modifications.clear()
                    self.staplenums.clear()
                else:
                    self.staplenums.setStyleSheet("border: 1px solid red")
            else:
                self.prime3.setStyleSheet("background-color: red")
                self.prime5.setStyleSheet("background-color: red")
        else:
            self.modifications.setStyleSheet("border: 1px solid red")

    def comb(self):
        '''
        this method adds modificatin to strand
        '''
        global sample_dict, staple_display, letter_add, mod_staple, \
            modified_oligo_dict, oligo_dict
        if "-" in self.staplenums.text():
            range_cut = self.staplenums.text().split("-")
            if len(range_cut) == 1:
                message("Error", "Range selected but only one entry detected.", error=True)
            try:
                for x in range(int(range_cut[0]), int(range_cut[1]) + 1):
                    zb = str(x)
                    staple_in = False
                    if (sample_dict[zb][3], sample_dict[zb][5]) not in letter_add:
                        staple_display.append(zb)
                        letter_add.append((sample_dict[zb][3], sample_dict[zb][5]))
                        mod_staple[self.modifications.text()].append(zb)
                        if self.p3V:
                            modified_oligo_dict[sample_dict[zb][3]] = \
                                oligo_dict[sample_dict[zb][3]] + mod_dict[self.modifications.text()]
                        elif self.p5V:
                            modified_oligo_dict[sample_dict[zb][3]] = \
                                mod_dict[self.modifications.text()] + oligo_dict[sample_dict[zb][3]]
                        sample_dict[zb][6] = "M"
                    else:
                        staple_in = True
                else:
                    if staple_in:
                        message("Error", "Selected staples already modified.", error=True)
            except IndexError:
                message("Error", "Invalid entry.", error=True)
        else:
            list_split = self.staplenums.text().split(",")
            list_of_staples = [x.replace(" ", "") for x in list_split]
            try:
                for x in list_of_staples:
                    staple_in = False
                    if (sample_dict[x][3], sample_dict[x][5]) not in letter_add:
                        staple_display.append(x)
                        letter_add.append((sample_dict[x][3], sample_dict[x][5]))
                        mod_staple[self.modifications.text()].append(x)
                        if self.p3V:
                            modified_oligo_dict[sample_dict[x][3]] = \
                                oligo_dict[sample_dict[x][3]] + mod_dict[self.modifications.text()]
                        elif self.p5V:
                            modified_oligo_dict[sample_dict[x][3]] = \
                                mod_dict[self.modifications.text()] + oligo_dict[sample_dict[x][3]]
                        sample_dict[x][6] = "M"
                    else:
                        staple_in = True
                else:
                    if staple_in:
                        message("ERROR", "Selected staples already modified.", error=True)
            except KeyError:
                message("ERROR", "Invalid entry.", error=True)

    def displayUpdate(self):
        '''
        this method updates the display
        '''
        global modified_oligo_dict, mod_dict, clear, track
        count = 0
        if clear:
            for x in track:
                self.container.layout().removeWidget(x)
            track.clear()
        clear = True
        try:
            for letter, modded_strand in modified_oligo_dict.items():
                if mod_dict[self.modifications.text()] in modded_strand:
                    underline = modded_strand.replace\
                        (mod_dict[self.modifications.text()],
                         ("+" + mod_dict[self.modifications.text()] + "+"))
                    label = QLabel(f"{letter} : {underline}")
                    track.append(label)
        except KeyError:
            if len(self.modifications.text()) > 0:
                message("ERROR", "Invalid entry.", error=True)
        for x in track:
            count += 1
            self.container.layout().addWidget(x, count, 0)

    def closeEvent(self, a0: QCloseEvent) -> None:
        '''
        this method allows display to function on startup
        note: it should not be used by user
        '''
        global clear
        clear = False


class MainWidget(QWidget):
    '''
    constructs the window holding the graph/menu together
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("prototype")
        layout = QVBoxLayout(self)
        layout.addWidget(MenuWindow())
        global iii
        iii = GraphWindow()
        layout.addWidget(iii)


if __name__ == "__main__":
    '''
    program run
    '''
    app = QApplication([])
    widget = MainWidget()
    widget.show()
    app.setStyle(QStyleFactory.create("Fusion"))
    app.exec_()
