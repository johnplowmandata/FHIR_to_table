# FHIR_to_table
Parsing FHIR files and writing to some table format
The remit was to take a set of synthetically produced FHIR files and write them to a tabular format (relational DB, parquet, etc.) using any common programming language.

## Description of solution
Due to the time-boxed nature of the exercise I've stuck to what I know (Python) and also stuck to a platform and environment that was most readily to hand - a Windows VM that have available with Python and Pycharm already installed and working.
I've spent the alloted time becoming familiar with the structure of the FHIR files, picking out some of the key elements and then writing the code to parse and convert those key elements. 

## Deployment and running
requirements
libraries used
how to invoke

## Limitations of the solution
only some elements picked out - hence some data is lost - enough for demo purposes though
relies on files being in a directory accessible on VM


## Performance and Scaling
### ways to improve via code
- language - there may be gains to be had by using C# or java. However, I wouldn't normally recommend this unless as a last option
- multi-threading - once the list of files in the directory/bucket/store has been captured, rather than just loop through those in a single thread, it's possible to split this into a number of threads.  See ThreadsSnippet.py for an example.
- parsing - probably ways to parse more efficiently but I haven't looked at that in detail - the focus so far has just been to get things working
- batching - appending to DataFrames can get less performant when they get large - would have to test this with larger datasets and adjust batch sizes or find other ways of collating/writing the parsed info.  I have done this very successfully before by ensuring there is write/append every 1,000 or 5,000 rowsrather than appending large numbers of rows.

### Architectural Options for Scaling
- cloud gives lots of options.  This solution built on the C:\ drive of my Windows VM was convenient for a rapid dev and build, but obviously not for deploying a proper solution.
- lambda (serverless) extremely scalable and only pay for actual usage.
- S3 (or equivalent) rather than local would offer I/O scalability and storage for large volumes, as well as a ready-made archive/lifecycle facility
- Even if (for some strange reason) you wanted to use EC2, that is still scalable to a certain extent because you can adjust the server types and storage options.  This could still be a viable option for certain load types but for most loads there are better design patterns.
- near real-time could be achieved by lambda being triggered when file lands in S3
- Containerisation - encapsulate the solution in a lightweight container such as Docker and then orchestrate using something like Kubernetes or Fargate
- Streaming - If files could be delivered via stream such as Kafka or Kinesis - possible to do the transformation as part of the streaming process.  Or the stream could be consumed by multiple consumers such as containers.

