''' Command line interface for Aether '''
from __future__ import print_function
import sys
import click
import os

@click.command()
@click.option('-I', '--interactive', is_flag=True, help='Enables interactive mode.')
@click.option('--dry-run', is_flag=True, help='Runs Aether in dry-run mode. This shows' +
              ' what cloud computing resources Aether would use, but does not actually' +
              ' use them or perform any computation.')
@click.option('-A', '--input-file', default='', type=str, help='The name of a text' +
              ' file, wherein each line corresponds to an argument passed to one' +
              ' of the distributed batch jobs.')
@click.option('-L', '--provisioning-file', default='prov.psv', type=str, help='Filename of the' +
              ' provisioning file.')
@click.option('-P', '--processors', default=-1, type=str, help='The number of cores' +
              ' that each batch job requires')
@click.option('-M','--memory', default=-1, type=str, help='The amount of memory, in ' +
              'Gigabytes, that each batch job will require.')
@click.option('-N', '--name', default='', type=str, help='The name of the project.' +
              ' This should be unique, as an S3 bucket is created on Amazon for this' +
              ' project, and they must have unique names.')
@click.option('-E', '--key-ID', default='',
              type=str, help='Cloud CLI Access Key ID.')
@click.option('-K', '--key', default='', type=str, help='Cloud CLI Access Key.')
@click.option('-R', '--region', default='', type=str,
              help='The region/datacenter' +
              ' that the pipeline should be run in (e.g. "us-east-1").')
@click.option('-B', '--bin-dir', default='', type=str, help='The directory with' +
              ' applications runnable on the cloud image that are dependencies for' +
              ' your batch jobs. Paths in your scripts must be reachable from the top' +
              ' level of this directory.')
@click.option('-S', '--script', default='', type=str, help='The script to be run for' +
              ' every line in input-file and distributed across the cluster.')
@click.option('-D', '--data', default='', type=str, help='The directory of any data' +
              ' that the job script will need to access.')
def cli(interactive, dry_run, input_file, provisioning_file, processors, memory, name,
        key_id, key, region, bin_dir, script, data):
    '''The Aether Command Line Interface'''
    if not interactive:
        def need_arg(argname):
            raise Exception(("Missing or incorrect argument: \"%s\". " % argname) +
                            "Rerun with \"--help\" for assistance.")
        try:
            if input_file == '':
                need_arg('input-file')
            elif provisioning_file == '':
                need_arg('provisioning-file')
            elif processors < 0:
                need_arg('processors')
            elif memory < 0:
                need_arg('memory')
            elif name == '':
                need_arg('name')
            elif key_id == '':
                need_arg('key-ID')
            elif key == '':
                need_arg('key')
            elif region == '':
                need_arg('region')
            elif bin_dir == '':
                need_arg('bin-dir')
            elif script == '':
                need_arg('script')
            elif data == '':
                need_arg('data')
            os.system("bin/initiate_compute.sh "+input_file+' '+provisioning_file+' '+processors+' '+memory+' '+name+' '+key_id+' '+key+' '+region+' '+bin_dir+' '+script+' '+data)
        except Exception as exc:
            print(exc.message, file=sys.stderr)
            sys.exit(1)
    #        elif data == '':
    #            need_arg('data')
    else:
        dirr='/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-2])+'/'
        os.system("python "+dirr+"wrapper/wrapper.py")

if __name__ == "__main__":
    cli()
