from collections import namedtuple
import pyxlpr.data.icdar.rrc_evaluation_funcs_1_1 as rrc_evaluation_funcs
import importlib

def evaluation_imports():
    """
    evaluation_imports: Dictionary ( key = module name , value = alias  )  with python modules used in the evaluation. 
    """
    return {'math': 'math', 'numpy': 'np'}

def default_evaluation_params():
    """
    default_evaluation_params: Default parameters to use for the validation and evaluation.
    """
    return {'AREA_RECALL_CONSTRAINT': 0.8, 'AREA_PRECISION_CONSTRAINT': 0.4, 'EV_PARAM_IND_CENTER_DIFF_THR': 1, 'MTYPE_OO_O': 1.0, 'MTYPE_OM_O': 0.8, 'MTYPE_OM_M': 1.0, 'GT_SAMPLE_NAME_2_ID': 'gt_img_([0-9]+).txt', 'DET_SAMPLE_NAME_2_ID': 'res_img_([0-9]+).txt', 'CRLF': False}

def validate_data(gtFilePath, submFilePath, evaluationParams):
    """
    Method validate_data: validates that all files in the results folder are correct (have the correct name contents).
                            Validates also that there are no missing files in the folder.
                            If some error detected, the method raises the error
    """
    gt = rrc_evaluation_funcs.load_zip_file(gtFilePath, evaluationParams['GT_SAMPLE_NAME_2_ID'])
    subm = rrc_evaluation_funcs.load_zip_file(submFilePath, evaluationParams['DET_SAMPLE_NAME_2_ID'], True)
    for k in gt:
        rrc_evaluation_funcs.validate_lines_in_file(k, gt[k], evaluationParams['CRLF'], True, True)
    for k in subm:
        if (k in gt) == False:
            raise Exception('The sample %s not present in GT' % k)
        rrc_evaluation_funcs.validate_lines_in_file(k, subm[k], evaluationParams['CRLF'], True, False)

def evaluate_method(gtFilePath, submFilePath, evaluationParams):
    """
    Method evaluate_method: evaluate method and returns the results
        Results. Dictionary with the following values:
        - method (required)  Global method metrics. Ex: { 'Precision':0.8,'Recall':0.9 }
        - samples (optional) Per sample metrics. Ex: {'sample1' : { 'Precision':0.8,'Recall':0.9 } , 'sample2' : { 'Precision':0.8,'Recall':0.9 }
    """
    for module, alias in evaluation_imports().items():
        globals()[alias] = importlib.import_module(module)

    def one_to_one_match(row, col):
        cont = 0
        for j in range(len(recallMat[0])):
            if recallMat[row, j] >= evaluationParams['AREA_RECALL_CONSTRAINT'] and precisionMat[row, j] >= evaluationParams['AREA_PRECISION_CONSTRAINT']:
                cont = cont + 1
        if cont != 1:
            return False
        cont = 0
        for i in range(len(recallMat)):
            if recallMat[i, col] >= evaluationParams['AREA_RECALL_CONSTRAINT'] and precisionMat[i, col] >= evaluationParams['AREA_PRECISION_CONSTRAINT']:
                cont = cont + 1
        if cont != 1:
            return False
        if recallMat[row, col] >= evaluationParams['AREA_RECALL_CONSTRAINT'] and precisionMat[row, col] >= evaluationParams['AREA_PRECISION_CONSTRAINT']:
            return True
        return False

    def num_overlaps_gt(gtNum):
        cont = 0
        for detNum in range(len(detRects)):
            if detNum not in detDontCareRectsNum:
                if recallMat[gtNum, detNum] > 0:
                    cont = cont + 1
        return cont

    def num_overlaps_det(detNum):
        cont = 0
        for gtNum in range(len(recallMat)):
            if gtNum not in gtDontCareRectsNum:
                if recallMat[gtNum, detNum] > 0:
                    cont = cont + 1
        return cont

    def is_single_overlap(row, col):
        if num_overlaps_gt(row) == 1 and num_overlaps_det(col) == 1:
            return True
        else:
            return False

    def one_to_many_match(gtNum):
        many_sum = 0
        detRects = []
        for detNum in range(len(recallMat[0])):
            if gtRectMat[gtNum] == 0 and detRectMat[detNum] == 0 and (detNum not in detDontCareRectsNum):
                if precisionMat[gtNum, detNum] >= evaluationParams['AREA_PRECISION_CONSTRAINT']:
                    many_sum += recallMat[gtNum, detNum]
                    detRects.append(detNum)
        if round(many_sum, 4) >= evaluationParams['AREA_RECALL_CONSTRAINT']:
            return (True, detRects)
        else:
            return (False, [])

    def many_to_one_match(detNum):
        many_sum = 0
        gtRects = []
        for gtNum in range(len(recallMat)):
            if gtRectMat[gtNum] == 0 and detRectMat[detNum] == 0 and (gtNum not in gtDontCareRectsNum):
                if recallMat[gtNum, detNum] >= evaluationParams['AREA_RECALL_CONSTRAINT']:
                    many_sum += precisionMat[gtNum, detNum]
                    gtRects.append(gtNum)
        if round(many_sum, 4) >= evaluationParams['AREA_PRECISION_CONSTRAINT']:
            return (True, gtRects)
        else:
            return (False, [])

    def area(a, b):
        dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin) + 1
        dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin) + 1
        if dx >= 0 and dy >= 0:
            return dx * dy
        else:
            return 0.0

    def center(r):
        x = float(r.xmin) + float(r.xmax - r.xmin + 1) / 2.0
        y = float(r.ymin) + float(r.ymax - r.ymin + 1) / 2.0
        return Point(x, y)

    def point_distance(r1, r2):
        distx = math.fabs(r1.x - r2.x)
        disty = math.fabs(r1.y - r2.y)
        return math.sqrt(distx * distx + disty * disty)

    def center_distance(r1, r2):
        return point_distance(center(r1), center(r2))

    def diag(r):
        w = r.xmax - r.xmin + 1
        h = r.ymax - r.ymin + 1
        return math.sqrt(h * h + w * w)

    def rectangle_to_points(rect):
        points = [int(rect.xmin), int(rect.ymax), int(rect.xmax), int(rect.ymax), int(rect.xmax), int(rect.ymin), int(rect.xmin), int(rect.ymin)]
        return points
    perSampleMetrics = {}
    methodRecallSum = 0
    methodPrecisionSum = 0
    Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
    Point = namedtuple('Point', 'x y')
    if isinstance(gtFilePath, str):
        gt = rrc_evaluation_funcs.load_zip_file(gtFilePath, evaluationParams['GT_SAMPLE_NAME_2_ID'])
    else:
        gt = gtFilePath
    if isinstance(submFilePath, str):
        subm = rrc_evaluation_funcs.load_zip_file(submFilePath, evaluationParams['DET_SAMPLE_NAME_2_ID'], True)
    else:
        subm = submFilePath
    numGt = 0
    numDet = 0
    for resFile in gt:
        if isinstance(gt[resFile], bytes):
            gtFile = rrc_evaluation_funcs.decode_utf8(gt[resFile])
        else:
            gtFile = gt[resFile]
        recall = 0
        precision = 0
        hmean = 0
        recallAccum = 0.0
        precisionAccum = 0.0
        gtRects = []
        detRects = []
        gtPolPoints = []
        detPolPoints = []
        gtDontCareRectsNum = []
        detDontCareRectsNum = []
        pairs = []
        evaluationLog = ''
        recallMat = np.empty([1, 1])
        precisionMat = np.empty([1, 1])
        pointsList, _, transcriptionsList = rrc_evaluation_funcs.get_tl_line_values_from_file_contents(gtFile, evaluationParams['CRLF'], True, True, False)
        for n in range(len(pointsList)):
            points = pointsList[n]
            transcription = transcriptionsList[n]
            dontCare = transcription == '###'
            gtRect = Rectangle(*points)
            gtRects.append(gtRect)
            gtPolPoints.append(points)
            if dontCare:
                gtDontCareRectsNum.append(len(gtRects) - 1)
        evaluationLog += 'GT rectangles: ' + str(len(gtRects)) + (' (' + str(len(gtDontCareRectsNum)) + " don't care)\n" if len(gtDontCareRectsNum) > 0 else '\n')
        if resFile in subm:
            if isinstance(subm[resFile], bytes):
                detFile = rrc_evaluation_funcs.decode_utf8(subm[resFile])
            else:
                detFile = subm[resFile]
            pointsList, _, _ = rrc_evaluation_funcs.get_tl_line_values_from_file_contents(detFile, evaluationParams['CRLF'], True, False, False)
            for n in range(len(pointsList)):
                points = pointsList[n]
                detRect = Rectangle(*points)
                detRects.append(detRect)
                detPolPoints.append(points)
                if len(gtDontCareRectsNum) > 0:
                    for dontCareRectNum in gtDontCareRectsNum:
                        dontCareRect = gtRects[dontCareRectNum]
                        intersected_area = area(dontCareRect, detRect)
                        rdDimensions = (detRect.xmax - detRect.xmin + 1) * (detRect.ymax - detRect.ymin + 1)
                        if rdDimensions == 0:
                            precision = 0
                        else:
                            precision = intersected_area / rdDimensions
                        if precision > evaluationParams['AREA_PRECISION_CONSTRAINT']:
                            detDontCareRectsNum.append(len(detRects) - 1)
                            break
            evaluationLog += 'DET rectangles: ' + str(len(detRects)) + (' (' + str(len(detDontCareRectsNum)) + " don't care)\n" if len(detDontCareRectsNum) > 0 else '\n')
            if len(gtRects) == 0:
                recall = 1
                precision = 0 if len(detRects) > 0 else 1
            if len(detRects) > 0:
                outputShape = [len(gtRects), len(detRects)]
                recallMat = np.empty(outputShape)
                precisionMat = np.empty(outputShape)
                gtRectMat = np.zeros(len(gtRects), np.int8)
                detRectMat = np.zeros(len(detRects), np.int8)
                for gtNum in range(len(gtRects)):
                    for detNum in range(len(detRects)):
                        rG = gtRects[gtNum]
                        rD = detRects[detNum]
                        intersected_area = area(rG, rD)
                        rgDimensions = (rG.xmax - rG.xmin + 1) * (rG.ymax - rG.ymin + 1)
                        rdDimensions = (rD.xmax - rD.xmin + 1) * (rD.ymax - rD.ymin + 1)
                        recallMat[gtNum, detNum] = 0 if rgDimensions == 0 else intersected_area / rgDimensions
                        precisionMat[gtNum, detNum] = 0 if rdDimensions == 0 else intersected_area / rdDimensions
                evaluationLog += 'Find one-to-one matches\n'
                for gtNum in range(len(gtRects)):
                    for detNum in range(len(detRects)):
                        if gtRectMat[gtNum] == 0 and detRectMat[detNum] == 0 and (gtNum not in gtDontCareRectsNum) and (detNum not in detDontCareRectsNum):
                            match = one_to_one_match(gtNum, detNum)
                            if match is True:
                                if is_single_overlap(gtNum, detNum) is True:
                                    rG = gtRects[gtNum]
                                    rD = detRects[detNum]
                                    normDist = center_distance(rG, rD)
                                    normDist /= diag(rG) + diag(rD)
                                    normDist *= 2.0
                                    if normDist < evaluationParams['EV_PARAM_IND_CENTER_DIFF_THR']:
                                        gtRectMat[gtNum] = 1
                                        detRectMat[detNum] = 1
                                        recallAccum += evaluationParams['MTYPE_OO_O']
                                        precisionAccum += evaluationParams['MTYPE_OO_O']
                                        pairs.append({'gt': gtNum, 'det': detNum, 'type': 'OO'})
                                        evaluationLog += 'Match GT #' + str(gtNum) + ' with Det #' + str(detNum) + '\n'
                                    else:
                                        evaluationLog += 'Match Discarded GT #' + str(gtNum) + ' with Det #' + str(detNum) + ' normDist: ' + str(normDist) + ' \n'
                                else:
                                    evaluationLog += 'Match Discarded GT #' + str(gtNum) + ' with Det #' + str(detNum) + ' not single overlap\n'
                evaluationLog += 'Find one-to-many matches\n'
                for gtNum in range(len(gtRects)):
                    if gtNum not in gtDontCareRectsNum:
                        match, matchesDet = one_to_many_match(gtNum)
                        if match is True:
                            evaluationLog += 'num_overlaps_gt=' + str(num_overlaps_gt(gtNum))
                            if num_overlaps_gt(gtNum) >= 2:
                                gtRectMat[gtNum] = 1
                                recallAccum += evaluationParams['MTYPE_OO_O'] if len(matchesDet) == 1 else evaluationParams['MTYPE_OM_O']
                                precisionAccum += evaluationParams['MTYPE_OO_O'] if len(matchesDet) == 1 else evaluationParams['MTYPE_OM_O'] * len(matchesDet)
                                pairs.append({'gt': gtNum, 'det': matchesDet, 'type': 'OO' if len(matchesDet) == 1 else 'OM'})
                                for detNum in matchesDet:
                                    detRectMat[detNum] = 1
                                evaluationLog += 'Match GT #' + str(gtNum) + ' with Det #' + str(matchesDet) + '\n'
                            else:
                                evaluationLog += 'Match Discarded GT #' + str(gtNum) + ' with Det #' + str(matchesDet) + ' not single overlap\n'
                evaluationLog += 'Find many-to-one matches\n'
                for detNum in range(len(detRects)):
                    if detNum not in detDontCareRectsNum:
                        match, matchesGt = many_to_one_match(detNum)
                        if match is True:
                            if num_overlaps_det(detNum) >= 2:
                                detRectMat[detNum] = 1
                                recallAccum += evaluationParams['MTYPE_OO_O'] if len(matchesGt) == 1 else evaluationParams['MTYPE_OM_M'] * len(matchesGt)
                                precisionAccum += evaluationParams['MTYPE_OO_O'] if len(matchesGt) == 1 else evaluationParams['MTYPE_OM_M']
                                pairs.append({'gt': matchesGt, 'det': detNum, 'type': 'OO' if len(matchesGt) == 1 else 'MO'})
                                for gtNum in matchesGt:
                                    gtRectMat[gtNum] = 1
                                evaluationLog += 'Match GT #' + str(matchesGt) + ' with Det #' + str(detNum) + '\n'
                            else:
                                evaluationLog += 'Match Discarded GT #' + str(matchesGt) + ' with Det #' + str(detNum) + ' not single overlap\n'
                numGtCare = len(gtRects) - len(gtDontCareRectsNum)
                if numGtCare == 0:
                    recall = float(1)
                    precision = float(0) if len(detRects) > 0 else float(1)
                else:
                    recall = float(recallAccum) / numGtCare
                    precision = float(0) if len(detRects) - len(detDontCareRectsNum) == 0 else float(precisionAccum) / (len(detRects) - len(detDontCareRectsNum))
                hmean = 0 if precision + recall == 0 else 2.0 * precision * recall / (precision + recall)
        methodRecallSum += recallAccum
        methodPrecisionSum += precisionAccum
        numGt += len(gtRects) - len(gtDontCareRectsNum)
        numDet += len(detRects) - len(detDontCareRectsNum)
        perSampleMetrics[resFile] = {'precision': precision, 'recall': recall, 'hmean': hmean, 'pairs': pairs, 'recallMat': [] if len(detRects) > 100 else recallMat.tolist(), 'precisionMat': [] if len(detRects) > 100 else precisionMat.tolist(), 'gtPolPoints': gtPolPoints, 'detPolPoints': detPolPoints, 'gtDontCare': gtDontCareRectsNum, 'detDontCare': detDontCareRectsNum, 'evaluationParams': evaluationParams, 'evaluationLog': evaluationLog}
    methodRecall = 0 if numGt == 0 else methodRecallSum / numGt
    methodPrecision = 0 if numDet == 0 else methodPrecisionSum / numDet
    methodHmean = 0 if methodRecall + methodPrecision == 0 else 2 * methodRecall * methodPrecision / (methodRecall + methodPrecision)
    methodMetrics = {'precision': methodPrecision, 'recall': methodRecall, 'hmean': methodHmean}
    resDict = {'calculated': True, 'Message': '', 'method': methodMetrics, 'per_sample': perSampleMetrics}
    return resDict
if __name__ == '__main__':
    rrc_evaluation_funcs.main_evaluation(None, default_evaluation_params, validate_data, evaluate_method)