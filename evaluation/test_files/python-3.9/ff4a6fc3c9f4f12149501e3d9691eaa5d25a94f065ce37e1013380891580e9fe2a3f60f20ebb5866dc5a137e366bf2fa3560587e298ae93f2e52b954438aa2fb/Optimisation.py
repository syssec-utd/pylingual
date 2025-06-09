from pathlib import Path
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas, NavigationToolbar2WxAgg as NavigationToolbar
import shutil
import ctypes as ct
from .PostProcessHydrology import PostProcessHydrology
from .Catchment import *
from .Comparison import *
from ..wolf_array import *
from ..PyGui import GenMapManager, HydrologyModel
from . import cst_exchanges as cste
from . import constant as cst
from ..PyTranslate import _

class CaseOpti(GenMapManager):
    launcherDir: str
    launcherParam: Wolf_Param
    refCatchment: Catchment
    idToolItem: int
    mydro: HydrologyModel

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.launcherDir = ''

    def read_param(self, dir, copyDefault=False, callback=None, workingDir=''):
        self.launcherDir = dir
        if not os.path.exists(self.launcherDir):
            try:
                os.mkdir(self.launcherDir)
                shutil.copyfile(workingDir + 'launcher.param.default', os.path.join(self.launcherDir, 'launcher.param'))
                shutil.copyfile(workingDir + 'launcher.param.default', os.path.join(self.launcherDir, 'launcher.param.default'))
            except OSError:
                print('Creation of the directory %s failed' % self.launcherDir)
            else:
                print('Successfully created the directory %s' % self.launcherDir)
        if copyDefault:
            shutil.copyfile(workingDir + 'launcher.param.default', os.path.join(self.launcherDir, 'launcher.param'))
            shutil.copyfile(workingDir + 'launcher.param.default', os.path.join(self.launcherDir, 'launcher.param.default'))
        self.launcherParam = Wolf_Param(to_read=True, filename=os.path.join(self.launcherDir, 'launcher.param'), title='launcher')

    def show_launcherParam(self, event):
        self.launcherParam.Show()
        pass

    def show_mydro(self, event):
        self.mydro.Show()
        pass

class Optimisation(wx.Frame):
    workingDir: str
    myParams: dict
    myParamsPy: dict
    curParams_vec: np.ndarray
    nbParams: int
    optiFactor: ct.c_double
    comparHowParam: Wolf_Param
    saParam: Wolf_Param
    optiParam: Wolf_Param
    dllFortran: ct.CDLL
    pathDll: str
    callBack_proc: dict
    callBack_ptr: dict
    myCases: list

    def __init__(self, parent=None, title='', w=500, h=500):
        super(Optimisation, self).__init__(parent, title=title, size=(w, h))
        self.workingDir = ''
        self.myParams = {}
        self.myParamsPy = {}
        self.nbParams = 0
        self.pathDll = Path(os.path.dirname(__file__)).parent
        self.callBack_proc = {}
        self.callBack_ptr = {}
        self.myCases = []
        self.initGUI()
        self.load_dll(self.pathDll, 'WolfDll.dll')

    def initGUI(self):
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        newClick = fileMenu.Append(wx.ID_ANY, 'New')
        self.Bind(wx.EVT_MENU, self.new, newClick)
        openClick = fileMenu.Append(wx.ID_ANY, 'Open')
        self.Bind(wx.EVT_MENU, self.load, openClick)
        resetClick = fileMenu.Append(wx.ID_ANY, 'Reset')
        self.Bind(wx.EVT_MENU, self.reset, resetClick)
        fileMenu.AppendSeparator()
        quitClick = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Quit\tCtrl+W')
        fileMenu.Append(quitClick)
        quitClick = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Quit\tCtrl+W')
        paramMenu = wx.Menu()
        testOptiClick = paramMenu.Append(wx.ID_ANY, 'test_opti.param')
        self.Bind(wx.EVT_MENU, self.show_optiParam, testOptiClick)
        compareHowClick = paramMenu.Append(wx.ID_ANY, 'compare.how.param')
        self.Bind(wx.EVT_MENU, self.show_comparHowParam, compareHowClick)
        saClick = paramMenu.Append(wx.ID_ANY, 'sa.param')
        self.Bind(wx.EVT_MENU, self.show_saParam, saClick)
        paramMenu.AppendSeparator()
        toolMenu = wx.Menu()
        applyClick = toolMenu.Append(wx.ID_ANY, 'Apply best parameters')
        self.Bind(wx.EVT_MENU, self.apply_optim, applyClick)
        visualiseClick = toolMenu.Append(wx.ID_ANY, 'Visualise best parameters')
        self.Bind(wx.EVT_MENU, self.plot_optim, visualiseClick)
        launchMenu = wx.Menu()
        normalLaunchClick = launchMenu.Append(wx.ID_ANY, '1 Basin')
        self.Bind(wx.EVT_MENU, self.launch_lumped_optimisation, normalLaunchClick)
        SDLaunch = launchMenu.Append(wx.ID_ANY, 'Semi-Distributed')
        self.Bind(wx.EVT_MENU, self.launch_semiDistributed_optimisation, SDLaunch)
        menuBar.Append(fileMenu, 'File')
        menuBar.Append(paramMenu, 'Param files')
        menuBar.Append(toolMenu, 'Tools')
        menuBar.Append(launchMenu, 'Launch')
        self.SetMenuBar(menuBar)
        self.SetSize((1700, 900))
        self.SetTitle('Optimisation')
        self.Centre()
        myExceptions = ['File']
        self.disable_all_MenuBar(exceptions=myExceptions)

    def quitGUI(self, event):
        self.Close()

    def new(self, event):
        launcherDir = 'simul_1'
        idir = wx.DirDialog(None, 'Choose an optimisation directory')
        if idir.ShowModal() == wx.ID_CANCEL:
            print('Optimisation cancelled!')
        self.workingDir = idir.GetPath() + '\\'
        launcherDir = os.path.join(self.workingDir, launcherDir)
        self.default_files(None)
        shutil.copyfile(self.workingDir + 'test_opti.param.default', os.path.join(self.workingDir, 'test_opti.param'))
        shutil.copyfile(self.workingDir + 'sa.param.default', os.path.join(self.workingDir, 'sa.param'))
        shutil.copyfile(self.workingDir + 'compare.how.param.default', os.path.join(self.workingDir, 'compare.how.param'))
        if not os.path.exists(launcherDir):
            try:
                os.mkdir(launcherDir)
            except OSError:
                print('Creation of the directory %s failed' % launcherDir)
            else:
                print('Successfully created the directory %s' % launcherDir)
        shutil.copyfile(self.workingDir + 'launcher.param.default', os.path.join(launcherDir, 'launcher.param'))
        shutil.copyfile(self.workingDir + 'launcher.param.default', os.path.join(launcherDir, 'launcher.param.default'))
        self.optiParam = Wolf_Param(to_read=True, filename=os.path.join(self.workingDir, 'test_opti.param'), title='test_opti', toShow=False)
        newCase = CaseOpti()
        newCase.read_param(launcherDir, copyDefault=True, callback=self.update_parameters_launcher, workingDir=self.workingDir)
        self.myCases.append(newCase)
        self.init_dir_in_params()
        self.comparHowParam = Wolf_Param(to_read=True, filename=os.path.join(self.workingDir, 'compare.how.param'), title='compare.how', toShow=False)
        self.saParam = Wolf_Param(to_read=True, filename=os.path.join(self.workingDir, 'sa.param'), title='sa', toShow=False)
        self.saParam.callback = self.update_parameters_SA
        self.init_with_reference()
        self.init_myParams()
        self.init_with_default_lumped(replace=True)
        try:
            newId = wx.Window.NewControlId()
            iMenu = self.MenuBar.FindMenu('Param files')
            paramMenu = self.MenuBar.Menus[iMenu][0]
            curName = 'Case ' + str(1)
            caseMenu = wx.Menu()
            paramCaseFile = caseMenu.Append(wx.ID_ANY, 'launcher.param')
            self.Bind(wx.EVT_MENU, newCase.show_launcherParam, paramCaseFile)
            guiHydroCase = caseMenu.Append(wx.ID_ANY, 'GUI Hydro')
            newCase.mydro = HydrologyModel(dir=newCase.launcherParam.get_param('Calculs', 'Répertoire simulation de référence'))
            newCase.mydro.Hide()
            self.Bind(wx.EVT_MENU, newCase.show_mydro, guiHydroCase)
            curCase = paramMenu.Append(newId, curName, caseMenu)
        except:
            "ERROR: launch again the app and apply 'load' files."
        self.enable_MenuBar('Param files')
        self.enable_MenuBar('Launch')

    def load(self, event):
        idir = wx.FileDialog(None, 'Choose an optimatimisation file', wildcard='Fichiers param (*.param)|*.param')
        if idir.ShowModal() == wx.ID_CANCEL:
            print('Post process cancelled!')
        fileOpti = idir.GetPath()
        self.workingDir = idir.GetDirectory() + '\\'
        self.optiParam = Wolf_Param(to_read=True, filename=fileOpti, title='test_opti', toShow=False)
        self.workingDir = self.optiParam.get_param('Optimizer', 'dir')
        nbcases = int(self.optiParam.get_param('Cases', 'nb'))
        if nbcases > 1:
            wx.MessageBox(_('So far, there can only have 1 case! This will change soon.'), _('Error'), wx.OK | wx.ICON_ERROR)
            return
        for i in range(nbcases):
            newCase = CaseOpti()
            launcherDir = self.optiParam.get_param('Cases', 'dir_' + str(i + 1))
            newCase.read_param(launcherDir, copyDefault=False, callback=self.update_parameters_launcher)
            newId = wx.Window.NewControlId()
            iMenu = self.MenuBar.FindMenu('Param files')
            paramMenu = self.MenuBar.Menus[iMenu][0]
            curName = 'Case ' + str(i + 1)
            iItem = self.MenuBar.FindMenuItem('Param files', curName)
            if iItem == wx.NOT_FOUND:
                caseMenu = wx.Menu()
                paramCaseFile = caseMenu.Append(wx.ID_ANY, 'launcher.param')
                self.Bind(wx.EVT_MENU, newCase.show_launcherParam, paramCaseFile)
                guiHydroCase = caseMenu.Append(wx.ID_ANY, 'GUI Hydro')
                newCase.mydro = HydrologyModel(dir=newCase.launcherParam.get_param('Calculs', 'Répertoire simulation de référence'))
                newCase.mydro.Hide()
                self.Bind(wx.EVT_MENU, newCase.show_mydro, guiHydroCase)
                curCase = paramMenu.Append(newId, curName, caseMenu)
            else:
                print('WARNING : this scenario was not implemented yet. This might induce an error!')
                curCase = paramMenu.Replace(iItem)
            newCase.idMenuItem = newId
            self.myCases.append(newCase)
        self.comparHowParam = Wolf_Param(to_read=True, filename=os.path.join(self.workingDir, 'compare.how.param'), title='compare.how', toShow=False)
        self.saParam = Wolf_Param(to_read=True, filename=os.path.join(self.workingDir, 'sa.param'), title='sa', toShow=False)
        for i in range(nbcases):
            self.get_reference(idLauncher=i)
            self.init_myParams(idLauncher=i)
        self.checkIntervals()
        self.init_with_default_lumped()
        self.enable_MenuBar('Param files')
        self.enable_MenuBar('Launch')

    def apply_optim(self, event, idLauncher=0):
        bestParams = self.collect_optim()
        refCatch = self.myCases[idLauncher].refCatchment
        myModel = refCatch.myModel
        filePath = os.path.join(refCatch.workingDir, 'Subbasin_' + str(refCatch.myEffSortSubBasins[0]) + '\\')
        myModelDict = cste.modelParamsDict[myModel]['Parameters']
        for i in range(self.nbParams):
            myType = self.myParams[i + 1]['type']
            if int(myType) > 0:
                self.myParams[i + 1]['value'] = bestParams[i]
                fileName = myModelDict[int(myType)]['File']
                myGroup = myModelDict[int(myType)]['Group']
                myKey = myModelDict[int(myType)]['Key']
                if 'Convertion Factor' in myModelDict[int(myType)]:
                    convFact = myModelDict[int(myType)]['Convertion Factor']
                else:
                    convFact = 1.0
                tmpWolf = Wolf_Param(to_read=True, filename=filePath + fileName, toShow=False)
                tmpWolf.myparams[myGroup][myKey]['value'] = bestParams[i] / convFact
                tmpWolf.SavetoFile(None)
                tmpWolf.OnClose(None)
                tmpWolf = None
            else:
                self.curParams_vec[i] = bestParams[i]
                self.update_timeDelay(i + 1)
                refCatch.save_timeDelays([self.myParams[i + 1]['junction_name']])
                print('TO DO : Complete the python parameter dict!!!!!!!')
        self.optiFactor = ct.c_double(bestParams[-1])

    def init_lumped_hydro(self, event):
        self.init_optimizer()

    def init_with_default_lumped(self, replace=False):
        if replace:
            r = wx.ID_NO
        else:
            r = wx.MessageDialog(None, 'Do you want to keep your own parameters files?', 'Warning', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION).ShowModal()
        if r != wx.ID_YES:
            self.optiParam.change_param('Cases', 'nb', 1)
            self.optiParam.change_param('Optimizer', 'tuning_method', 2)
            self.optiParam.change_param('Optimizer', 'max_nb_run', 30000)
            self.optiParam.change_param('Comparison factors', 'nb', 1)
            self.optiParam.change_param('Comparison factors', 'which_factor_1', 1)
            self.comparHowParam.change_param('Comparison global characteristics', 'nb', 1)
            self.comparHowParam.change_param('Comparison 1', 'type', 1)
            self.comparHowParam.change_param('Comparison 1', 'nb factors', 1)
            self.comparHowParam.change_param('Comparison 1', 'nb intervals', 1)
            self.comparHowParam.change_param('Comparison 1', 'factor 1', 1)
            self.saParam.change_param('Optimisation parameters', 'eps', 0.001)
            self.saParam.change_param('Optimisation parameters', 'rt', 0.1)
            self.saParam.change_param('Optimisation parameters', 'ns', 10)
            self.saParam.change_param('Optimisation parameters', 'nt', 10)
            self.saParam.change_param('Optimisation parameters', 'neps', 3)
            self.saParam.change_param('Optimisation parameters', 'Nombre iteration max', 500)
            self.saParam.change_param('Optimisation parameters', 'Initial Temperature', 20)
            self.saParam.callback = self.update_parameters_SA
            self.myCases[0].launcherParam.change_param('Calculs', 'Type de modèle', 4)
            self.myCases[0].launcherParam.change_param('Calculs', 'Nombre de simulations parallèles', 1)
            self.myCases[0].launcherParam.change_param('Récupération des résultats', 'Nombre de bords de convergence', 0)
            self.myCases[0].launcherParam.change_param('Récupération des résultats', 'Nombre de noeuds de convergence', 1)
            self.myCases[0].launcherParam.change_param('Récupération des résultats', 'extract_exchange_zone', 0)
            self.myCases[0].launcherParam.change_param('Récupération des résultats', 'type_of_geom', 2)
            self.myCases[0].launcherParam.change_param('Récupération des résultats', 'type_of_exchange', 15)
            self.myCases[0].launcherParam.change_param('Récupération des résultats', 'type_of_data', 13)
            self.init_lumped_model()
            self.init_myParams()
            self.optiParam.SavetoFile(None)
            self.optiParam.Reload(None)
            self.comparHowParam.SavetoFile(None)
            self.comparHowParam.Reload(None)
            self.saParam.SavetoFile(None)
            self.saParam.Reload(None)
            self.myCases[0].launcherParam.SavetoFile(None)
            self.myCases[0].launcherParam.Reload(None)

    def init_lumped_model(self):
        self.saParam.myparams['Initial parameters']['Read initial parameters?']['value'] = 0
        myModel = self.myCases[0].refCatchment.myModel
        nbParams = cste.modelParamsDict[myModel]['Nb']
        myModelDict = cste.modelParamsDict[myModel]['Parameters']
        prefix1 = 'param_'
        i = 1
        for element in myModelDict:
            paramName = prefix1 + str(i)
            self.myCases[0].launcherParam.myparams[paramName] = {}
            self.myCases[0].launcherParam.myparams[paramName]['type_of_data'] = {}
            self.myCases[0].launcherParam.myparams[paramName]['type_of_data']['value'] = element
            i += 1
        self.myCases[0].launcherParam.myparams['Paramètres à varier']['Nombre de paramètres à varier']['value'] = nbParams
        self.nbParams = nbParams
        prefix2 = 'Parameter '
        for i in range(1, self.nbParams + 1):
            paramName = prefix2 + str(i)
            if not paramName in self.saParam.myparams['Lowest values']:
                self.saParam.myparams['Lowest values'][paramName] = {}
                self.saParam.myparams['Lowest values'][paramName]['value'] = 0.0
            if not paramName in self.saParam.myparams['Highest values']:
                self.saParam.myparams['Highest values'][paramName] = {}
                self.saParam.myparams['Highest values'][paramName]['value'] = 0.0
            if not paramName in self.saParam.myparams['Steps']:
                self.saParam.myparams['Steps'][paramName] = {}
                self.saParam.myparams['Steps'][paramName]['value'] = 0.0
            if not paramName in self.saParam.myparams['Initial parameters']:
                self.saParam.myparams['Initial parameters'][paramName] = {}
                self.saParam.myparams['Initial parameters'][paramName]['value'] = 0.0
            paramName = prefix1 + str(i)
            self.myCases[0].launcherParam.myparams[paramName]['geom_filename'] = {}
            self.myCases[0].launcherParam.myparams[paramName]['geom_filename']['value'] = 'my_geom.txt'
            self.myCases[0].launcherParam.myparams[paramName]['type_of_geom'] = {}
            self.myCases[0].launcherParam.myparams[paramName]['type_of_geom']['value'] = 0
            self.myCases[0].launcherParam.myparams[paramName]['type_of_exchange'] = {}
            self.myCases[0].launcherParam.myparams[paramName]['type_of_exchange']['value'] = -3

    def init_myParams(self, idLauncher=0):
        self.nbParams = int(self.myCases[idLauncher].launcherParam.get_param('Paramètres à varier', 'Nombre de paramètres à varier'))
        for i in range(1, self.nbParams + 1):
            curParam = 'param_' + str(i)
            self.myParams[i] = {}
            self.myParams[i]['type'] = self.myCases[idLauncher].launcherParam.get_param(curParam, 'type_of_data')
            self.myParams[i]['value'] = 0.0
            typeParam = int(self.myParams[i]['type'])
            if typeParam < 0:
                self.myParamsPy[i] = self.myParams[i]
                if type == cste.exchange_parameters_py_timeDelay:
                    self.myParamsPy[i]['update'] = self.myCases[idLauncher].refCatchment.update_timeDelay
                    self.myParamsPy[i]['junction_name'] = self.myCases[idLauncher].launcherParam.get_param(curParam, 'junction_name')

    def collect_optim(self):
        nameTMP = self.optiParam.get_param('Optimizer', 'fname')
        optimFile = os.path.join(self.workingDir, nameTMP + '.rpt')
        try:
            with open(optimFile, newline='') as fileID:
                data_reader = csv.reader(fileID, delimiter=' ', skipinitialspace=True)
                list_data = []
                for raw in data_reader:
                    if len(raw) > 1:
                        if raw[0] + ' ' + raw[1] == 'Best run':
                            list_data.append(raw[3:-1])
            matrixData = np.array(list_data[0]).astype('float')
        except:
            wx.MessageBox(_('The best parameters file is not found!'), _('Error'), wx.OK | wx.ICON_ERROR)
        return matrixData

    def init_with_reference(self, idLauncher=0):
        defaultPath = self.myCases[idLauncher].launcherParam.get_param('Calculs', 'Répertoire simulation de référence')
        if not os.path.exists(defaultPath):
            defaultPath = ''
        idir = wx.FileDialog(None, 'Choose a reference file', wildcard='Fichiers post-processing (*.postPro)|*.postPro', defaultDir=defaultPath)
        if idir.ShowModal() == wx.ID_CANCEL:
            print('Post process cancelled!')
        refFileName = idir.GetPath()
        refDir = idir.GetDirectory() + '\\'
        myPostPro = PostProcessHydrology(postProFile=refFileName)
        self.myCases[idLauncher].refCatchment = myPostPro.myCatchments['Catchment 1']['Object']
        self.myCases[idLauncher].launcherParam.myparams['Calculs']['Répertoire simulation de référence']['value'] = self.myCases[idLauncher].refCatchment.workingDir
        geomName = self.myCases[idLauncher].launcherParam.get_param('Récupération des résultats', 'geom_filename')
        open(self.myCases[idLauncher].launcherDir[idLauncher] + geomName, mode='a').close()
        dateTmp = self.myCases[idLauncher].refCatchment.paramsInput.myparams['Temporal Parameters']['Start date time']['value']
        self.comparHowParam.myparams['Comparison 1']['date begin 1']['value'] = dateTmp
        dateTmp = self.myCases[idLauncher].refCatchment.paramsInput.myparams['Temporal Parameters']['End date time']['value']
        self.comparHowParam.myparams['Comparison 1']['date end 1']['value'] = dateTmp
        self.myCases[idLauncher].launcherParam.SavetoFile(None)
        self.myCases[idLauncher].launcherParam.Reload(None)
        self.comparHowParam.SavetoFile(None)
        self.comparHowParam.Reload(None)

    def get_reference(self, refFile='', idLauncher=0):
        if refFile == '':
            defaultPath = self.myCases[idLauncher].launcherParam.get_param('Calculs', 'Répertoire simulation de référence')
            if not os.path.exists(defaultPath):
                defaultPath = ''
            idir = wx.FileDialog(None, 'Choose a reference file', wildcard='Fichiers post-processing (*.postPro)|*.postPro', defaultDir=defaultPath)
            if idir.ShowModal() == wx.ID_CANCEL:
                print('Post process cancelled!')
            refFileName = idir.GetPath()
        myPostPro = PostProcessHydrology(postProFile=refFileName)
        self.myCases[idLauncher].refCatchment = myPostPro.myCatchments['Catchment 1']['Object']
        self.myCases[idLauncher].launcherParam.myparams['Calculs']['Répertoire simulation de référence']['value'] = self.myCases[idLauncher].refCatchment.workingDir
        geomName = self.myCases[idLauncher].launcherParam.get_param('Récupération des résultats', 'geom_filename')
        open(os.path.join(self.myCases[idLauncher].launcherDir, geomName), mode='a').close()
        self.myCases[idLauncher].launcherParam.SavetoFile(None)
        self.myCases[idLauncher].launcherParam.Reload(None)
        try:
            stationOut = self.optiParam.myparams['Semi-Distributed']['Station measures 1']['value']
            compareFileName = self.optiParam.myparams['Semi-Distributed']['File reference 1']['value']
            shutil.copyfile(compareFileName, os.path.join(self.workingDir, 'compare.txt'))
        except:
            try:
                stationOut = self.comparHowParam.myparams['Comparison 1']['station measures']['value']
            except:
                stationOut = ' '
        self.myCases[idLauncher].refCatchment.define_station_out(stationOut)

    def init_dir_in_params(self):
        self.optiParam.myparams['Optimizer']['dir']['value'] = self.workingDir
        for i in range(len(self.myCases)):
            self.optiParam.myparams['Cases']['dir_' + str(i + 1)]['value'] = os.path.join(self.workingDir, 'simul_' + str(i + 1))
        self.optiParam.myparams['Predefined parameters']['fname']['value'] = self.workingDir + 'param.what'
        self.optiParam.SavetoFile(None)
        self.optiParam.Reload(None)

    def update_dir_in_params(self):
        self.optiParam.myparams['Optimizer']['dir']['value'] = self.workingDir
        for i in range(len(self.myCases)):
            self.optiParam.myparams['Cases']['dir_' + str(i + 1)]['value'] = self.myCases[i].launcherDir
        self.optiParam.myparams['Predefined parameters']['fname']['value'] = self.workingDir + 'param.what'
        self.optiParam.SavetoFile(None)
        self.optiParam.Reload(None)

    def checkIntervals(self):
        print('So far do nothing to check intervals!')

    def update_parameters_launcher(self, idLauncher=0):
        self.myCases[idLauncher].launcherParam.myparams['Paramètres à varier']['Nombre de paramètres à varier']['value'] = self.nbParams

    def update_parameters_SA(self):
        for curGroup in self.saParam.myIncParam:
            for element in self.saParam.myIncParam[curGroup]:
                curParam = self.saParam.myIncParam[curGroup][element]
                if not 'Ref param' in curParam:
                    savedDict = self.saParam.myIncParam[curGroup]['Saved'][curGroup]
                    templateDict = self.saParam.myIncParam[curGroup]['Dict']
                    for i in range(1, self.nbParams + 1):
                        curGroup = curParam.replace('$n$', str(i))
                        if curGroup in self.saParam.myparams:
                            savedDict[curGroup] = {}
                            savedDict[curGroup] = self.saParam.myparams[curGroup]
                        elif curGroup in savedDict:
                            self.saParam.myparams[curGroup] = {}
                            self.saParam.myparams[curGroup] = savedDict[curGroup]
                        else:
                            self.saParam.myparams[curGroup] = {}
                            self.saParam.myparams[curGroup] = templateDict.copy()
        self.saParam.SavetoFile(None)
        self.saParam.Reload(None)

    def plot_optim(self, event, idLauncher=0):
        figure = Figure(figsize=(5, 4), dpi=100)
        self.axes = figure.add_subplot(111)
        self.myCases[idLauncher].refCatchment.plot_allSub(withEvap=False, withCt=False, selection_by_iD=self.myCases[idLauncher].refCatchment.myEffSubBasins, graph_title='My optimal configuration', show=False, writeDir=self.workingDir, figure=figure)
        self.canvas = FigureCanvas(self, -1, figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.TOP | wx.LEFT | wx.EXPAND)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.toolbar.update()
        self.SetSizer(self.sizer)
        self.Fit()

    def load_dll(self, path, fileName):
        libpath = os.path.join(path, 'libs', fileName)
        try:
            self.dllFortran = ct.CDLL(libpath)
        except:
            print('Erreur de chargement de la librairie WolfDLL.dll')

    def default_files(self, event):
        pathPtr = self.workingDir.encode('ansi')
        fileNamePtr = 'test_opti.param'.encode('ansi')
        self.dllFortran.new_optimizer_files_py.restype = ct.c_int
        self.dllFortran.new_optimizer_files_py.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int]
        print('Launch a Fortran procedure')
        id = self.dllFortran.new_optimizer_files_py(pathPtr, fileNamePtr, ct.c_int(len(pathPtr)), ct.c_int(len(fileNamePtr)))
        print('id optimizer = ', id)
        print('End of Fortran procedure')

    def compute_optimizer(self, idOpti=1):
        self.dllFortran.compute_optimizer_py.restype = ct.c_int
        self.dllFortran.compute_optimizer_py.argtypes = [ct.POINTER(ct.c_int)]
        print('Launch a Fortran procedure')
        isOk = self.dllFortran.compute_optimizer_py(ct.byref(ct.c_int(idOpti)))
        print('End of Fortran procedure')
        if isOk != 0:
            print('ERROR: in the Fotran routine in the optimizer computation!')

    def init_optimizer(self, idForced=-1):
        pathPtr = self.workingDir.encode('ansi')
        fileNamePtr = 'test_opti.param'.encode('ansi')
        self.dllFortran.init_optimizer_py.restype = ct.c_int
        self.dllFortran.init_optimizer_py.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int, ct.POINTER(ct.c_int)]
        if idForced < 0:
            opt_id = None
        else:
            opt_id = ct.byref(ct.c_int(idForced))
        print('Launch a Fortran procedure')
        id = self.dllFortran.init_optimizer_py(pathPtr, fileNamePtr, ct.c_int(len(pathPtr)), ct.c_int(len(fileNamePtr)), opt_id)
        print('id optimizer = ', id)
        print('End of Fortran procedure')

    def init_optimizer_again(self, event, idForced=1):
        pathPtr = self.workingDir.encode('ansi')
        fileNamePtr = 'test_opti.param'.encode('ansi')
        self.dllFortran.init_optimizer_py.restype = ct.c_int
        self.dllFortran.init_optimizer_py.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_int, ct.c_int, ct.POINTER(ct.c_int)]
        if idForced < 0:
            opt_id = None
        else:
            opt_id = ct.byref(ct.c_int(idForced))
        print('Launch a Fortran procedure')
        id = self.dllFortran.init_optimizer_py(pathPtr, fileNamePtr, ct.c_int(len(pathPtr)), ct.c_int(len(fileNamePtr)), opt_id)
        print('id optimizer = ', id)
        print('End of Fortran procedure')

    def compute_distributed_hydro_model(self, idLauncher=0):
        self.dllFortran.compute_dist_hydro_model_py.restype = ct.c_int
        self.dllFortran.compute_dist_hydro_model_py.argtypes = [ct.c_char_p, ct.c_int]
        pathPtr = self.myCases[idLauncher].refCatchment.workingDir.encode('ansi')
        print('Compute distributed hydro model ...')
        isOk = self.dllFortran.compute_dist_hydro_model_py(pathPtr, ct.c_int(len(pathPtr)))
        print('End of distributed hydro model.')

    def associate_ptr(self, event, which='all', idOpti=1, idLauncher=0):
        self.dllFortran.associate_ptr_py.restype = ct.c_int
        self.dllFortran.associate_ptr_py.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int, ct.POINTER(ct.c_int), ct.POINTER(ct.c_double)]
        self.dllFortran.get_cptr_py.restype = ct.POINTER(ct.c_double)
        self.dllFortran.get_cptr_py.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int, ct.POINTER(ct.c_int)]
        self.dllFortran.associate_callback_fct.restype = ct.c_int
        self.dllFortran.associate_callback_fct.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int, ct.POINTER(ct.c_int), ct.POINTER(ct.c_double)]
        if which.lower() == 'all':
            self.associate_ptr_params(idOpti, idLauncher)
            self.associate_ptr_opti_factor(idOpti, idLauncher)
            self.associate_ptr_q_all(idOpti, idLauncher)
            self.associate_callback_fct_update(idOpti, idLauncher)
            self.associate_callback_fct_getcvg(idOpti, idLauncher)

    def associate_callback_fct(self):
        print('')

    def associate_callback_fct_update(self, idOpti=1, idLauncher=0):
        self.callBack_proc[cste.fptr_update] = ct.CFUNCTYPE(ct.c_int, ct.c_int)
        update_proc = self.callBack_proc[cste.fptr_update]
        self.callBack_ptr[cste.fptr_update] = update_proc(self.update_hydro)
        update_ptr = self.callBack_ptr[cste.fptr_update]
        self.dllFortran.associate_callback_fct.restype = ct.c_int
        self.dllFortran.associate_callback_fct.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int, ct.POINTER(ct.c_int), update_proc]
        ndims = 1
        dims = np.zeros((ndims,), dtype=ct.c_int, order='F')
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))
        self.dllFortran.associate_callback_fct(ct.byref(ct.c_int(idOpti)), ct.byref(ct.c_int(idLauncher + 1)), ct.c_int(cste.fptr_update), pointerDims, update_ptr)
        print('End of update pointer association!')

    def associate_callback_fct_getcvg(self, idOpti=1, idLauncher=0):
        self.callBack_proc[cste.fptr_get_cvg] = ct.CFUNCTYPE(ct.c_int, ct.POINTER(ct.c_double))
        getcvg_proc = self.callBack_proc[cste.fptr_get_cvg]
        self.callBack_ptr[cste.fptr_get_cvg] = getcvg_proc(self.get_cvg)
        getcvg_ptr = self.callBack_ptr[cste.fptr_get_cvg]
        self.dllFortran.associate_callback_fct.restype = ct.c_int
        self.dllFortran.associate_callback_fct.argtypes = [ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int, ct.POINTER(ct.c_int), getcvg_proc]
        ndims = 1
        dims = np.zeros((ndims,), dtype=ct.c_int, order='F')
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))
        self.dllFortran.associate_callback_fct(ct.byref(ct.c_int(idOpti)), ct.byref(ct.c_int(idLauncher + 1)), ct.c_int(cste.fptr_get_cvg), pointerDims, getcvg_ptr)
        print('End of pointer association!')

    def associate_ptr_q_all(self, idOpti=1, idLauncher=0):
        ndims = 3
        dims = np.zeros((ndims,), dtype=ct.c_int, order='F')
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))
        counter = 1
        for iSub in self.myCases[idLauncher].refCatchment.myEffSortSubBasins:
            mydict = self.myCases[idLauncher].refCatchment.dictIdConversion
            idIP = list(mydict.keys())[list(mydict.values()).index(iSub)]
            curSub = self.myCases[idLauncher].refCatchment.subBasinDict[idIP]
            dims[2] = counter
            dims[0] = len(self.myCases[idLauncher].refCatchment.time)
            curSub.ptr_q_all = None
            curSub.ptr_q_all = self.dllFortran.get_cptr_py(ct.byref(ct.c_int(idOpti)), ct.byref(ct.c_int(idLauncher + 1)), ct.c_int(cste.ptr_q_all), pointerDims)
            curSub.myHydro = None
            curSub.myHydro = self.make_nd_array(curSub.ptr_q_all, shape=(dims[0], dims[1]), dtype=ct.c_double, order='F', own_data=False)
            counter += 1

    def associate_ptr_params(self, idOpti=1, idLauncher=0):
        ndims = 1
        dims = np.empty((ndims,), dtype=ct.c_int, order='F')
        dims[0] = self.nbParams
        self.curParams_vec = np.empty((self.nbParams,), dtype=ct.c_double, order='F')
        pointerParam = self.curParams_vec.ctypes.data_as(ct.POINTER(ct.c_double))
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))
        isOk = self.dllFortran.associate_ptr_py(ct.byref(ct.c_int(idOpti)), ct.byref(ct.c_int(idLauncher + 1)), ct.c_int(cste.ptr_params), pointerDims, pointerParam)
        print('End of param pointer association.')

    def associate_ptr_opti_factor(self, idOpti=1, idLauncher=0):
        ndims = 1
        dims = np.empty((ndims,), dtype=ct.c_int, order='F')
        dims[0] = 1
        self.optiFactor = ct.c_double(0.0)
        pointerDims = dims.ctypes.data_as(ct.POINTER(ct.c_int))
        isOk = self.dllFortran.associate_ptr_py(ct.byref(ct.c_int(idOpti)), ct.byref(ct.c_int(idLauncher + 1)), ct.c_int(cste.ptr_opti_factors), pointerDims, ct.byref(self.optiFactor))
        print('End of factor pointer association.')

    def init_distributed_hydro_model(self, event):
        pathPtr = self.workingDir.encode('ansi')
        fileNamePtr = 'test_opti.param'.encode('ansi')
        self.dllFortran.init_dist_hydro_model_py.restype = ct.c_int
        self.dllFortran.init_dist_hydro_model_py.argtypes = []
        print('Launch a Fortran procedure')
        id = self.dllFortran.init_dist_hydro_model_py()
        print('id distributed_hydro_model = ', id)
        print('End of Fortran procedure')

    def launch_lumped_optimisation(self, event, idOpti=1):
        self.init_optimizer(idOpti)
        self.associate_ptr(None, which='all', idOpti=idOpti)
        self.compute_optimizer(idOpti=idOpti)
        print('Best parameters : ', self.curParams_vec)
        print('Best Factor = ', self.optiFactor)
        self.apply_optim(None)
        self.enable_MenuBar('Tools')

    def test_update_hydro_py(self, event):
        self.dllFortran.test_update_hydro.restype = None
        self.dllFortran.test_update_hydro.argtypes = []
        self.dllFortran.test_update_hydro()

    def launch_semiDistributed_optimisation(self, event, idOpti=1, idLauncher=0):
        if self.optiParam.get_group('Semi-Distributed') != None:
            nbRefs = self.optiParam.get_param('Semi-Distributed', 'nb')
            onlyOwnSub = self.optiParam.get_param('Semi-Distributed', 'Own_SubBasin')
            if onlyOwnSub == None:
                onlyOwnSub = False
            doneList = []
            sortJct = []
            readDict = {}
            for iRef in range(1, nbRefs + 1):
                stationOut = self.optiParam.myparams['Semi-Distributed']['Station measures ' + str(iRef)]['value']
                compareFileName = self.optiParam.myparams['Semi-Distributed']['File reference ' + str(iRef)]['value']
                readDict[stationOut] = compareFileName
            sortJct = self.myCases[idLauncher].refCatchment.sort_level_given_junctions(list(readDict.keys()), changeNames=False)
            for iOpti in range(len(sortJct)):
                stationOut = sortJct[iOpti]
                compareFileName = readDict[stationOut]
                shutil.copyfile(os.path.join(self.workingDir, compareFileName), os.path.join(self.workingDir, 'compare.txt'))
                self.myCases[idLauncher].refCatchment.define_station_out(stationOut)
                self.myCases[idLauncher].refCatchment.activate_usefulSubs(blockJunction=doneList, onlyItself=onlyOwnSub)
                self.optiParam.change_param('Optimizer', 'fname', stationOut)
                self.optiParam.SavetoFile(None)
                self.optiParam.Reload(None)
                self.prepare_calibration_timeDelay(stationOut=stationOut)
                self.init_optimizer(idOpti)
                self.associate_ptr(None, idOpti=idOpti)
                self.compute_optimizer(idOpti)
                self.apply_optim(None)
                self.compute_distributed_hydro_model()
                self.myCases[idLauncher].refCatchment.read_hydro_eff_subBasin()
                doneList.append(stationOut)
        self.enable_MenuBar('Tools')
        print('End of semi-distributed optimisation!')

    def update_hydro(self, idCompar):
        for element in self.myParamsPy:
            junctionName = self.myParamsPy[element]['junction_name']
            timeDelta = self.curParams_vec[element - 1]
            if timeDelta != self.myParamsPy[element]['value']:
                self.myParamsPy[element]['value'] = timeDelta
                isOk = self.myParamsPy[element]['update'](junctionName, value=timeDelta)
        isOk = self.myCases[0].refCatchment.update_hydro(idCompar)
        print('curParam = ', self.curParams_vec)
        print('All timeDelays = ', self.myCases[0].refCatchment.get_all_timeDelay())
        return isOk

    def get_cvg(self, pointerData):
        isOk = self.myCases[0].refCatchment.get_cvg(pointerData)
        return isOk

    def update_timeDelay(self, index):
        isOk = 0.0
        newTimeDelay = self.curParams_vec[index - 1]
        if self.myParamsPy[index]['value'] != newTimeDelay:
            junctionName = self.myParamsPy[index]['junction_name']
            self.myParamsPy[index]['value'] = newTimeDelay
            isOk = self.myParamsPy[index]['update'](junctionName, value=newTimeDelay)
        return isOk

    def prepare_calibration_timeDelay(self, stationOut, idLauncher=0):
        readTxt = int(self.optiParam.get_param('Semi-Distributed', 'Calibrate_times'))
        if readTxt == 1:
            calibrate_timeDelay = True
        else:
            calibrate_timeDelay = False
        myModel = self.myCases[idLauncher].refCatchment.myModel
        nbParamsModel = cste.modelParamsDict[myModel]['Nb']
        if calibrate_timeDelay:
            oldDim = len(self.myParams)
            for i in range(nbParamsModel + 1, oldDim + 1):
                del self.myParams[i]
                del self.myParamsPy[i]
            inletsNames = self.myCases[idLauncher].refCatchment.get_inletsName(stationOut)
            nbInlets = len(inletsNames)
            nbParams = nbParamsModel + nbInlets
            self.nbParams = nbParams
            self.myCases[idLauncher].launcherParam.change_param('Paramètres à varier', 'Nombre de paramètres à varier', nbParams)
            prefix1 = 'param_'
            prefix2 = 'Parameter '
            for i in range(nbInlets):
                paramName = prefix1 + str(nbParamsModel + i + 1)
                self.myCases[idLauncher].launcherParam.myparams[paramName] = {}
                self.myCases[idLauncher].launcherParam.myparams[paramName]['type_of_data'] = {}
                self.myCases[idLauncher].launcherParam.myparams[paramName]['type_of_data']['value'] = cste.exchange_parameters_py_timeDelay
                self.myCases[idLauncher].launcherParam.myparams[paramName]['type_of_data']['type'] = 'Integer'
                self.myCases[idLauncher].launcherParam.myparams[paramName]['geom_filename'] = {}
                self.myCases[idLauncher].launcherParam.myparams[paramName]['geom_filename']['value'] = 'my_geom.txt'
                self.myCases[idLauncher].launcherParam.myparams[paramName]['type_of_geom'] = {}
                self.myCases[idLauncher].launcherParam.myparams[paramName]['type_of_geom']['value'] = 0
                self.myCases[idLauncher].launcherParam.myparams[paramName]['type_of_exchange'] = {}
                self.myCases[idLauncher].launcherParam.myparams[paramName]['type_of_exchange']['value'] = -3
                self.myCases[idLauncher].launcherParam.myparams[paramName]['junction_name'] = {}
                self.myCases[idLauncher].launcherParam.myparams[paramName]['junction_name']['value'] = inletsNames[i]
                self.myParams[nbParamsModel + i + 1] = {}
                self.myParams[nbParamsModel + i + 1]['type'] = self.myCases[idLauncher].launcherParam.get_param(paramName, 'type_of_data')
                self.myParams[nbParamsModel + i + 1]['value'] = 0.0
                self.myParamsPy[nbParamsModel + i + 1] = self.myParams[nbParamsModel + i + 1]
                self.myParamsPy[nbParamsModel + i + 1]['update'] = self.myCases[idLauncher].refCatchment.update_timeDelay
                self.myParamsPy[nbParamsModel + i + 1]['junction_name'] = inletsNames[i]
                paramName = prefix2 + str(nbParamsModel + i + 1)
                self.saParam.change_param('Lowest values', paramName, 0.0)
                self.saParam.change_param('Highest values', paramName, 5.0 * 24.0 * 3600.0)
                self.saParam.change_param('Steps', paramName, self.myCases[idLauncher].refCatchment.deltaT)
                self.saParam.change_param('Initial parameters', paramName, 12.0 * 3600.0)
        else:
            self.nbParams = nbParamsModel
            self.myCases[idLauncher].launcherParam.change_param('Paramètres à varier', 'Nombre de paramètres à varier', self.nbParams)
        self.myCases[idLauncher].launcherParam.SavetoFile(None)
        self.myCases[idLauncher].launcherParam.Reload(None)
        self.saParam.SavetoFile(None)
        self.saParam.Reload(None)

    def reset(self, event):
        print('TO DO !!!!')

    def disable_all_MenuBar(self, exceptions=[]):
        for element in range(len(self.MenuBar.Menus)):
            curMenu = self.MenuBar.Menus[element][0]
            nameMenu = self.MenuBar.Menus[element][1]
            if not nameMenu in exceptions:
                self.MenuBar.EnableTop(element, False)

    def enable_MenuBar(self, menuBar: str):
        idMenu = self.MenuBar.FindMenu(menuBar)
        self.MenuBar.EnableTop(idMenu, enable=True)

    def enable_Menu(self, menuItem: str, menuBar: str, isEnable: bool):
        idItem = self.MenuBar.FindMenuItem(menuBar, menuItem)
        objItem = self.MenuBar.FindItemById(idItem)
        objItem.Enable(isEnable)

    def add_Case(self):
        print('TO DO!!!')

    def launch_optimisation(self, idOpti=1):
        if self.optiParam.get_group('Semi-Distributed') != None:
            self.launch_semiDistributed_optimisation(idOpti=idOpti)
        else:
            self.launch_lumped_optimisation(None, idOpti=idOpti)
            self.apply_optim(None)

    def show_optiParam(self, event):
        self.optiParam.Show()
        pass

    def show_saParam(self, event):
        self.saParam.Show()
        pass

    def show_comparHowParam(self, event):
        self.comparHowParam.Show()
        pass

    def make_nd_array(self, c_pointer, shape, dtype=np.float64, order='C', own_data=True, readonly=False):
        arr_size = np.prod(shape[:]) * np.dtype(dtype).itemsize
        buf_from_mem = ct.pythonapi.PyMemoryView_FromMemory
        buf_from_mem.restype = ct.py_object
        buf_from_mem.argtypes = (ct.c_void_p, ct.c_int, ct.c_int)
        if readonly:
            buffer = buf_from_mem(c_pointer, arr_size, 256)
        else:
            buffer = buf_from_mem(c_pointer, arr_size, 512)
        arr = np.ndarray(tuple(shape[:]), dtype, buffer, order=order)
        if own_data and (not arr.flags.owndata):
            return arr.copy()
        else:
            return arr