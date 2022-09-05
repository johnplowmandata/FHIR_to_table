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


## Performance
### ways to improve via code
language
multi-threading
probably ways to parse more efficiently
appending to DataFrames can get less performant when they get large - would have to test this with larger datasets and adjust batch sizes or find other ways of collating/writing the parsed info
### architectural improvements
cloud gives more options
lambda (serverless) extremely scalable and only pay for actual usgae.
S3 (or equivalent) rather than local would offer I/O scalability and storage for large volumes, as well as a ready-made archive/lifecycle facility
Even if (for some strange reason) you wanted to use EC2, that is still scalable
near real-time could be achieved by lambda being triggered when file lands in S3
files could be delivered via stream - possible to do the transformation as part of the stream

