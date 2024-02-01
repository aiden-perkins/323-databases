# Data Lifecycle: Generation and Collection,
# using parallel lists of primitive values (ugh).
if __name__ == "__main__":
    readings = int(input("How many weather readings? "))
    temperatures = []
    pressures = []
    humidities = []

    for i in range(readings):
        temperature = float(input("Enter temperature: "))
        pressure = float(input("Enter pressure: "))
        humidity = float(input("Enter humidity: "))

        # Construct a tuple to contain the three readings and append it to the list.
        temperatures.append(temperature)
        pressures.append(pressure)
        humidities.append(humidity)

    # Echo the input to output.
    print("Your readings:")
    for i in range(len(temperatures)):
        print(f"\tTemp: {temperatures[i]}", end="")
        print(f"\tPressure: {pressures[i]}", end="")
        print(f"\tHumidity: {humidities[i]}")