# demonstrates that only the validated data got into the pickled version.
import pickle
from weatherreading import WeatherReading

if __name__ == "__main__":
    file = open('pickle_demo.bin', 'rb')
    validated_data = pickle.load(file)
    print("The validated readings:")
    for reading in validated_data:
        print(f"\tTemp: {reading.temperature}", end="")
        print(f"\tPressure: {reading.pressure}", end="")
        print(f"\tHumidity: {reading.humidity}")
