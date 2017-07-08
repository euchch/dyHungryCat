# DY's Hungry Cat

This is an all-in-one project meant to handle Dynamic-Yield's hungry cat's diet,  
It will monitor the cat intake and notify owners when it is mal-nutritiond, carful - he needs a LOT of food and is pretty picky about it to!

This is the first time I'm writing anything (let alone AWS related) in Python - so be gentle with me and don't laugh too hard at my mistakes.

## Getting Started

This project is built on top of main.py file, which includes a testing function (def) and 2 different handlers,  
1 of the handlers is meant to be run on s3 files put event (or any other method you so choose such as listenning to an sqs queue)  
the 2 handler is meant to run every set time, probably every minute, to make sure the cat is not dying of hunger, the poor little thing

### Prerequisites

Since we all have different google api users, aws users etc, there are configuration files you must add yourself in the root folder:  
passwords.json:  
```
{
    "userAccessKey": "your aws access key",
    "userSecretAccessKey": "your aws secret key",
    "gApiKey": "you google-api key <placeholder, will probably not be in use>",
    "rdsPassword": "your mysql user's password",
    "sesSecretKey": "secret key for mail sender user on amazon's ses service"
}
```
  
gApi.json:  
The json you get from google-cloud service when created oAuth2-able access

### Installing

Before uploading python as a lambda function to aws - you must install it's prerequisits onto the root directory,  
inside the file requirements.txt there's a list of pip packages that are meant to be installed before zipping the folder and uploading it to Amazon,

An example to quickly install all the packages:  
  * `xargs -L 1 pip install -e . < requirements.txt  `  
  * `Get-Content .\requirements.txt | ForEach-Object {pip install -e . $_ }`  

## Running the tests

There are no unit-testings for this project, you can run "maintest" or uncomment the lines that run the lambda function locally after setting up the event

## Deployment

This short project uses the following technologies, which you should have access to all:  
Google-cloud vision api (note you have to enable the vision api seperatly for this project)  
Amazon:  
S3 triggers to lambda functions  
Cloudwatch trigger to lambda function  
SES to send emails  
RDS to keep track on feeding and notifications  

## Built With

None, it's a pyhthon script

## Contributing

ME! :)

## Versioning

## Authors

* See: Contributing

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thank you, Dynamic yield for concidering me for a position in your company.  
Thank you for this interesting excersise, it was surprizingly frustarating as it was fun but I did enjoy lerearning and dealing with things I've never dealt with before.  
Thank you, Whoever you are for surviving, possibly enjoying, reading all the way to here.  
