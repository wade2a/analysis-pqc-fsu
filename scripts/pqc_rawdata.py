import os

class PQC_RawData:
    '''
    This class is used to store 'raw' measurement data and extracted parameters for use with .xml templates
    The format of fields to be filled in the xml files (capitalized) are based on https://github.com/pasenov/PQC-XML-Templates
    Additional information about layout of fields and parameters: 
    https://indico.cern.ch/event/1025087/contributions/4338409/attachments/2233160/3784425/Structure%20of%20HALFMOON%20Extracted%20Par.pdf
    
    29.09.2021, Moritz Wiehe
    '''

    def __init__(self,path,test,meta,series):
        self.data={}
        self.path=path
        self.test=test
        print(self.test,"=selftest")        
        self.sample_name=meta.get('sample_name').replace('2_S','2-S')
        print('sample name = ', self.sample_name)
        if 'HPK_VPX' in self.sample_name:
            man,batch,wafer,sensortype,hm,location=self.sample_name.split('_')
            detector = 'TRK'
        elif 'HGC' in self.sample_name: #hephy sample naming "HGC_C_300_OBA49323_18_NW"
            testlocation = 'HEPHY'
            testinstitution = 'Institut fuer Hochenergiephysik'
            man = 'HPK'
            detector = 'HGC'
            samplesplit = self.sample_name.split('_')
            sensortype = samplesplit[2]
            batch = samplesplit[3]
            wafer = samplesplit[4]
            location = samplesplit[5]
            if location == 'NW':
                location = 'TL'
            elif location == 'SE':
                location = 'BR'
            #remove after testing!!
            if sensortype.startswith('3'):
                scratchpad = '104700'
        elif "FSU" in self.sample_name:
            testlocation = 'FSU'
            testinstitution = 'Florida State University'
            man = 'HPK'
            detector = 'HGC'
            samplesplit = self.sample_name.split('_')
            scratchpad = samplesplit[1]
            location = samplesplit[2]
            batch = samplesplit[3]
            wafer = samplesplit[4]
        else:
            # Sample name could not be parsed
            man,batch,wafer,sensortype,hm,location='__','__','__','__','__','__'
            detector = 'HGC'
        if detector == 'TRK': #leaving tracker code alone
            self.sensortype=sensortype.replace('2-S','2S').replace('PSP','PS-p').replace('PSS','PS-s')
            self.sample_position=meta.get('sample_position')
            self.sample_comment=meta.get('sample_comment')
            self.contact_name=meta.get('contact_name')
            self.measurement_name=meta.get('measurement_name')
            self.measurement_type=meta.get('measurement_type')
            is_IV='iv' in self.measurement_type
            is_CV='cv' in self.measurement_type
            self.IVCV='IV' if is_IV else 'CV' if is_CV else ''
            self.start_timestamp=meta.get('start_timestamp')
            self.operator=meta.get('operator')
            self.waiting_time=meta.get('waiting_time')
            filename=os.path.basename(self.path)
            self.out_file_name= os.path.splitext(filename)[0]+'.xml'

            #self.LOCATION='Hephy'
            self.INITIATED_BY_USER=self.operator
            self.RUN_BEGIN_TIMESTAMP=self.start_timestamp.replace('T',' ')
            self.COMMENT_DESCRIPTION=''
            self.FILE_NAME=filename
            self.WAITING_TIME_S=self.waiting_time.split(' ')[0]
            
            self.NAME_LABEL=self.edit_sample_name(self.sample_name,location)
            self.KIND_OF_PART='{} Halfmoon {}'.format(self.sensortype,location[0])
            self.KIND_OF_HM_SET_ID={'L':'Left','R':'Right','_':'__'}[location[1]]
            self.KIND_OF_HM_FLUTE_ID,self.KIND_OF_HM_STRUCT_ID,self.KIND_OF_HM_CONFIG_ID=self.get_structure()
            if self.measurement_name=="FET":
                self.PAR_EXTENSION_TABLE_NAME="TC"
            else:
                self.PAR_EXTENSION_TABLE_NAME=self.IVCV

            self.VERSION=self.PAR_EXTENSION_TABLE_NAME+'_measurement-004'
            
            
            self.PROCEDURE_TYPE=self.measurement_name.replace("Capacitor","Cap").replace("structure","str").replace("Source","Src") #maximum number of letters is 40
        elif detector == 'HGC': #xml code for HGC Database
            if scratchpad.startswith('1'):
                if location == 'TL':
                    self.KIND_OF_PART = '300um Si Sensor LD Halfmoon-TL'
                else:
                    self.KIND_OF_PART = '300um Si Sensor LD Halfmoon-BR'
            elif scratchpad.startswith('2'):
                if location == 'TL':
                    self.KIND_OF_PART = '200um Si Sensor LD Halfmoon-TL'
                else:
                    self.KIND_OF_PART = '200um Si Sensor LD Halfmoon-BR'   
            elif scratchpad.startswith('3'):
                if location == 'TL':
                    self.KIND_OF_PART = '120um Si Sensor HD Halfmoon-TL'
                else:
                    self.KIND_OF_PART = '120um Si Sensor HD Halfmoon-BR'
            else:
                print('error in scratchpad')
                print('scratchpad=',scratchpad)
                input()
            #self.sensortype=sensortype.replace('2-S','2S').replace('PSP','PS-p').replace('PSS','PS-s')
            self.sample_position=meta.get('sample_position')
            self.sample_comment=meta.get('sample_comment')
            self.contact_name=meta.get('contact_name')
            self.measurement_name=meta.get('measurement_name')
            self.measurement_type=meta.get('measurement_type')
            is_IV='iv' in self.measurement_type
            is_CV='cv' in self.measurement_type
            self.IVCV='IV' if is_IV else 'CV' if is_CV else ''
            self.start_timestamp=meta.get('start_timestamp')
            self.operator=meta.get('operator')
            self.waiting_time=meta.get('waiting_time')
            filename=os.path.basename(self.path)
            self.out_file_name= os.path.splitext(filename)[0]+'.xml'
            self.SERIAL_NUMBER = scratchpad + '_' + location
            self.NAME_LABEL = self.KIND_OF_PART + scratchpad
            self.LOCATION = testlocation
            self.INSTITUTION = testinstitution
            self.RUN_NAME=filename
            self.INITIATED_BY_USER=self.operator
            self.RUN_BEGIN_TIMESTAMP=self.start_timestamp.replace('T',' ')
            self.COMMENT_DESCRIPTION=self.sample_comment
            self.FILE_NAME=filename
            
            self.WAITING_TIME_S=self.waiting_time.split(' ')[0]



            
    def add_data(self,data_dict):
        self.data={**self.data,**data_dict}

    def edit_sample_name(self,sample_name,location=None):
        sample_name=sample_name.replace('HPK_VPX','')
        if location:
            sample_name=sample_name.replace('E'+location[1],'EE')
            sample_name=sample_name.replace('W'+location[1],'WW')
        return sample_name

    def get_structure(self):
        lookup={
            'FET':['PQC1','FET_PSS','Not Used'],# PQC Flute 1 has PSS layout FET
            'MOS capacitor (HV Source)':['PQC1','MOS_QUARTER','Not Used'],
            'Capacitor test structure Left 10kHz 250mV (HV Source)':['PQC1','CAP_W','Not Used'],
            'Capacitor test structure Right 10kHz 250mV (HV Source)':['PQC1','CAP_E','Not Used'],
            'Polysilicon Van-der-Pauw cross':['PQC1','VDP_POLY','Standard'],
            'Reverse Polysilicon Van-der-Pauw cross':['PQC1','VDP_POLY','Rotated'],
            'N+ Van-der-Pauw cross':['PQC1','VDP_STRIP','Standard'],
            'Reverse N+ Van-der-Pauw cross':['PQC1','VDP_STRIP','Rotated'],
            'P-stop Van-der-Pauw cross':['PQC1','VDP_STOP','Standard'],
            'Reverse P-stop Van-der-Pauw cross':['PQC1','VDP_STOP','Rotated'],
            'GCD':['PQC2','GCD','Not Used'],
            'N+ linewidth structure':['PQC2','LINEWIDTH_STRIP','Not Used'],
            'P-stop linewidth structure (2-wire)':['PQC2','LINEWIDTH_STOP','Not Used'],
            'P-stop linewidth structure (4-wire)':['PQC2','LINEWIDTH_STOP','Not Used'],
            'Polysilicon meander':['PQC2','R_POLY','Not Used'],
            'Dielectric Breakdown 1':['PQC2','DIEL_SW','Not Used'],
            'Diode IV':['PQC3','DIODE_HALF','Not Used'],
            'Diode CV':['PQC3','DIODE_HALF','Not Used'],
            'Metal clover leaf Van-der-Pauw':['PQC3','CLOVER_METAL','Standard'],
            'Reverse Metal clover leaf Van-der-Pauw':['PQC3','CLOVER_METAL','Rotated'],
            'P+ cross-bridge Van-der-Pauw':['PQC3','VDP_EDGE','Standard'],
            'Reverse P+ cross-bridge Van-der-Pauw':['PQC3','VDP_EDGE','Rotated'],
            'P+ cross-bridge linewidth':['PQC3','VDP_EDGE','Linewidth'],
            'Bulk cross':['PQC3','VDP_BULK','Standard'],
            'Reverse bulk cross':['PQC3','VDP_BULK','Rotated'],
            'Metal meander':['PQC3','MEANDER_METAL','Not Used'],
            'GCD05':['PQC4','GCD05','Not Used'],
            'N+ CBKR':['PQC4','CBKR_STRIP','Standard'],
            'Polysilicon CBKR':['PQC4','CBKR_POLY','Standard'],
            'Polysilicon contact chain':['PQC4','CC_POLY','Not Used'],
            'P+ contact chain':['PQC4','CC_EDGE','Not Used'],
            'N+ contact chain':['PQC4','CC_STRIP','Not Used']}
        FLUTE_ID,STRUCT_ID,CONFIG_ID=lookup[self.measurement_name]

        if FLUTE_ID[-1] != self.contact_name[-1]:
            raise ValueError('Flute nr. mismatch',self.sample_name,self.test)

        return FLUTE_ID,STRUCT_ID,CONFIG_ID
