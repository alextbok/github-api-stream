
# GitHub API Stream

Provides scripts to stream all users and repositories 
from the GitHub API (taking advantage of its pagination).
The scripts are meant to be run as background processes,
as they take a while to complete (the huge number of
users/repositories is a contributing factor, but the GitHub 
API rate-limit is mainly to blame).

Out of the box, the scripts stream and print the users/repos.
To do something useful with the data, read on:

Each script contains a method for you to implement (and do
what you want with the data stream). Currently, these methods
simply print the results. These methods are process_users(...)
and process_repos(...)

Hopefully these scripts can save you some time collecting the 
data you need so you have more time to mine them.

NOTE: 
These scripts assume you have registered for the GitHub
developer program (https://developer.github.com/program/)



## Streaming users:

  This script can process ~50,000 users per hour

  To run (from the requests folder):
    python users.py <github username> <github password>



## Streaming Repositories:

  This script can process ~5,000 repositories per hour

  To run (from the requests folder):
    python repos.py <github username> <github password>
