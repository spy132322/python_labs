def main():
    try:
        pri: float = float(input("price="))
        dis: float = float(input("discount="))
        vat: float = float(input("vat="))
        base: float = pri*(1-dis/100)
        vat_am: float = base * (vat/100)
        total: float = base + vat_am
        print(f"База после скидки: {base} ₽\nНДС: {vat_am} ₽\nИтого к оплате: {total} ₽")
    except Exception as e:
        print(f"Шо, Опять? {e}")    
if __name__ == "__main__":
    main()