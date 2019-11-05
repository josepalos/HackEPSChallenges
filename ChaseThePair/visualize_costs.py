#!/usr/bin/env python3
import sys
import subprocess
import glob
import tempfile
import os
import json
import matplotlib.pylab as plt


BASE_PATH = os.path.dirname(os.path.realpath(__file__))
GENERATOR_PATH = os.path.join(BASE_PATH, "resources", "generatorwrapper.sh")
SOLVER_PATH = os.path.join(BASE_PATH, "chase2")

def generate_set(tmpdir, size):
    command = "{} {}".format(GENERATOR_PATH, size)
    p = subprocess.run(command, shell=True, cwd=tmpdir)
    set_file = glob.glob(os.path.join(tmpdir, "*.set"))[0]
    return set_file


def execute_solver(tmpdir, chase, set):
    command = [SOLVER_PATH, str(chase), set]
    print(command)
    p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       cwd=tmpdir)

    loading_time = None
    v1_time = None
    v2_time = None
    chasing_time = None
    total_time = None
    #print(p.stdout.decode())

    for line in p.stdout.decode().split('\n'):
        if line.startswith("Loading time:"):
            loading_time = float(line.split(':')[1])
            continue
        if line.startswith("Chasing vector 1:"):
            v1_time = float(line.split(':')[1])
            continue
        if line.startswith("Chasing vector 2:"):
            v2_time = float(line.split(':')[1])
            continue
        if line.startswith("Total Chasing time:"):
            chasing_time = float(line.split(':')[1])
            continue
        if line.startswith("Total time:"):
            total_time = float(line.split(':')[1])
            continue
    return {"loading": loading_time,
            "v1": v1_time,
            "v2": v2_time,
            "chasing": chasing_time,
            "total": total_time}
  

def main():
    times_filename = "times.json"
    generate = not os.path.isfile(times_filename)
    chase_value = 10

    if generate:
        times = {}
        sizes = [10, 10**2, 10**3, 5*10**3, 10**4, 5*10**4, 10**5, 5*10**5, 10**6,
                 5*10**6, 10**7, 5*10**7]
        for size in sizes:
            with tempfile.TemporaryDirectory() as tmpdir:
                set_file = generate_set(tmpdir, size)
                print("Set generated. Start solver")
                time = execute_solver(tmpdir, str(chase_value), set_file)
            times[size] = time
        with open(times_filename, "w") as f:
            json.dump(times, f)
    else:
        with open(times_filename, "r") as f:
            times = json.load(f)
        times = {int(k):v for k,v in times.items()}


    print(times.keys())
    lists = sorted(times.items())
    x, y = zip(*lists)

    loading = [el["loading"] for el in y]
    v1_times = [el["v1"] for el in y]
    v2_times = [el["v2"] for el in y]
    total_times = [el["total"] for el in y]
    chase_times = [el["chasing"] for el in y]
    print(chase_times)
    plt.plot(x, total_times)
    plt.plot(x, loading)
    plt.plot(x, v1_times)
    plt.plot(x, v2_times)
    plt.plot(x, chase_times)
    plt.show()
    print(times)

if __name__ == "__main__":
    main()
