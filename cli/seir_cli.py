#!/usr/bin/env python3
"""
SeirChain CLI - Command Line Interface for SeirChain operations
"""

import click
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.bls_tools import bls_group
from cli.pof_tools import pof_group
from cli.data_tools import data_group
from cli.security_tools import security_group
from cli.benchmark_tools import benchmark_group
from cli.node_tools import node_group

@click.group()
@click.version_option(version="1.0.0")
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """SeirChain CLI - Tools for BLS signatures, PoF mining, and network operations"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose

# Register command groups
cli.add_command(bls_group)
cli.add_command(pof_group)
cli.add_command(data_group)
cli.add_command(security_group)
cli.add_command(benchmark_group)
cli.add_command(node_group)

if __name__ == '__main__':
    cli()
