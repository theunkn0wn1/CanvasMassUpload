# Canvas LMS Mass upload
This is a tool to submit many files to an assignment in Canvas LMS.

This tool exists because some instructors require uploading many loose files to an assignment, which is extremely time consuming to do by hand via the Canvas LMS webpage.


# why is the package `test_harness`?
long story... FIXME

# What do i need to use this?
Python >=3.6

You will need an access token from your canvas LMS, the setup script will guide you through that process.

# Getting started
First, install the package.
```shell
 pip install . 
```

Then, for the first run you will need to generate a config file to store some global stuff, specifically the canvas LMS base url and the token.

```shell
$ gen_upload_config
===============================================
Unknown's Canvas mass-uploader, configuration helper
===============================================
This helper script will help you generate a configuration file, this is necessary to keep track of some mandatory bits that only need be set once.
Please give me the url to a sample assignment [https://canvas.saddleback.edu/courses/45192/assignments/948561]: 
Ok, for the next part you are going to need to generate an API key if you haven't already.
Unfortunately i can't do this for you, but here is the URL :: https://canvas.saddleback.edu/profile/settings
On that page, you will need to click the 'New access Token' button and fill in the prompt
Once thats done, copy the resulting key and feed it to me here 
Canvas API key (will not echo to terminal): 
2021-02-26 12:43:58.452 | INFO     | __main__:cli:50 - Done with secrets module configuration. (1/3)
2021-02-26 12:43:58.453 | INFO     | __main__:cli:54 - Done with default course module configuration. (2/3)
Ok, last step. Please enter a glob pattern for the filetypes to glob for. [*.txt *.java]: 
2021-02-26 12:44:00.106 | INFO     | __main__:cli:62 - Done with basic submission module configuration. (3/3).
2021-02-26 12:44:00.106 | DEBUG    | __main__:cli:63 - Generating configuration file...
2021-02-26 12:44:00.106 | DEBUG    | __main__:cli:68 - emitting config file...
2021-02-26 12:44:00.107 | SUCCESS  | __main__:cli:74 - Done! you can find the config file at /some/absolute/dir/mass_upload.toml
```
