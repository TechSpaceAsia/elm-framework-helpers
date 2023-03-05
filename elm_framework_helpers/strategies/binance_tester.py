import csv
import fire
import reactivex
from reactivex import operators

def aggregate(current: float, accumulator: tuple[int, int]):
    print(current, accumulator)

def back_test(path: str, step: float):
    with open(path) as csv_file:
        reader = csv.reader(csv_file)
        initial_price = float(next(reader)[1])
        csv_file.seek(0)
        reactivex.of(reader).pipe(
            operators.map(lambda x: float(x[1])),
            operators.pairwise(),
            operators.scan(
                aggregate
            , (0, 0))
        ).subscribe(print)
            
if __name__ == "__main__":
    fire.Fire(back_test)
