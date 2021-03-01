
# Backend take-home assignment
You're a developer working for a large company.

The company wants to save money on hard drives, a policy
has been put in place that requires all employees to store all their data as
zip files.

Unfortunately, most employees' computers do not have software for zipping files,
and installing such software is not possible since the entire IT department
has been sacked.

Instead, it is decided that the zipping will be handled through a service, the
construction of which is placed in your able hands.

## Requirements
The service should be designed as an HTTP API, with endpoints for the following:
* Uploading a file
  - Should take a file together with filename (stretch goal: and username), and return some
    type of file ID.
  - Should trigger a background job that zips the file.
* Retrieving a file
  - Should take a file ID and return the zipped file, or an error if the file
    hasn't been zipped yet.
* Listing files
  - Should produce a list of the uploaded files, date and size. (stretch goal: username)
* Tests for to show the functions work utilizing whatever is a common framework for the language of choice.

## Guidelines
You may use any languages and tools you like to develop a solution.

Please design your solution to be as robust and realistic as possible, and use
what you consider to be best practices for API and code design, data storage,
et cetera.

We want to get an idea how you approach real-world problems, so try to commit
often and be prepared to discuss your design choices.
