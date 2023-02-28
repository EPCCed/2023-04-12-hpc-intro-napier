import sys
import datetime
from functools import reduce
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
    
    start_time = datetime.datetime.now()
    # Show the number of CPUs available
    print(f"SIZE: 1")
    
    primes = parallel_primes(k, 0, 1)
    
    elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
    print(f"The number of prime numbers is {len(primes)}")
    print(f"It took {elapsed_time}s to find them.")
