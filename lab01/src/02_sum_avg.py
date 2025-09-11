def main():
    try:
        val_a: float = float(input("a: "))
        val_b: float = float(input("b: "))
        print(f"sum={val_a+val_b:.2f}; avg={(val_a+val_b)/2:.2f}")
    except Exception as a:
        print(f"Мне действительно надо что-то писать? ну вот код ошибки: {a}")

if __name__ == "__main__":
    main()