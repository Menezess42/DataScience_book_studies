# TQDM Library
# creates personalized loading bars

# Aqui existem poucos recursos interessantes.
# Primeiro, um iterável encapsulado em tqdm.tqdm produzirá uma barra de progresso

import tqdm
import random

for i in tqdm.tqdm(range(100)):
    # Faça algo devagar
    _ = [random.random() for _ in range(1000000)]


# It's also possible to define the bar description during exhibition.
# 4 this, capturate the tqdm iterator in a with statement

from typing import List

def primes_up_to(n: int) -> List[int]:
    primes = [2]
    with tqdm.trange(3, n) as t:
        for i in t:
            # i é primo se não for divisivel por nenhum primo anterior
            i_is_prime = not any(i % p == 0 for p in primes)
            if i_is_prime:
                primes.append(i)

            t.set_description(f"{len(primes)} primes")

    return primes

my_primes = primes_up_to(100_000)
