import json
import math
import os
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import argparse

SAVEFIG_INFER_VALUE = 'INFER_SAVEFIG_FILENAME'


def parse_args(*argument_list):
  parser = argparse.ArgumentParser()
  parser.add_argument('--test-class', default='VariationalGMMTest')
  parser.add_argument('--test-method',
                      default='bivariateOkSeparatedNormalTest')
  parser.add_argument('--scored-grid',
                      default='target/scores/3gaussians-7k-grid.json')
  parser.add_argument('--plot', default='density',
                      choices=['density', 'components', 'difference'])
  parser.add_argument('--savefig', nargs='?', const=SAVEFIG_INFER_VALUE)
  args = parser.parse_args(*argument_list)
  return args


def load_json_dump(filename):
  with open(filename) as infile:
    data = json.load(infile)
  X, Y, Z = [], [], []
  for point in data:
    x, y = point['metrics']['data']
    X.append(x)
    Y.append(y)
    Z.append(point['score'])
  return X, Y, Z


def load_cluster_parameters(filename):
  with open(filename) as infile:
    data = json.load(infile)
  return [p['data'] for p in data]


def plot_score_contours(args):
  X, Y, Z = load_json_dump(args.scored_grid)

  minX, maxX = min(X), max(X)
  minY, maxY = min(Y), max(Y)

  size = int(math.sqrt(len(Z)))
  X = np.reshape(X, (size, size))
  Y = np.reshape(Y, (size, size))
  Z = np.reshape(Z, (size, size))

  try:
    means = load_cluster_parameters('target/scores/{0.test_class}-{0.test_method}-means.json'.format(args))  # noqa
    sigmas = load_cluster_parameters('target/scores/{0.test_class}-{0.test_method}-covariances.json'.format(args))  # noqa
    with open('target/scores/{0.test_class}-{0.test_method}-weights.json'.format(args)) as infile:  # noqa
      weights = json.load(infile)

    # normalize weights to sum to 1.
    weights = [w / sum(weights) for w in weights]
  except:
    pass

  def format_args(i):
    kwargs = {}
    kwargs['mux'] = means[i][0]
    kwargs['muy'] = means[i][1]
    kwargs['sigmax'] = math.sqrt(sigmas[i][0][0])
    kwargs['sigmay'] = math.sqrt(sigmas[i][1][1])
    kwargs['sigmaxy'] = sigmas[i][0][1]
    return kwargs

  Zgaussians = weights[0] * mlab.bivariate_normal(X, Y, **format_args(0))
  for i in range(1, len(means)):
    Zgaussians += weights[i] * mlab.bivariate_normal(X, Y, **format_args(i))

  if args.plot == 'components':
    CS = plt.contour(X, Y, Zgaussians, linewidth=10000, inline=1)
  elif args.plot == 'density':
    CS = plt.contour(X, Y, Z, linewidth=10000, inline=1)
  elif args.plot == 'difference':
    CS = plt.contour(X, Y, Z - Zgaussians, linewidth=10000, inline=1)
  plt.clabel(CS, inline=1)

  if args.savefig:
    if args.savefig == SAVEFIG_INFER_VALUE:
      name = os.path.basename(args.scored_grid).rsplit('.')[0]
      filename = 'target/plots/{}.png'.format(name)
    else:
      filename = args.savefig
    print 'saving figure to - ', filename
    plt.savefig(filename, dpi=320)
  else:
    plt.show()


if __name__ == '__main__':
  # XX, YY, ZZ = load_json_dump('target/scores/3gaussians-7k-data.json')
  # plt.hist2d(XX, YY, bins=60)
  args = parse_args()
  plot_score_contours(args)
