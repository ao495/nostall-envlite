"""
EnvLite CLI - Command-line interface
"""
from __future__ import annotations

import sys
import argparse
from pathlib import Path
from .core import EnvLite


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="NoStall EnvLite - Lightweight environment management"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # init command
    subparsers.add_parser("init", help="Initialize EnvLite")
    
    # set command
    set_parser = subparsers.add_parser("set", help="Set environment variable")
    set_parser.add_argument("key_value", help="KEY=VALUE format")
    
    # get command
    get_parser = subparsers.add_parser("get", help="Get environment variable")
    get_parser.add_argument("key", help="Environment variable name")
    
    # load command
    subparsers.add_parser("load", help="Load environment variables")
    
    # sync command
    sync_parser = subparsers.add_parser("sync", help="Sync to remote")
    sync_parser.add_argument("--url", help="Remote sync URL")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    envlite = EnvLite()
    
    if args.command == "init":
        print("✅ EnvLite initialized")
        print(f"   Config path: {envlite.config_path}")
    
    elif args.command == "set":
        if "=" not in args.key_value:
            print("❌ Error: Use KEY=VALUE format")
            sys.exit(1)
        key, value = args.key_value.split("=", 1)
        envlite.set(key, value)
        print(f"✅ Set {key}")
    
    elif args.command == "get":
        value = envlite.get(args.key)
        if value:
            print(value)
        else:
            print(f"❌ {args.key} not found")
            sys.exit(1)
    
    elif args.command == "load":
        envlite.load()
        print("✅ Environment variables loaded")
    
    elif args.command == "sync":
        envlite.sync(args.url)
        print("✅ Sync completed")


if __name__ == "__main__":
    main()

