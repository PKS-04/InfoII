import os
import pyedflib
import numpy as np
import nilearn
import pydicom
import dicom2nifti
import matplotlib.pyplot as plt
from nilearn import plotting
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from pydicom.dataset import FileDataset
from pyedflib import highlevel
from pydicom import uid
from pydicom.errors import InvalidDicomError
import numpy as np
import sys

class EDF():
    def __init__(self):
        self.__nombre=None
        self.ruta= None
        self.__id=None
        self.__fecha=None
        self.__edad=None       
    
    def lector_mostraredf(self,ver_canales=None):
        existencia = os.path.exists('./edf')
        if existencia is False:
            carpeta = os.mkdir('./edf')
            self.carpetaedf = os.path.dirname(carpeta)
            return self.carpetaNueva
        else:
            self.carpetaedf = './edf'
            for archivo in os.listdir(self.carpetaedf):
                if archivo.endswith('.edf'):
                    try:
                        self.ruta = os.path.join(self.carpetaedf,archivo)
                        self.read = pyedflib.EdfReader(self.ruta)
                        f = pyedflib.EdfReader(self.ruta)
                        n = f.signals_in_file
                        signal_labels = f.getSignalLabels()
                        frecuencia_muestreo = f.getSampleFrequency(0) 
                        num_muestras = f.getNSamples()[0]  
                        tiempo = np.arange(num_muestras) / frecuencia_muestreo  
                        sigbufs = np.zeros((n, f.getNSamples()[0]))
                        for i in np.arange(n):
                            sigbufs[i, :] = f.readSignal(i).astype(float)            
                            plt.plot(tiempo, sigbufs[i, :])
                            plt.xlabel("Tiempo (s)")
                            plt.ylabel("Amplitud (uV)") 
                            plt.title(signal_labels[i])
                            plt.show()
                    except Exception as e:
                        print(f"Error al visualizar el archivo EDF: {e}")
                        return None, None,None 

            
                else:
                    return False
            
    def convertedf(self,edf,dicom):
        try:
            for archivo in os.listdir(edf):
                if archivo.endswith('.edf'):
                    self.ruta = os.path.join(edf,archivo)
                    self.leer = pyedflib.EdfReader(self.ruta)
                    return self.leer
                else:
                    return False
            "edf = pyedflib.EdfReader(edf)"
            ds = Dataset()   
            header = edf.getHeader()
            ds.PatientName = header['patientname']
            ds.StudyDate = edf.getStartdatetime().strftime("%Y%m%d")
            ds.StudyTime = edf.getStartdatetime().strftime("%H%M%S")
            ds.PatientBirthDate = header['birthdate']
            ds.PatientSex = header['gender']
            ds.PatientID = header['patientcode']
            ds.ManufacturerModelName = header['equipment']
            waveform_sequence = Sequence()
            shared_func_groups_seq = Sequence()
            waveform_annotation_sequence = Sequence()


            for channel_idx in range(edf.signals_in_file):
            
                waveform_ds = Dataset()

            
                waveform_ds.SamplingFrequency = edf.getSampleFrequency(channel_idx)
                waveform_ds.WaveformBitsAllocated = 16
                waveform_ds.WaveformSampleInterpretation = "SS"
                waveform_ds.WaveformData = edf.readSignal(channel_idx)
                waveform_sequence.append(waveform_ds)
                per_frame_func_groups_ds = Dataset()
                per_frame_func_groups_ds.WaveformSequence = Sequence([waveform_ds])
                per_frame_func_groups_ds.ChannelLabel = edf.getLabel(channel_idx)
                per_frame_func_groups_ds.ChannelDerivationDescription = edf.getPhysicalDimension(channel_idx)
                shared_func_groups_seq.append(per_frame_func_groups_ds)       
                waveform_annotation_ds = Dataset()
                waveform_annotation_ds.ChannelLabel = edf.getLabel(channel_idx)
                concept_code_sequence = Sequence()
                for cid in [3035, 3038, 3039, 3040]:
                    item = Dataset()
                    item.CodeValue = str(cid)
                    item.CodingSchemeDesignator = "CID"
                    item.CodeMeaning = "Concept Name"  
                    concept_code_sequence.append(item)

                waveform_annotation_ds.ConceptCodeSequence = concept_code_sequence
                waveform_annotation_sequence.append(waveform_annotation_ds)

            ds.SharedFunctionalGroupsSequence = shared_func_groups_seq
            ds.Modality = "EEG"
            ds.WaveformBitsAllocated = 16
            ds.WaveformSampleInterpretation = "SS"
            ds.NumberOfWaveformChannels = len(edf.getSignalLabels())

            ds.file_meta = Dataset()
            ds.file_meta.MediaStorageSOPClassUID = uid.ExplicitVRLittleEndian
            ds.file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
            ds.file_meta.TransferSyntaxUID = uid.ImplicitVRLittleEndian 
            ds.is_little_endian = True
            ds.is_implicit_VR = True
            ds.save_as(dicom, write_like_original=False)
            print("Conversion completa.") #EDF convert to DICOM
        except Exception as e: 
            print(f"Error al convertir el archivo EDF: {e}")
            return None, None,None
    def leerdicom(dicom):    
        dcm = pydicom.dcmread(dicom)
        print(dcm)

    def validardicom(dicom):
        try:
            pydicom.dcmread(dicom)
            print("DICOM file is valid.")
        except InvalidDicomError:
            print("DICOM file is invalid.")

class DICOM():
    def cargardicom(self,dicom):
        for archivo in os.listdir(dicom):
            if archivo.endswith('.dcm'):
                self.dicom = os.path.join(dicom,archivo)
                self.leer = pydicom.dcmread(self.dicom)
                return self.leer
            else:
                return False
    def convertdicom(self,dicom):
        self.dicom = dicom
        verificar = os.path.exists('./nifti')
        if verificar is False:
            carpeta = os.mkdir('./nifti')
            self.carpetaNueva = os.path.dirname(carpeta)
            return self.carpetaNueva
        else:
            self.carpetaNueva = './nifti'
        self.conversion = dicom2nifti.convert_directory(self.dicom,self.carpetaNueva)
        
class Imagen():
    def __init__(self):
        self.nifti= None
    def verNifti(self):
        for archivo in os.listdir(self.carpetaNueva):
          if archivo.endswith('.nii.gz'):
            self.nifti = os.path.join(self.carpetaNueva,archivo)
            self.read = nilearn.image.load_img(self.nifti)
            self.imagen = plotting.plot_anat(self.read, display_mode = '', title = '', colorbar = True, cmap = '')
            return self.imagen
          else:
            return False