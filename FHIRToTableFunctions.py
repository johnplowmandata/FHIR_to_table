from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.encounter import Encounter
from fhir.resources.reference import Reference
from fhir.resources.coding import Coding
import pandas as pd
import os
import datetime
import time
import logging
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def CreatePatientDF():
    """
Creates an empty DataFrame to load the patient information into
    :return: patientDF - returns the empty dataframe
    """
    # define column names
    patientKeys = ['patientID','patientFamilyName','patientGivenName','patientBirthDate',
                    'patientGender','patientTelecomType','patientTelecomValue']

    # create empty dataframe prior to fetching and constructing dataframe of patient details
    patientDF = pd.DataFrame(columns=patientKeys)
    return(patientDF)

def CreateEncounterDF():
    """
    Creates an empty DataFrame to load the encounter information into
        :return: encounterDF - returns the empty dataframe
    """
    # define column names
    encounterKeys = ['encounterID','encounterStartTime','encounterEndTime','encounterLocationDisplay',
                     'encounterLocationReference','participantName','participantReference',
                     'encounterCodingDisplay','encounterCodingCode'
                     ]
    # create empty dataframe prior to fetching and constructing dataframe of patient details
    encounterDF = pd.DataFrame(columns=encounterKeys)
    return(encounterDF)

def GetPatient(res, patientDF):
    """
Parse the Patient resource for key information to be used in the table
    :param res:         takes the Patient resource as the initial input
    :param patientDF:   existing DataFrame which will be appended to by any new info found
    :return patientDF:  DataFrame with row(s) appended
    """
    # dictionary will be appended
    try:
        newPatient = {}
        patient = Patient.parse_obj(res)
        patientName = patient.name
        humanName = HumanName.parse_obj(patientName[0])
        newPatient['patientFamilyName'] = humanName.family
        newPatient['patientGivenName'] = humanName.given[0]
        newPatient['patientBirthDate'] = patient.birthDate
        newPatient['patientGender'] = patient.gender
        newPatient['patientID'] = patient.id
        telecom = patient.telecom[0]
        newPatient['patientTelecomType'] = telecom.system
        newPatient['patientTelecomValue'] = telecom.value
        patientDF = patientDF.append([newPatient])
    except Exception as err:
        print(err)
    return(patientDF, patient.id)

def GetEncounter(res, encounterDF, patientID):
    """
Parse the Encounter resource for key information to be used in the table
        :param res:           takes the Encounter resource as the initial input
        :param encounterDF:   existing DataFrame which will be appended to by any new info found
        :return encounterDF:  DataFrame with row(s) appended
        """
    try:
        newEncounter = {}
        encounter = Encounter.parse_obj(res)
        newEncounter['encounterID'] = encounter.id
        newEncounter['patientID'] = patientID
        encounterPeriod = encounter.period
        newEncounter['encounterStartTime'] = encounterPeriod.start
        newEncounter['encounterEndTime'] = encounterPeriod.end

        locationres = encounter.location[0]
        encounterLocation = locationres.location

        newEncounter['encounterLocationDisplay'] = encounterLocation.display
        newEncounter['encounterLocationReference'] = encounterLocation.reference
        participant = encounter.participant[0].individual
        newEncounter['participantName'] = participant.display
        newEncounter['participantReference'] = participant.reference
        encounterType = encounter.type[0].coding
        encounterCoding = Coding.parse_obj(encounterType[0])
        newEncounter['encounterCoding'] = encounterCoding.display
        newEncounter['encounterCodingCode'] = encounterCoding.code

        encounterDF = encounterDF.append([newEncounter])
    except Exception as err:
        print(err)

    return(encounterDF)
