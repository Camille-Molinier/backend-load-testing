import os
import time
import argparse
import threading
from random import randint
import matplotlib.pyplot as plt

from utils.requestor import Requestor

execution_times = []
lock = threading.Lock()


def movement_fuzzing(thread_id, requestor, max_nb_repeat, use_max_repeat):
    global execution_times

    # Get World
    world = requestor.getWorld()

    # Join
    player = requestor.join()

    # Move player
    nb_repeat = max_nb_repeat if use_max_repeat else randint(1, max_nb_repeat)
    move_times = []
    actual_dir_x = randint(-4,4)
    actual_dir_y = randint(-4,4)
    last_change_dir = 0
    for _ in range(nb_repeat):
        newX = player.pos_x + actual_dir_x
        newY = player.pos_y + actual_dir_y
        start_time = time.time()
        requestor.move(player.id, newX, newY)
        end_time = time.time()
        execution_time = end_time - start_time
        move_times.append(execution_time*1000)
        last_change_dir += 1
        if last_change_dir > 20:
            actual_dir_x = randint(-4, 4)
            actual_dir_y = randint(-4, 4)
        time.sleep(0.01)

    with lock:
        execution_times.extend(move_times)

    requestor.quit(player.id)
    print(f"Thread {thread_id} a finished {nb_repeat} executions")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--nb_threads", type=int, default=10, help="Number of threads to use"
    )
    parser.add_argument(
        "--max_nb_repeat", type=int, default=10, help="Maximum number of repeated movements"
    )
    parser.add_argument(
        "--version", type=int, default=-1, help="Maximum number of repeated movements"
    )
    parser.add_argument(
        "--use_vm", action="store_true", help="Use virtual machine or localhost"
    )
    parser.add_argument(
        "--use_max_repeat", action="store_true", help="Use only the maximum number of repeated movements"
    )

    opt = parser.parse_args()

    threads = []
    for i in range(opt.nb_threads):
        api = 'http://sharkio.istic.univ-rennes1.fr:8080' if opt.use_vm else 'http://localhost:8080'
        thread_requestor = Requestor(api)
        thread = threading.Thread(target=movement_fuzzing, args=(i, thread_requestor, opt.max_nb_repeat, opt.use_max_repeat))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All threads finished")

    host = 'vm' if opt.use_vm else 'localhost'
    repeat = f'{opt.max_nb_repeat}_repeats' if opt.use_max_repeat else 'random_repeats'
    space_repeat = repeat.replace('_', ' ')
    version = f'V{opt.version}/' if opt.version > 0 else ''

    plt.hist(execution_times, bins=30)
    plt.xlabel('Response times (ms)')
    plt.ylabel('Frequencies')
    plt.title(f'Response times for {opt.nb_threads} threads doing {space_repeat} in {host}')
    plt.savefig(f'../figs/{version}{host}/movement_fuzzing_{opt.nb_threads}_threads_{repeat}.png')
