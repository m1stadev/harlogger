import click
from pymobiledevice3.cli.cli_common import Command
from pymobiledevice3.lockdown import LockdownClient

from harlogger.sniffers import Filters, SnifferPreference, SnifferProfile


@click.group()
def cli():
    pass


@cli.command('profile', cls=Command)
@click.option('pids', '-p', '--pid', type=click.INT, multiple=True, help='filter pid list')
@click.option('--color/--no-color', default=True)
@click.option('process_names', '-pn', '--process-name', multiple=True, help='filter process name list')
@click.option('images', '-i', '--image', multiple=True, help='filter image list')
@click.option('--request/--no-request', is_flag=True, default=True, help='show requests')
@click.option('--response/--no-response', is_flag=True, default=True, help='show responses')
@click.option('-u', '--unique', is_flag=True, help='show only unique requests per image/pid/method/uri combination')
def cli_profile(lockdown: LockdownClient, pids, process_names, color, request, response, images, unique):
    """
    Sniff using CFNetworkDiagnostics.mobileconfig profile.

    This requires the specific Apple profile to be installed for the sniff to work.
    """
    filters = Filters(pids, process_names, images)
    SnifferProfile(lockdown, filters=filters, request=request, response=response, color=color, unique=unique).sniff()


@cli.command('preference', cls=Command)
@click.option('-o', '--out', type=click.File('w'), help='file to store the har entries into upon exit (ctrl+c)')
@click.option('pids', '-p', '--pid', type=click.INT, multiple=True, help='filter pid list')
@click.option('--color/--no-color', default=True)
@click.option('process_names', '-pn', '--process-name', multiple=True, help='filter process name list')
@click.option('images', '-i', '--image', multiple=True, help='filter image list')
@click.option('--request/--no-request', is_flag=True, default=True, help='show requests')
@click.option('--response/--no-response', is_flag=True, default=True, help='show responses')
@click.option('-u', '--unique', is_flag=True, help='show only unique requests per image/pid/method/uri combination')
def cli_preference(lockdown: LockdownClient, out, pids, process_names, images, request, response, color, unique):
    """
    Sniff using the secret com.apple.CFNetwork.plist configuration.

    This sniff includes the request/response body as well but requires the device to be jailbroken for
    the sniff to work
    """
    filters = Filters(pids, process_names, images)
    SnifferPreference(lockdown, filters=filters, request=request, response=response, out=out, color=color,
                      unique=unique).sniff()


if __name__ == '__main__':
    cli()
