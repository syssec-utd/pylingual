import os
import numpy as np
from dicompylercore.dicomparser import DicomParser as dparser
import pydicom
from skimage.draw import polygon2mask

def load_patient(dicom_dir_path, dicom_files):
    filearray = [f for f in dicom_files if os.path.isfile(os.path.join(dicom_dir_path, f))]
    patient = {}
    dose_files = [f for f in filearray if 'dose' in f.lower()]
    for n in range(0, len(filearray)):
        dcmfile = str(os.path.join(dicom_dir_path, filearray[n]))
        dp = dparser(dcmfile)
        dcmfile = str(os.path.join(dicom_dir_path, filearray[n]))
        dp = dparser(dcmfile)
        if 'ImageOrientationPatient' in dp.ds and (not dp.GetSOPClassUID() == 'rtdose'):
            if not 'images' in patient:
                patient['images'] = []
            patient['images'].append(dp.ds)
        elif dp.ds.Modality in ['RTSTRUCT']:
            patient['rtss'] = dp.ds
        elif dp.ds.Modality in ['RTPLAN']:
            patient['rtplan'] = dp.ds
    if 'rtss' in patient:
        d = dparser(patient['rtss'])
        s = d.GetStructures()
        for k in s.keys():
            s[k]['planes'] = d.GetStructureCoordinates(k)
            s[k]['thickness'] = d.CalculatePlaneThickness(s[k]['planes'])
        patient['structures'] = s
    if 'images' in patient:
        if not 'id' in patient:
            patient.update(dparser(patient['images'][0]).GetDemographics())
        patient['images'] = [dparser(im) for im in patient['images']]
    if 'images' in patient:
        sortedimages = []
        unsortednums = []
        sortednums = []
        images = patient['images']
        sort = 'IPP'
        parallel = True
        for (i, item) in enumerate(images):
            if i > 0:
                iop0 = np.array(item.ds.ImageOrientationPatient)
                iop1 = np.array(images[i - 1].ds.ImageOrientationPatient)
                if np.any(np.array(np.round(iop0 - iop1), dtype=np.int32)):
                    parallel = False
                    break
                ipp0 = np.array(item.ds.ImagePositionPatient)
                ipp1 = np.array(images[i - 1].ds.ImagePositionPatient)
                if not np.any(np.array(np.round(ipp0 - ipp1), dtype=np.int32)):
                    parallel = False
                break
        if parallel:
            sort = 'IPP'
        elif not images[0].InstanceNumber == images[1].InstanceNumber:
            sort = 'InstanceNumber'
        elif not images[0].AcquisitionNumber == images[1].AcquisitionNumber:
            sort = 'AcquisitionNumber'
        last_im = None
        for (i, image) in enumerate(images):
            last_im = image
            if sort == 'IPP':
                unsortednums.append(image.ds.ImagePositionPatient[2])
            else:
                unsortednums.append(image.data_element(sort).value)
        if 'hf' in last_im.ds.PatientPosition.lower() and sort == 'IPP':
            sortednums = sorted(unsortednums, reverse=True)
        else:
            sortednums = sorted(unsortednums)
        for (s, num_slice) in enumerate(sortednums):
            for (i, image) in enumerate(images):
                if sort == 'IPP':
                    if num_slice == image.ds.ImagePositionPatient[2]:
                        sortedimages.append(image)
                elif num_slice == image.data_element(sort).value:
                    sortedimages.append(image)
        patient['images'] = sortedimages
    return patient

def np_struct_from_patient(patient, struct_name, case_sensitive):
    first_im = np.array(patient['images'][0].GetImage())
    im_len = len(patient['images'])
    matrix_shape = (im_len, first_im.shape[0], first_im.shape[1])
    structure_matrix = np.zeros(matrix_shape)
    for imagenum in range(0, len(patient['images'])):
        patient['images'][imagenum].ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
        structurepixlut = patient['images'][imagenum].GetPatientToPixelLUT()
        imdata = patient['images'][imagenum].GetImageData()
        z = '%.2f' % imdata['position'][2]
        if 'p' in imdata['patientposition'].lower():
            prone = True
        else:
            prone = False
        if 'ff' in imdata['patientposition'].lower():
            feetfirst = True
        else:
            feetfirst = False
        pil_im = patient['images'][imagenum].GetImage()
        np_im_bw = np.array(pil_im)
        struct_slice = np.zeros(np_im_bw.shape)
        if 'structures' in patient:
            for (id, structure) in patient['structures'].items():
                if case_sensitive:
                    found_struct = structure['name'] == struct_name
                else:
                    found_struct = structure['name'].lower() == struct_name.lower()
                if found_struct:
                    struct_slice = struct_slice_np(structure['name'], np_im_bw, structurepixlut, structure, z, prone, feetfirst)
        structure_matrix[imagenum] += struct_slice
    return structure_matrix

def get_contour_pixel_data(pixlut, contour, prone=False, feetfirst=False):
    """Convert structure data into pixel data using the patient to pixel LUT."""
    pixeldata = []
    for (p, point) in enumerate(contour):
        for (xv, xval) in enumerate(pixlut[0]):
            if xval > point[0] and (not prone) and (not feetfirst):
                break
            elif xval < point[0]:
                if feetfirst or prone:
                    break
        for (yv, yval) in enumerate(pixlut[1]):
            if yval > point[1] and (not prone):
                break
            elif yval < point[1] and prone:
                break
        pixeldata.append((xv, yv))
    return pixeldata

def struct_slice_np(name, im_slice, structurepixlut, structure, position, prone, feetfirst):
    if not 'zarray' in structure:
        structure['zarray'] = np.array(list(structure['planes'].keys()), dtype=np.float32)
        structure['zkeys'] = structure['planes'].keys()
    if not len(structure['zarray']):
        return
    zmin = np.amin(np.abs(structure['zarray'] - float(position)))
    index = np.argmin(np.abs(structure['zarray'] - float(position)))
    mask = np.zeros(np.rot90(im_slice).shape)
    if zmin < 0.5:
        for contour in structure['planes'][list(structure['zkeys'])[index]]:
            verts = []
            if contour['type'] == u'CLOSED_PLANAR':
                pixeldata = get_contour_pixel_data(structurepixlut, contour['data'], prone, feetfirst)
                point = pixeldata[-1]
                verts.append((point[0], point[1]))
                for point in pixeldata:
                    verts.append((point[0], point[1]))
            mask += polygon2mask(np.rot90(im_slice).shape, verts)
        mask = np.rot90(np.flipud(mask), 3)
        assert mask.shape == im_slice.shape
        mask[mask > 1] = 1
        return mask
    return np.zeros(im_slice.shape)

def struct_to_mask(dicom_dir, dicom_files, struct_name, case_sensitive=True):
    patient = load_patient(dicom_dir, dicom_files)
    np_struct = np_struct_from_patient(patient, struct_name, case_sensitive)
    return np_struct