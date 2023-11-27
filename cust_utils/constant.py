from os.path import join, abspath, dirname

ds_dir = join(abspath(dirname(dirname(__file__))), "data", "dataset", "jianhun")

weights = join(abspath(dirname(dirname(__file__))), "runs", "train", "exp", "weights", "best.pt")
