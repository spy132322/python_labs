class Human:
    _Name: str
    _Age: int
    def __init__(self, name: str, age: int = 0):
        self._Name = name
        self._Age = age
    def get_name(self):
        return self._Name
    def get_age(self):
        return self._Age

def main():
    try:
        human = Human(input("Имя: "), int(input("Возраст: ")))
        print(f"Привет, {human.get_name()}! Через год тебе будет {human.get_age() + 1}.")
    except Exception as e:
        print(f"Ничесе ты умный: {e}")
        
if __name__ =="__main__":
    main()