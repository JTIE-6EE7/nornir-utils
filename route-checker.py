#!/usr/bin/env python

import os
import argparse
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir.core.inventory import Inventory, Host, Group
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from rich import print as pretty
from pprint import pprint as pp

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--routes", action="store_true", help="show IP routes")
parser.add_argument("-n", "--net", default="", help="show a single network")
parser.add_argument("-f", "--net_file", default="", help="import a list of networks")
args = parser.parse_args()


# function to collect info from devices
def collect_info(task):


    if args.net:
        networks = [
            args.net
        ]

    elif args.net_file:
        networks = [] 
        net_file = args.net_file
        with open(net_file) as fh:
            for line in fh:
                net = line.rstrip()
                networks.append(f"{net}")

    else:
        networks = [
            "10.0.0.0/8",
    ]
        

    # init list of routes
    routes = []
    # build command for each network
    for net in networks:
        cmd = f"show ip route {net} longer vrf all"
        # run nornir to collect routing table for that route
        output = task.run(task=netmiko_send_command, use_textfsm=True, command_string=cmd)

        # add result to list of routes
        if isinstance(output.result, list):
            routes.append(output.result)
    #print(routes)
    task.host['routes'] = routes


# function to check routes and next hops
def check_routes(task):
    # print each hostname
    pretty(f"\n[bold deep_sky_blue1]HOST: {task.host}")

    # recursive function to find dicts within lists within lists
    def find_routes(nested_routes_list):
        # init list of routes found
        routes = []
        #interate over nested list
        for item in nested_routes_list:
            # if dict, add it to routes
            if isinstance(item, dict):
                routes.append(item)
            # is list, do it again
            elif isinstance(item, list):
                routes.extend(find_routes(item))
        # return list of dicts (routes found)
        return routes

    # run outer function and get a list of routes
    routes = find_routes(task.host['routes'])

    # parse routes and print output
    for route in routes:
        print(f"{route['network']: <13} via {route['nexthop_if']: <8} - {route['nexthop_ip']}")


# Initializing and running the Norn
def main():

    # Init the Norn!
    nr = InitNornir()

    # get creds from env variables if not set in inventory
    if nr.inventory.defaults.username == None:
        nr.inventory.defaults.username = os.getenv("nornir_usr")

    if nr.inventory.defaults.password == None:
        nr.inventory.defaults.password = os.getenv("nornir_pwd")

    # Run the Norn!
    result = nr.run(task=collect_info)

    # fixes print overlap
    nr.runner.num_workers = 1

    # Route validation task
    if args.routes:
        print("\n" + "~" * 40)
        pretty(f"\n[bold deep_sky_blue1]*** ROUTE STATUS ***")

        nr.run(task=check_routes)


if __name__ == "__main__":
    main()
