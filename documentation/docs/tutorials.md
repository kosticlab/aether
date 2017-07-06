
# Prerequisite Skills
To follow along with this tutorial, you should have working knowledge of the Unix command line and Bash.
If you are not familiar with these, we have included links to several free tutorials below.
Note that they are sorted by time investment and in ascending order.

- [Unix Basics for Bioinformatics](http://bioinformatics.uconn.edu/unix-basics/ )
- [Just Enough Unix for Bioinformatics](http://jnmaloof.github.io/BIS180L_web/2017/04/04/2Just_Enough_Unix/)
- [Command Line Bootcamp](http://rik.smith-unna.com/command_line_bootcamp/)
- [Advanced Bash-Scripting Guide](http://www.tldp.org/LDP/abs/html/index.html)

You should also be somewhat familiar with Amazon Web Services \(AWS\), and have an AWS account.
If you do not feel comfortable with using AWS, we recommend that you consider reading through [this tutorial](http://docs.aws.amazon.com/gettingstarted/latest/awsgsg-intro/gsg-aws-intro.html).
An Azure account may also be used.
You can learn more about using Azure [here](https://docs.microsoft.com/en-us/azure/fundamentals-introduction-to-azure).

---

# Prerequisite Software

To run Aether, you will need a copy of Python (Version 2.7).
If you have not already installed Python, we recommend installing [Anaconda](https://www.continuum.io/downloads), which comes with Python and several core packages.
Instructions for installing Anaconda are available [here](https://docs.continuum.io/anaconda/install/).

## With Anaconda
If you have Anaconda, dependencies for Aether are handled automatically during the installation process.


## Without Anaconda

If you do not use Anaconda, you will have to install dependencies manually.
This is not recommended.
These dependencies are:

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [AWS Command Line Interface](https://aws.amazon.com/cli/)
- [Azure Command Line Interface](https://azure.github.io/projects/clis/)
- [jq](https://stedolan.github.io/jq/)
- [scipy](https://www.scipy.org/install.html)
- [numpy](http://www.numpy.org/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [Click](http://click.pocoo.org/5/)

If you would like to build the documentation, you will also have to install [MkDocs](http://www.mkdocs.org/#installation).

---

# Configuration and Setup
In this section, you will find a detailed explanation of how to install or uninstall Aether.
We also describe how to build the documentation page on your own machine.

---

## Installation
To install Aether, you first need to acquire a copy of it from [GitHub](https://github.com/kosticlab/aether).
To do this, you may either clone the git repository, or download an archive.
To clone the git repository, run the following in the command line:
```sh
git clone git@github.com:kosticlab/aether.git
```
Alternatively, you can download an archive of Aether [here](https://github.com/kosticlab/diabimmune/archive/master.tar.gz).
To unpack the archive, run the following:
```sh
tar -xvf aether-master.tar.gz
mv aether-master aether
```

Once you have acquired a copy of Aether, open the directory for Aether.
We herein refer to this directory, or folder, as the "Aether directory".
If you have Anaconda installed, simply run:
```sh
make build
```
If you do not have Anaconda installed, instead run:
```sh
make build-noconda
```

---

## Building Documentation
If you would like to build the documentation for Aether on your machine, run the following commands while in the Aether directory:
```sh
make docs
```
Note that some additional instructions for viewing the docs will be printed to your console when you run this command.

---

## Removal
If you would like to uninstall Aether from your machine, simply run the following commands while in the Aether directory:
```sh
make clean
```

Once the Aether package has been uninstalled, simply delete the Aether directory that you downloaded from GitHub.

---

# Running Aether
This section contains a detailed overview of Aether and how it functions.
It also contains explanations of the various data used by Aether.

---

## Execution Modes for Aether
Aether can be run in several different modes.
The three primary modes are interactive mode, non-interactive mode, and "dry run" mode.
The interactive mode will prompt the user for the various inputs, whereas the non-interactive mode will pull this information from the command line arguments.
Lastly, the "dry run" mode will show the user what resources Aether would have bid on, as well as their cost.
However, "dry run" mode will not actually run anything on the cloud, and thus will not result in any cloud resources being used.
Information about running Aether with these modes is located below.

### Interactive Mode
When Aether is run in interactive mode, it will prompt you for the various
program parameters.
Because Aether's optimization method requires a number of parameters, the
interactive mode is highly recommended for new users.
To run interactive mode, simply run the following in the Aether directory:
```sh
aether --interactive [ARGS]
```
Or
```sh
aether --I [ARGS]
```

### Non-Interactive Mode
The non-interactive mode will not prompt the user for any input information.
Non-interactive mode is generally not recommended for new users.
To run Aether in non-interactive mode, simply run the following in the Aether
directory:
```sh
aether [ARGS]
```

### Dry-Run Mode
The dry-run mode will show the user what bids Aether suggests, but will not use
any cloud resources.
To run Aether in dry-run mode, simply run the following in the Aether directory:
```sh
aether --dry-run [ARGS]
```
Note that you can run the Dry-Run mode in interactive mode by just adding the
``--interactive`` or ``-I`` argument to this command.

### Command Line Arguments
As always, additional information about command line arguments for may be found by running:
```
aether --help
```
This will output the following:

```text
Usage: aether [OPTIONS]

  The Aether Command Line Interface

Options:
  -I, --interactive             Enables interactive mode.
  --dry-run                     Runs Aether in dry-run mode. This shows what
                                cloud computing resources Aether would use,
                                but does not actually use them or perform any
                                computation.
  -A, --input-file TEXT         The name of a text file, wherein each line
                                corresponds to an argument passed to one of
                                the distributed batch jobs.
  -L, --provisioning-file TEXT  Filename of the provisioning file.
  -P, --processors INTEGER      The number of cores that each batch job
                                requires
  -M, --memory INTEGER          The amount of memory, in Gigabytes, that each
                                batch job will require.
  -N, --name TEXT               The name of the project. This should be
                                unique, as an S3 bucket is created on Amazon
                                for this project, and they must have unique
                                names.
  -E, --key-ID TEXT             Cloud CLI Access Key ID.
  -K, --key TEXT                Cloud CLI Access Key.
  -R, --region TEXT             The region/datacenter that the pipeline should
                                be run in (e.g. "us-east-1").
  -B, --bin-dir TEXT            The directory with applications runnable on
                                the cloud image that are dependencies for your
                                batch jobs. Paths in your scripts must be
                                reachable from the top level of this
                                directory.
  -S, --script TEXT             The script to be run for every line in input-
                                file and distributed across the cluster.
  -D, --data TEXT               The directory of any data that the job script
                                will need to access.
  --help                        Show this message and exit.
```

---

## Finding Account Information Required to Run Aether

Not all of the data that Aether needs to run can be securely accessed automatically.
In particular, we do not access your private AWS account information, and instead require the user to input this information.
We provide details on how to find this data in the sections below.

---

### Access Key Information

Instructions for locating your AWS Access Key ID and Access Key can be found [here](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

---

### Instance Limits Information

When you run Aether, you will be prompted for some information on account limits, as AWS does not allow them to be programmatically retrieved.
In the ``.gif`` below, we show a demonstration of where to access this information on the [AWS website](https://aws.amazon.com).

![An animation showing how to access the AWS Account Limits](resources/limits.gif "How To Find Account Limits")

These account limits are automatically saved in the ``instances.p`` file, and may be entered into the bidder on subsequent runs to save time.

Once you have entered account limits into Aether, it will begin solving the multi-objective optimization problem of selecting the optimal bidding strategy.
This is a computationally intensive process, during which Aether is iteratively performing a number of high-dimensional convex optimizations.
On a lightweight computer \(e.g., an older laptop\), this may impact performance of other programs that are running.

---

## Cloud Resource Provisioning Information

After running Aether, you will find that it has generated a new file, named ``prov.psv``.
This file contains the provisioning information for the batch processing pipeline, which is the second component of Aether.
We turn now to the details of ``prov.psv``.
Each line in ``prov.psv`` is a list delimited by the vertical bar character.
In order, the columns represent``TYPE``, ``PROCESSORS``, ``RAM``, ``STORAGE``, ``BIDDABLE``, which we explain in the table below.

| Column Name | Definition                                                                           |
|------------:|:-------------------------------------------------------------------------------------|
| TYPE        | The type of instance that is being requested. This is a name defined by the provider.|
| PROCESSORS  | The number of processors that are available to this type of instance.                |
| RAM         | The amount of Random Access Memory (RAM) that is available to this type of instance. |
| STORAGE     | Whether there is ephemeral storage available to this instance during use.            |
| BIDDABLE    | Whether this instance should be bid upon or purchased at its standard market price.  |

As an example, if ``prov.psv`` contains the following:

```text
c4.large|2|3|false|true
c4.large|2|3|false|false
```

Then Aether would instruct the batch processing pipeline to spin up two ``c4.large`` instances, purchasing one at market cost and bidding on the second one.
As an aside, it is possible to run the batch processing pipeline without the bidder if you already have ``prov.psv`` (e.g., generated it manually, reusing it).
To do so, simply replace ``--file=prov.psv`` with ``--file=YourFileHere.psv``, where ``YourFileHere.psv`` is the name of your ``.psv`` file with the provisioning information in it.

---

## Job Run-Time Environment and Resources Available by Default

Each time you submit a batch of jobs to Aether, it provides some information about the environment to the job that is being executed.
An example of this is seen below.
A copy of this template is also located in ``examples/template``.
Additionally, the ``bin`` folder that was uploaded to the cloud should be available to the job script at ``bin``.
Note that this is not the global ``/bin``, but instead relative to the job script's execution location.

```bash
#!/bin/bash
PASSEDARGUMENT=$1
PROCS=$2
MEMFRAC=$3
PRIMARYHOST=$4
OUTPUTFOLDER=$5
LOCALIP=$6
# Code goes here (likely includes uploading of results to s3 bucket)

# Access uploaded scripts, programs, and binaries e.g. "python
#bin/uploaded_script_name.py" or "bin/upload_script_name.sh"

#this script should always conclude with the line below in order to tell the
master node to assign a new job.
bin/terminate_job.sh $6 $1 $4

```

Details about these parameters are shown in the table below.

| Parameter        | Information                                                                                            |
|-----------------:|:-------------------------------------------------------------------------------------------------------|
| PASSEDARGUMENT   | The string representing an argument for an individual batch job                                        |
| PROCS            | The number of processors that this task can safely utilize.                                            |
| MEMFRAC          | The memory fraction of the current node that this task can safely utilize.                             |
| PRIMARYHOST      | The static IP address of the node controlling batch processing. Will be notified upon task completion. |
| OUTPUTFOLDER     | The location in cloud file system to store the job outputs.                                            |
| LOCALIP          | The local IP of this machine.                                                                          |

Finally, note that any item in the DATA folder may be downloaded from the cloud file system (e.g., S3) during job run-time using the AWS or Azure Command Line Interface.
Locations could be part of pre-generated arguments, as the S3 bucket is named the same as previously chosen project name.

---

## Acessing Data Storage During Job Run-Time
To add storage to a batch node for jobs require large amounts of disk space,
run:
```
bin/add_ebs_storage.sh SIZE DEVMNT
```

Details about these parameters are shown in the table below.

| Parameter        | Information                                                                                            |
|-----------------:|:-------------------------------------------------------------------------------------------------------|
| SIZE             | The number representing the size in GB of the SSD to attach.                                           |
| DEVMNT           | The location in /dev to be created and used to mount the disk.                                         |

This utility should be run from within the batch job processing script from the
previous section, likely including a check to see whether or not the desired
disk has been previously mounted.
---

# Examples

We have included several examples of using Aether below.
Because distributed systems are inherently complex and nondeterministic, we strongly recommend reading through these examples before running Aether on your own.

---

## Example: Basic Use

In ``examples/basic`` there exists ``args.txt`` and ``test.sh``. If the batch
processing script is run with interactive mode with ``args.txt`` as the input
file argument and ``test.sh`` as the script argument the bidder will be run and
on the distributed compute that is spun up each replica node will upon receipt of a task  write the passed line from
``args.txt`` to a file, wait for 30 seconds, upload the file to S3, and then
communicate to the primary node that the job is complete and that another job
can begin. If there are no new jobs then the instances terminate themselves
automatically.

### Accessing Output

Output can be accessed in an S3 bucket that bears the same name as the project
passed in via the name argument, e.g. ``s3://projectname``. Logs that are
automatically generated are also placed in this bucket.

---

## Example: Assembling Metagenomes (in paper)

This is the example use of the pipeline that is presented in the paper that
demonstrates more complex uses. This
example is located in ``examples/metagenome_assembly``. To run this example in
interactive mode,
place ``assemble_sample.py`` in a folder with built versions of
[prokka](https://github.com/tseemann/prokka) and
[megahit](https://github.com/voutcn/megahit) and pass the location of this
folder as the bin-dir argument. Pass ``batch_script.sh``, which essentially is
just a wrapper to run the python script in ``bin``, as the script argument. Pass
the location of a folder containing fastq files of paired end metagenomic reads
as the data argument. Finally, for the input file argument, pass a text file
where each line contains the s3 locations (parameterized by name given to
project) of 2 matching paired end reads
separated by a comma, e.g.
``s3://nameofproject/data/samplexpe1.fastq.gz,s3://nameofproject/data/samplexpe2.fast1.gz``. For the analysis done in the paper 1572 samples were assembled but this script can be used on any number of samples.

---

# Advanced Features

This section discusses a number of Aether's useful, but advanced, features.
However, many of these features have complexities or unique aspects that make them less straightforward or more involved than those discussed thus far.
As such, it is recommended that you first read through the documentation above.

---

## Add A Microsoft Azure Machine To A Running Batch Processing Pipeline

To add a Microsoft azure node to a currently executing Aether pipeline, run ``bin/az.sh [args]`` where ``[args]`` are
the following 21 arguments in sequential order:

| Argument Number  | Information                                                                                            |
|-----------------:|:-------------------------------------------------------------------------------------------------------|
| 1                | Azure Username                                                                                         |
| 2                | Azure Password                                                                                         |
| 3                | Azure Subscription ID                                                                                  |
| 4                | Azure Resource Group Name                                                                              |
| 5                | Azure Location                                                                                         |
| 6                | Azure Public IP Identifier                                                                             |
| 7                | Azure DNS Identifier                                                                                   |
| 8                | Azure Virtual Network Name                                                                             |
| 9                | Azure Subnet Name                                                                                      |
| 10               | Azure NIC Name                                                                                         |
| 11               | Azure Virtual Machine Name                                                                             |
| 12               | AWS CLI Key ID                                                                                         |
| 13               | AWS CLI Key                                                                                            |
| 14               | AWS Region                                                                                             |
| 15               | Batch Jobs Azure VM Can Handle Concurrently                                                            |
| 16               | Processors Needed Per Batch Job                                                                        |
| 17               | Fraction Of Node Memory That One Task Will Utilize                                                     |
| 18               | S3 Location Where Output Should Be Uploaded To                                                         |
| 19               | Static IP Of Primary Node                                                                              |
| 20               | For Compatibility With Scripts For AWS Always Make This Argument "false"                               |
| 21               | Type Of Azure VM To Spin Up                                                                            |

---

## Add Your Local Machine To A Running Batch Processing Pipeline

Please note that it is a requirement that your hardware has a static IP address and is not being operated under any sort of scheduler.
To add your own hardware to a currently executing Aether pipeline, run
``bin/local.sh [args]`` where ``[args]`` are
the following 9 arguments in sequential order:

| Argument Number  | Information                                                                                            |
|-----------------:|:-------------------------------------------------------------------------------------------------------|
| 1                | AWS CLI Key ID                                                                                         |
| 2                | AWS CLI Key                                                                                            |
| 3                | AWS Region                                                                                             |
| 4                | Batch Jobs Your Hardware Can Handle Concurrently                                                       |
| 5                | Processors Needed Per Batch Job                                                                        |
| 6                | Fraction Of Node Memory That One Task Will Utilize                                                     |
| 7                | S3 Location Where Output Should Be Uploaded To                                                         |
| 8                | Static IP Of Primary Node                                                                              |
| 9                | For Compatibility With Scripts For AWS Always Make This Argument "false"                               |

---

