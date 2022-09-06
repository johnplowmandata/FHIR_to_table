from FHIRToTableFunctions import *

# Get config
configParser = configparser.RawConfigParser()
configFilePath = r'c:\temp\emis\emis.cfg'
configParser.read(configFilePath)
logFile = configParser.get('FHIR-config', 'logFile')
inputDirectory = configParser.get('FHIR-config', 'inputDirectory')
outputDirectory = configParser.get('FHIR-config', 'outputDirectory')

# Setup new logger and configure
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(logFile)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Begin the process by writing a header to the log and capturing start time
logger.info('')
logger.info("*************** Begin EMIS FHIR Parse Run ****************")
startTime = datetime.datetime.now()

# Create empty DataFrames for each resource type we will capture
# (also relates to each table we will write to)
patientDF = CreatePatientDF()
encounterDF = CreateEncounterDF()

# Check and report how many files there are
numFiles = len(os.listdir(inputDirectory))
logger.info(str(numFiles) + ' files in directory ' + inputDirectory)

# Now loop through the files and parse them
for file in os.listdir(inputDirectory):
    filename = os.path.join(inputDirectory, os.fsdecode(file))

    # top-level parsing
    bundle = Bundle.parse_file(filename)
    bundle_len = len(bundle.entry)

    logger.info(str(bundle_len) + ' objects contained in file ' + filename + ' ...............processing')
    # Now parse the bundle and extract the bits we want into DataFrames
    for n in range (0, bundle_len):
        res = bundle.entry[n].resource
        if res.resource_type == 'Patient':
            patientDF, patientID = GetPatient(res, patientDF)
        elif res.resource_type == 'Encounter':
            encounterDF = GetEncounter(res, encounterDF, patientID)

# print to screen to sense-check results during dev
print(patientDF)
print(encounterDF)

# convert dates and datetimes to correct data types prior to writing to tables
patientDF['patientBirthDate'] = pd.to_datetime(patientDF['patientBirthDate'], utc=True)
encounterDF['encounterStartTime'] = pd.to_datetime(encounterDF['encounterStartTime'], utc=True)
encounterDF['encounterEndTime'] = pd.to_datetime(encounterDF['encounterEndTime'], utc=True)

# Write DataFrames to parquet
patientDF.to_parquet(os.path.join(outputDirectory, 'patient.parquet'), engine='fastparquet')
encounterDF.to_parquet(os.path.join(outputDirectory, 'encounter.parquet'), engine='fastparquet')

# Lets do a test before the end to check at least the count of patients is as expected
testDF = pd.read_parquet(os.path.join(outputDirectory, 'patient.parquet'))
assert testDF.shape[0] == numFiles, "Number of patients should match number of files ***************************** ALERT ALERT ************************"

logger.info("*************** Finished EMIS FHIR Parse Run ****************")
logger.info("Started at " + str(startTime))
logger.info("Ended at   " + str(datetime.datetime.now()))
logger.info("Elapsed    " + str(datetime.datetime.now() - startTime))
logger.info("*************************************************************")
logger.info("*************************************************************")
logger.info("*************************************************************")