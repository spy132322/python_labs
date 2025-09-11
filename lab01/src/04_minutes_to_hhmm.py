def min2time(mins: int):
    min = mins%60
    hours = mins//60
    return {'min': min, 'hour': hours}

def main():
    try:
        result = min2time(int(input("Минуты: ")))
        print(f"{result['hour']}:{result['min']}")
    except Exception as e:
        print(f"Да: {e}")

if __name__ == "__main__":
    main()