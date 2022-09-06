# ThreadSnippet.py
"""
    Does not work standalone.
    In fact I would have to restructure slightly to get this working
    Code snippet showing example of how multi-threading could be applied
"""
with ThreadPoolExecutor(max_workers=20) as executor:
    # loop through list of filenames found in directory
    for file in os.listdir(directory):
        # new thread
        # Throttle rate at which requests added (throttling can be removed if no limitations))
        time.sleep(0.1)
        # Submit jobs to the thread pool to be executed
        threads.append(
            executor.submit(GetPatient, res, patientDF)
        )
    # Collect results of completed threads and apply to DataFrames
    for task in as_completed(threads):
        try:
            patientDF, patientID = patientDF.append([task.result()])
        except Exception as err:
            print(err)
