from FHIRToTableFunctions import *

# Setup new logger and configure
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('c:\\temp\\emis\\emis.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info('')
logger.info("*************** Begin EMIS FHIR Parse Run ****************")
startTime = datetime.datetime.now()

patientDF = CreatePatientDF()
encounterDF = CreateEncounterDF()

#directory = os.fsencode(directory_in_str)
directory = 'c:\\temp\emis\data'
numFiles = len(os.listdir(directory))
logger.info(str(numFiles) + ' files in directory ' + directory)
for file in os.listdir(directory):
    filename = os.path.join(directory, os.fsdecode(file))

    bundle = Bundle.parse_file(filename)
    bundle_len = len(bundle.entry)

    logger.info(str(bundle_len) + ' objects contained in file ' + filename + ' ...............processing')
    for n in range (0, bundle_len):
        res = bundle.entry[n].resource
        if res.resource_type == 'Patient':
            patientDF, patientID = GetPatient(res, patientDF)
        elif res.resource_type == 'Encounter':
            encounterDF = GetEncounter(res, encounterDF, patientID)

print(patientDF)
print(encounterDF)
patientDF['patientBirthDate'] = pd.to_datetime(patientDF['patientBirthDate'], utc=True)
encounterDF['encounterStartTime'] = pd.to_datetime(encounterDF['encounterStartTime'], utc=True)
encounterDF['encounterEndTime'] = pd.to_datetime(encounterDF['encounterEndTime'], utc=True)
patientDF.to_parquet('c:\\temp\emis\output\patient.parquet', engine='fastparquet')
encounterDF.to_parquet('c:\\temp\emis\output\encounter.parquet', engine='fastparquet')

logger.info("*************** Finished EMIS FHIR Parse Run ****************")
logger.info("Started at " + str(startTime))
logger.info("Ended at   " + str(datetime.datetime.now()))
logger.info("Elapsed    " + str(datetime.datetime.now() - startTime))
logger.info("*************************************************************")
logger.info("*************************************************************")
logger.info("*************************************************************")