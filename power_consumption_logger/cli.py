"""Console script for power_consumption_logger."""
import argparse
import sys
import power_consumption_logger.power_consumption_logger as pcl


def main():
    """Console script for power_consumption_logger."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default='cmatic-D9CD14',
        help="""The the hostname: if not set cmatic-D9CD14 is used
            if host is set to 'simulate' artificial values (0.1)
            are delivered without invoking the web service
            """)
    parser.add_argument("--storage", default='.',
        help="Set a storage directory: if not set current directory is used")
    parser.add_argument("-p", "--period", type=int,
        help="""Period where the readout happens (in seconds),
            if not set the program reads once and writes to console
            """)
    args = parser.parse_args()
    if args.period == None:
        # one time readout for testing
        print('# timestamp C1   C2   C3   C4')
        print(data_to_str(data))
    else:
        # read continuously and do not return
        recorder = pcl.Writer(args.storage, args.host)
        recorder.record(args.period)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
