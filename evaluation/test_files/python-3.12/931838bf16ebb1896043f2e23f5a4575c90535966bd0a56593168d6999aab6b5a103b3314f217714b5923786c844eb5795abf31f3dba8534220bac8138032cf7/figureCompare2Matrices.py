"""
Created on Fri Jun  5 09:24:51 2020

@author: marcnol
"""
import os
import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import json, csv
from matrixOperations.HIMmatrixOperations import plotDistanceHistograms, plotMatrix
from matrixOperations.HIMmatrixOperations import plotsEnsemble3wayContactMatrix, calculate3wayContactMatrix, getMultiContact
from matrixOperations.HIMmatrixOperations import analysisHiMmatrix, listsSCtoKeep, calculatesEnsemblePWDmatrix

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-F1', '--rootFolder1', help='Folder with dataset 1')
    parser.add_argument('-F2', '--rootFolder2', help='Folder with dataset 2')
    parser.add_argument('-O', '--outputFolder', help='Folder for outputs')
    parser.add_argument('-P', '--parameters', help='Provide name of parameter files. folders2Load.json assumed as default')
    parser.add_argument('-A1', '--label1', help='Add name of label for dataset 1 (e.g. doc)')
    parser.add_argument('-W1', '--action1', help='Select: [all], [labeled] or [unlabeled] cells plotted for dataset 1 ')
    parser.add_argument('-A2', '--label2', help='Add name of label for dataset 1  (e.g. doc)')
    parser.add_argument('-W2', '--action2', help='Select: [all], [labeled] or [unlabeled] cells plotted for dataset 1 ')
    parser.add_argument('--fontsize', help='Size of fonts to be used in matrix')
    parser.add_argument('--axisLabel', help='Use if you want a label in x and y', action='store_true')
    parser.add_argument('--axisTicks', help='Use if you want axes ticks', action='store_true')
    parser.add_argument('--ratio', help='Does ratio between matrices. Default: difference', action='store_true')
    parser.add_argument('--cAxis', help='absolute cAxis value for colormap')
    parser.add_argument('--plottingFileExtension', help='By default: svg. Other options: pdf, png')
    parser.add_argument('--normalize', help='Matrix normalization factor: maximum, none, single value (normalize 2nd matrix by), bin pair e.g. 1,2')
    parser.add_argument('--inputMatrix', help='Source of input matrix: contact (default), PWD, iPWD')
    parser.add_argument('--pixelSize', help='pixelSize in microns')
    runParameters = {}
    args = parser.parse_args()
    if args.rootFolder1:
        rootFolder1 = args.rootFolder1
    else:
        rootFolder1 = '.'
    if args.rootFolder2:
        rootFolder2 = args.rootFolder2
        runParameters['run2Datasets'] = True
    else:
        rootFolder2 = '.'
        runParameters['run2Datasets'] = False
    if args.outputFolder:
        outputFolder = args.outputFolder
    else:
        outputFolder = 'none'
    if args.parameters:
        runParameters['parametersFileName'] = args.parameters
    else:
        runParameters['parametersFileName'] = 'folders2Load.json'
    if args.label1:
        runParameters['label1'] = args.label1
    else:
        runParameters['label1'] = 'doc'
    if args.label2:
        runParameters['label2'] = args.label2
    else:
        runParameters['label2'] = 'NE'
    if args.action1:
        runParameters['action1'] = args.action1
    else:
        runParameters['action1'] = 'labeled'
    if args.action2:
        runParameters['action2'] = args.action2
    else:
        runParameters['action2'] = 'labeled'
    if args.fontsize:
        runParameters['fontsize'] = args.fontsize
    else:
        runParameters['fontsize'] = 12
    if args.pixelSize:
        runParameters['pixelSize'] = args.pixelSize
    else:
        runParameters['pixelSize'] = 0.1
    if args.axisLabel:
        runParameters['axisLabel'] = args.axisLabel
    else:
        runParameters['axisLabel'] = False
    if args.axisTicks:
        runParameters['axisTicks'] = args.axisTicks
    else:
        runParameters['axisTicks'] = False
    if args.ratio:
        runParameters['ratio'] = args.ratio
    else:
        runParameters['ratio'] = False
    if args.cAxis:
        runParameters['cAxis'] = [float(i) for i in args.cAxis.split(',')]
    else:
        runParameters['cAxis'] = 0.6
    if args.plottingFileExtension:
        runParameters['plottingFileExtension'] = '.' + args.plottingFileExtension
    else:
        runParameters['plottingFileExtension'] = '.svg'
    if args.normalize:
        runParameters['normalize'] = args.normalize
    else:
        runParameters['normalize'] = 'none'
    if args.inputMatrix:
        runParameters['inputMatrix'] = args.inputMatrix
    else:
        runParameters['inputMatrix'] = 'contact'
    print('Input Folders:{}, {}'.format(rootFolder1, rootFolder2))
    print('Input parameters:{}'.format(runParameters))
    return (rootFolder1, rootFolder2, outputFolder, runParameters)

def normalizeMatrix(m1, m2, mode):
    print('Normalization: {}'.format(mode))
    if 'maximum' in mode:
        m1_norm = m1.max()
        m2_norm = m2.max()
    elif len(mode.split(',')) > 1:
        N = mode.split(',')
        m1_norm = 1
        m2_norm = m2[int(N[0]), int(N[1])] / m1[int(N[0]), int(N[1])]
    elif 'none' in mode:
        m1_norm = 1
        m2_norm = 1
    else:
        normFactor = float(mode)
        m1_norm = 1
        m2_norm = normFactor
    print('Normalizations: m1= {} | m2={}'.format(m1_norm, m2_norm))
    m1 = m1 / m1_norm
    m2 = m2 / m2_norm
    return (m1, m2)
if __name__ == '__main__':
    rootFolder1, rootFolder2, outputFolder, runParameters = parseArguments()
    HiMdata1 = analysisHiMmatrix(runParameters, rootFolder1)
    HiMdata1.runParameters['action'] = HiMdata1.runParameters['action1']
    HiMdata1.runParameters['label'] = HiMdata1.runParameters['label1']
    HiMdata1.loadData()
    nCells = HiMdata1.nCellsLoaded()
    HiMdata1.retrieveSCmatrix()
    HiMdata2 = analysisHiMmatrix(runParameters, rootFolder2)
    HiMdata2.runParameters['action'] = HiMdata2.runParameters['action2']
    HiMdata2.runParameters['label'] = HiMdata2.runParameters['label2']
    HiMdata2.loadData()
    nCells2 = HiMdata2.nCellsLoaded()
    HiMdata2.retrieveSCmatrix()
    if outputFolder == 'none':
        outputFolder = HiMdata1.dataFolder
    outputFileName1 = outputFolder + os.sep + 'Fig_ratio2HiMmatrices' + '_dataset1:' + HiMdata1.datasetName + '_label1:' + runParameters['label1'] + '_action1:' + runParameters['action1'] + '_dataset2:' + HiMdata2.datasetName + '_label2:' + runParameters['label2'] + '_action2:' + runParameters['action2'] + runParameters['plottingFileExtension']
    outputFileName2 = outputFolder + os.sep + 'Fig_mixedHiMmatrices' + '_dataset1:' + HiMdata1.datasetName + '_label1:' + runParameters['label1'] + '_action1:' + runParameters['action1'] + '_dataset2:' + HiMdata2.datasetName + '_label2:' + runParameters['label2'] + '_action2:' + runParameters['action2']
    if 'contact' in runParameters['inputMatrix']:
        m1 = HiMdata1.data['ensembleContactProbability']
        m2 = HiMdata2.data['ensembleContactProbability']
    elif 'iPWD' in runParameters['inputMatrix']:
        m1 = HiMdata1.SCmatrixSelected
        m2 = HiMdata2.SCmatrixSelected
        cells2Plot1 = listsSCtoKeep(runParameters, HiMdata1.data['SClabeledCollated'])
        cells2Plot2 = listsSCtoKeep(runParameters, HiMdata2.data['SClabeledCollated'])
        dataset1 = list(HiMdata1.ListData.keys())[0]
        dataset2 = list(HiMdata2.ListData.keys())[0]
        m1, _ = calculatesEnsemblePWDmatrix(m1, runParameters['pixelSize'], cells2Plot1, mode=HiMdata1.ListData[dataset1]['PWD_mode'])
        m2, _ = calculatesEnsemblePWDmatrix(m2, runParameters['pixelSize'], cells2Plot2, mode=HiMdata2.ListData[dataset2]['PWD_mode'])
        m1 = np.reciprocal(m1)
        m2 = np.reciprocal(m2)
    elif 'PWD' in runParameters['inputMatrix']:
        m1 = HiMdata1.SCmatrixSelected
        m2 = HiMdata2.SCmatrixSelected
        cells2Plot1 = listsSCtoKeep(runParameters, HiMdata1.data['SClabeledCollated'])
        cells2Plot2 = listsSCtoKeep(runParameters, HiMdata2.data['SClabeledCollated'])
        dataset1 = list(HiMdata1.ListData.keys())[0]
        dataset2 = list(HiMdata2.ListData.keys())[0]
        m1, _ = calculatesEnsemblePWDmatrix(m1, runParameters['pixelSize'], cells2Plot1, mode=HiMdata1.ListData[dataset1]['PWD_mode'])
        m2, _ = calculatesEnsemblePWDmatrix(m2, runParameters['pixelSize'], cells2Plot2, mode=HiMdata2.ListData[dataset2]['PWD_mode'])
    if m1.shape == m2.shape:
        fig1 = plt.figure(constrained_layout=True)
        spec1 = gridspec.GridSpec(ncols=1, nrows=1, figure=fig1)
        f1 = fig1.add_subplot(spec1[0, 0])
        if 'none' in runParameters['normalize']:
            mode = 'maximum'
        else:
            mode = runParameters['normalize']
        _m1, _m2 = (m1.copy(), m2.copy())
        _m1, _m2 = normalizeMatrix(_m1, _m2, mode)
        if runParameters['ratio'] == True:
            matrix = np.log(_m1 / _m2)
            cmtitle = 'log(ratio)'
        else:
            matrix = _m1 - _m2
            cmtitle = 'difference'
        if len(runParameters['cAxis']) == 2:
            cScale = runParameters['cAxis'][1]
        else:
            cScale = runParameters['cAxis'][0]
        print('Clim used: {}\n'.format(cScale))
        f1_ax1_im = HiMdata1.plot2DMatrixSimple(f1, matrix, list(HiMdata1.data['uniqueBarcodes']), runParameters['axisLabel'], runParameters['axisLabel'], cmtitle=cmtitle, cMin=-cScale, cMax=cScale, fontsize=runParameters['fontsize'], colorbar=True, axisTicks=runParameters['axisTicks'], cm='RdBu')
        plt.savefig(outputFileName1)
        print('Output figure: {}'.format(outputFileName1))
        fig2 = plt.figure(constrained_layout=True)
        spec2 = gridspec.GridSpec(ncols=1, nrows=1, figure=fig1)
        f2 = fig2.add_subplot(spec2[0, 0])
        _m1, _m2 = (m1.copy(), m2.copy())
        if 'none' in runParameters['normalize']:
            mode = 'none'
        else:
            mode = runParameters['normalize']
        _m1, _m2 = normalizeMatrix(_m1, _m2, mode)
        matrix2 = _m1
        for i in range(matrix2.shape[0]):
            for j in range(0, i):
                matrix2[i, j] = _m2[i, j]
        HiMdata1.plot2DMatrixSimple(f2, matrix2, list(HiMdata1.data['uniqueBarcodes']), runParameters['axisLabel'], runParameters['axisLabel'], cmtitle='probability', cMin=0, cMax=runParameters['cAxis'][0], fontsize=runParameters['fontsize'], colorbar=True, axisTicks=runParameters['axisTicks'], cm='coolwarm')
        plt.savefig(outputFileName2 + runParameters['plottingFileExtension'])
        np.save(outputFileName2 + '.npy', matrix2)
        print('Output figure: {}'.format(outputFileName2 + runParameters['plottingFileExtension']))
    else:
        print('Error: matrices do not have the same dimensions!')