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

    def cargaredf(self,edf):
        for archivo in os.listdir(edf):
            if archivo.endswith('.edf'):
                self.ruta = os.path.join(edf,archivo)
                self.leer = pydicom.dcmread(self.ruta)
                return self.leer
            else:
                return False
        
    
        
    def lector_mostraredf(self,edf_path,ver_canales=None):
        edf_path = r"D:\PKS\UdeA\INfo2\DICOM_Project\chb01_01.edf"
        try:
            f=pyedflib.EdfReader(edf_path)
            n=f.signals_in_file
            frec= f.getSampleFrequency(0)
            canales= f.getSignalLabels()
            datos = np.zeros((n, f.getNSamples()[0]))  
            
            f.close()
            if ver_canales is None:
                ver_canales = canales
                n_c= len(ver_canales)
                plt.figure(figsize=(12, 6 * n_c))  
            for i, canal in enumerate(ver_canales):
                canal = canales.index(canal)
                tiempo = np.arange(datos.shape[1]) / frec 

                plt.subplot(n_c, 1, i + 1)  
                plt.plot(tiempo, datos[canal, :])  
                plt.title(canal) 
                plt.xlabel("Tiempo (s)")  
                plt.ylabel("Amplitud (uV)")  

            plt.tight_layout()  
            plt.show()  
            n_c = datos.shape[0]
            n_m = datos.shape[1]
            f = pyedflib.EdfWriter(edf_path, n_channels= n_c)
            f.setSampleFrequency(frec)
            f.setSignalLabels(canales)
            f.writeSamples(datos.flatten())
            f.close()

        except Exception as e:
            print(f"Error al visualizar el archivo EDF: {e}")
            return None, None,None 

    def convertedf(self,edf,edf_path,dicom_path):

        edf = pyedflib.EdfReader(edf_path)
        ds = Dataset()   
        header = edf.getHeader()
        ds.PatientName = header['Nombre']
        ds.StudyDate = edf.getStartdatetime().strftime("%Y%m%d")
        ds.StudyTime = edf.getStartdatetime().strftime("%H%M%S")
        ds.PatientBirthDate = header['Fecha de nacimiento']
        ds.PatientSex = header['Genero']
        ds.PatientID = header['ID']
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
                item.CodeMeaning = "Concept Name"  # Replace with the appropriate name for each CID
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
        ds.save_as(dicom_path, write_like_original=False)
        print("Conversion completa.")

def read_dicom_data(dicom_path):    
    ds = pydicom.dcmread(dicom_path)
    print(ds)

def validate_dicom_file(dicom_path):
    try:
        pydicom.dcmread(dicom_path)
        print("DICOM file is valid.")
    except InvalidDicomError:
        print("DICOM file is invalid.")

class DICOM():
    def cargardicom(self,ruta):
        for archivo in os.listdir(ruta):
            if archivo.endswith('.dcm'):
                self.ruta = os.path.join(ruta,archivo)
                self.leer = pydicom.dcmread(self.ruta)
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
        self.__nifti= None
    def visualizarNifti(self):
        for archivo in os.listdir(self.carpetaNueva):
          if archivo.endswith('.nii.gz'):
            self.ruta = os.path.join(self.carpetaNueva,archivo)
            self.read = nilearn.image.load_img(self.ruta)
            self.imagen = plotting.plot_anat(self.read, display_mode = 'ortho', title = 'Planos Axial, Sagital y Coronal', colorbar = True, cmap = 'inferno')
            return self.imagen
          else:
            return False




"""# Ejemplo de uso:
edf = "mi_archivo_eeg.edf"  # Reemplaza con el nombre de tu archivo EDF
data, frecuencia_muestreo, etiquetas_canales = leer_archivo_edf(nombre_archivo)

if data is not None:
    print("Datos de las señales:")
    print(data)
    print("Frecuencia de muestreo:", frecuencia_muestreo)
    print("Etiquetas de los canales:", etiquetas_canales)

    # Puedes acceder a los datos de un canal específico:
    canal_deseado = "EEG Fp1-F7"  # Reemplaza con la etiqueta del canal que deseas
    indice_canal = etiquetas_canales.index(canal_deseado)
    datos_canal = data[indice_canal, :]
    print(f"Datos del canal {canal_deseado}:")
    print(datos_canal)
else:
    print("No se pudieron leer los datos del archivo.")

        pass"""
       # Ejemplo de uso:
edf =EDF()
edf_path = sys.argv[0]
dicom_path = edf_path.replace(".edf", ".dcm")
edf.convertedf(edf_path, dicom_path)
edf.read_dicom_data(dicom_path)
edf.validate_dicom_file(dicom_path)
