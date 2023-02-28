import numpy as np
import sys
import datetime
from mpi4py import MPI, futures
from functools import reduce, partial
import operator

def parallel_primes(k: int, rank=0, size=1) -> list:
    """Return a list of primes up to k
    
    Args:
        k: the number to calculate primes up to
    
    Returns:
        a list of prime integers
    """
    primes = list()
    for i in range(2+rank, k+1, size):
        reached_j = 2
        for j in range(2, i):
            if (i % j) == 0:
                break
            reached_j += 1
        if reached_j == i:
            primes.append(i)
    # print(rank, primes)
    return primes

if __name__ == '__main__':
    """Main executable.
    """
    # The largest number we should test as prime.
    k = 200_000
    
    # Declare an MPI Communicator for the parallel process to talk through
    comm = MPI.COMM_WORLD
    
    # Read the number of parallel processes tied into the comm channel
    cpus = comm.Get_size()

    # Find out the index ("rank") of *this* process
    rank = comm.Get_rank()

    if rank == 0:
        # Time how long it takes to get the primes.
        start_time = datetime.datetime.now()
        # Show the number of CPUs available
        print(f"SIZE: {cpus}")
        # Rank zero builds one list from list outputs of other ranks.
        primes_per_rank = [[]]*cpus
    else:
        primes_per_rank = None
    
    primes_dist = comm.scatter(primes_per_rank, root=0)
    primes_dist = parallel_primes(k, rank, cpus)
    primes = comm.gather(primes_dist, root=0)
    
    if rank == 0:
        primes = reduce(operator.add, primes, [])
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        print(f"The number of prime numbers is {len(primes)}")
        print(f"It took {elapsed_time}s to find them.")
