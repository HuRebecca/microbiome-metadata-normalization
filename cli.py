import click
import numpy as np
import pandas as pd
import re
import normalize_age as na

default_age = [] #add all column headers that have been seen before
default_unit = [] #add all column headers that have been seen before

'''
To Future Rebecca: A faster way to determine which of the default columns are
also in the present metadata file is to use set() to find the intersection

then, need to output which columns are thought to be age related but weren't used ?

*** Add age unit parameter***

Maybe add pass_context and use child functions ? 
'''



@click.group()
@click.option('--filename',
              prompt='Pick a metadata file to load',
              help='Metadata .csv or .tsv file name.')
@click.option('--delimeter',
              prompt='Delimeter used in metadata',
              help='The delimeter or separator used in the metadata file. " " for tab separated, "," for comma. " " for white space.')
@click.option('--agecolumns',
              prompt='Insert a list of age related columns in the metadata file',
              help='The numerical age-related columns to be used for normalization in the metadata')
@click.option('--unitcolumns',
              prompt='Insert a list of age unit related columns in the metadata file',
              help='The string age unit-realted columns to be used for normalization in the metadata')
def main(filename, delimeter, agecolumns=default_age, unitcolumns=default_unit):
    """Load in metadata file."""
    df = na.clean_csv(filename, delimeter)
    click.echo(df.head(5))
    df['qiita_host_age'] = normalize_age.mergenorm_age(df, agecolumns, unitcolumns)
    new_file_name = "added_age_" + str(filename)
    df.to_csv(new_file_name, index = False)


# @load_metadata.command()
# @click.option('--load_okay',
#               prompt='Is the metadata above formatted correctly? Y/N')
# def check_metadata(load_okay):
#     if load_okay == "Y" or load_okay == "y":
#         return
#     else:
#         load_metadata()


if __name__ == '__main__':
    main()

#-------------------------------------------
# import numpy as np
#
# import pyqrcode as pq
#
# import click
#
# from .functions import wifi_qr, qr2array
#
#
# @click.group()
# @click.option("--ssid", help="WiFi network name.")
# @click.option("--security", type=click.Choice(["WEP", "WPA", ""]))
# @click.option("--password", help="WiFi password.")
# @click.pass_context
# def main(ctx, ssid: str, security: str = "", password: str = ""):
#     qr = wifi_qr(ssid=ssid, security=security, password=password)
#     ctx.obj["qr"] = qr
#     ctx.obj["ssid"] = ssid
#     ctx.obj["security"] = security
#     ctx.obj["password"] = password
#
#
# @main.command()
# @click.pass_context
# def terminal(ctx):
#     print(ctx.obj["qr"].terminal())
#
#
# @main.command()
# @click.option("--filename", help="full path to the png file")
# @click.pass_context
# def png(ctx, filename, scale: int = 10):
#     ctx.obj["qr"].png(filename, scale)
#
#
# def start():
#     main(obj={})
#
#
# if __name__ == "__main__":
#     start()
