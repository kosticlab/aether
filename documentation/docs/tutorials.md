# Tutorials and Usage Information

---

## Prerequisites
To follow along with this tutorial, you should have working knowledge of the unix command line.
Additionally, you should be somewhat familiar with AWS.
If you do not feel comfortable with using AWS, we recommend that you consider reading through [this tutorial](http://docs.aws.amazon.com/gettingstarted/latest/awsgsg-intro/gsg-aws-intro.html).
Lastly, to run Cumulonimble, you will need a copy of Python (Version 2.7).
If you have not already installed Python, we recommend using [Anaconda](https://www.continuum.io/downloads), which comes with Python and several core packages.

---

## Configuration and Setup

### Installation
To install Cumulonimble, you first need to acquire a copy of it from [GitHub](https://github.com/kosticlab/cumulonimble).
To do this, you may either clone the git repository, or download an archive.
To clone the git repository, run the following in the command line:
```sh
    git clone git@github.com:kosticlab/cumulonimble.git
```
Alternatively, you can download an archive of Cumulonimble [here](https://github.com/kosticlab/diabimmune/archive/master.tar.gz).
To unpack the archive, run the following:
```sh
    tar -xvf cumulonimble-master.tar.gz
    mv cumulonimble-master cumulonimble
```

Once you have acquired a copy of Cumulonimble, open the directory for Cumulonimble and run the following:
```sh
    make build
```

### Building Documentation
If you would like to build the documentation for Cumulonimble on your machine, run the following commands while in the Cumulonimble directory:
```sh
    make docs
```

### Removal
If you would like to uninstall Cumulonimble from your machine, simply run the following commands while in the Cumulonimble directory:
```sh
    make clean
```

Once the Cumulonimble package has been uninstalled, simply delete the Cumulonimble directory that you downloaded from GitHub.

---

## Running Cumulonimble
Cumulonimble can be run in interactive mode and non-interactive mode.
The former will prompt the user for the various inputs, whereas the latter will pull this information from the command line arguments

### Interactive Mode
Advice on how to launch interactive mode.

### Non-Interactive Mode
Advice on how to run Cumulonimble in non-interactive mode.

---

