from lamp.utils.util import calc_ruler
import argparse

def main(high, low, size):
    ruler = calc_ruler(high, low, size)[0]
    print('Ruler:')
    for i, r in enumerate(ruler):
        print('%2d:    %.3f' % (i, r))

def build_parser():
    parser = argparse.ArgumentParser(description='Calc ruler')
    parser.add_argument('high', metavar='high', type=float, help='high')
    parser.add_argument('low', metavar='low', type=float, help='low')
    parser.add_argument('size', metavar='size', type=int, help='size')
    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    main(args.high, args.low, args.size)
