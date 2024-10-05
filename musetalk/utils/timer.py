import time
import json
file = open('timing.txt', 'w')

data: dict[str, list[float]] = {}

def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        # Get the class name if the function is a method
        if args and hasattr(args[0].__class__, func.__name__):
            class_name = args[0].__class__.__name__
            if f"{class_name}.{func.__name__}" not in data:
                data[f"{class_name}.{func.__name__}"] = []
            data[f"{class_name}.{func.__name__}"].append(end_time - start_time)
            file.write(f"{class_name}.{func.__name__} took {end_time - start_time:.4f} seconds\n")
        else:
            if func.__name__ not in data:
                data[func.__name__] = []
            data[func.__name__].append(end_time - start_time)
            file.write(f"{func.__name__} took {end_time - start_time:.4f} seconds\n")

        return result
    return wrapper

def close_file():
    with open('timing.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    file.close()
