# Tutorials and Usage Information

---

## Prerequisites
To follow along with this tutorial, you should have working knowledge of the unix command line.
Additionally, you should be somewhat familiar with AWS.
If you do not feel comfortable with using AWS, we recommend that you consider reading through [this tutorial](http://docs.aws.amazon.com/gettingstarted/latest/awsgsg-intro/gsg-aws-intro.html).
Lastly, to run Aether, you will need a copy of Python (Version 2.7).
If you have not already installed Python, we recommend using [Anaconda](https://www.continuum.io/downloads), which comes with Python and several core packages.

---

## Configuration and Setup

### Installation
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

Once you have acquired a copy of Aether, open the directory for Aether and run the following:
```sh
    make build
```

### Building Documentation
If you would like to build the documentation for Aether on your machine, run the following commands while in the Aether directory:
```sh
    make docs
```

### Removal
If you would like to uninstall Aether from your machine, simply run the following commands while in the Aether directory:
```sh
    make clean
```

Once the Aether package has been uninstalled, simply delete the Aether directory that you downloaded from GitHub.

---

## Running Aether
Aether can be run in interactive mode and non-interactive mode.
The former will prompt the user for the various inputs, whereas the latter will pull this information from the command line arguments

### Interactive Mode
Advice on how to launch interactive mode.

### Non-Interactive Mode
Advice on how to run Aether in non-interactive mode.

---

