from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
import time
import logging

def execution_time_handler(func):
    def wrapper(*args):
        start_time = time.time()
        result = func(*args)
        logging.debug(f"Execution time of function {func.__name__}: {time.time() - start_time} seconds")
        return result
    return wrapper

def numbers_without_reminder(number):
    numbers_output = []
    for i in range(1, number + 1):
        if number % i == 0:
            numbers_output.append(i)
    return numbers_output

@execution_time_handler
def factorize_synchronic(*number):
    factorize_synchronic_list = []
    for number in list(number):
        factorize_synchronic_list.append(numbers_without_reminder(number))
    return factorize_synchronic_list

@execution_time_handler
def factorize_asynchronic(*number):
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        return list(executor.map(numbers_without_reminder, list(number)))

def main():
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    
    a, b, c, d  = factorize_synchronic(128, 255, 99999, 10651060)
    a, b, c, d  = factorize_asynchronic(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

if __name__ == "__main__":
    main()
    