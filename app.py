# https://docs.python.org/3/howto/logging-cookbook.html#a-cli-application-starter-template

import argparse
import importlib
import logging
import logging.handlers
from rich.logging import RichHandler
from pathlib import Path
import os
import sys

from settings import Settings

def main():
    scriptname = os.path.basename(__file__)
    parser = argparse.ArgumentParser(scriptname)
    levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')

    parser.add_argument('--log-level', default='INFO', choices=levels)
    parser.add_argument('--config-path', default='config.env', help='Config path', type=Path)
    subparsers = parser.add_subparsers(dest='command', help='Available commands:')

    # dump for kodi
    dump_for_kodi_cmd = subparsers.add_parser('dump_for_kodi', help='Dump .vsmeta to .nfo if not exist')
    dump_for_kodi_cmd.add_argument('file', metavar='FILE', help='File or folder to process', type=Path)

    # update media database
    update_media_database_cmd = subparsers.add_parser('update_media_database', help='Update media database from NFOs for further analysis')
    update_media_database_cmd.add_argument('files', metavar='FILES', help='NFO to be scanned', nargs='+', type=Path)

    # launch media dashboard
    subparsers.add_parser('launch_media_dashboard', help='Launch grafana dashboard provisioned with media stats dashboard')

    options = parser.parse_args()
    # the code to dispatch commands could all be in this file. For the purposes
    # of illustration only, we implement each command in a separate module.
    try:
        mod = importlib.import_module(f'media_dashboard.commands.{options.command}')
        cmd = getattr(mod, 'command')
    except (ImportError, AttributeError):
        print('Unable to find the code for command \'%s\'' % options.command)
        return 1

    config = Settings(_env_file=options.config_path, _env_file_encoding='utf-8') # type: ignore

    # Could get fancy here and load configuration from file or dictionary
    fh = logging.handlers.TimedRotatingFileHandler( filename=config.Logger.file_path if config.Logger else 'log.txt')
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    ch = RichHandler(rich_tracebacks=True)
    ch.setFormatter(logging.Formatter('%(message)s'))

    logging.basicConfig(level=options.log_level, handlers=(fh, ch,))

    cmd(options, config)


if __name__ == '__main__':
    sys.exit(main())
