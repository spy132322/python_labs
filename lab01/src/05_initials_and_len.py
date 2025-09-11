class Human:
    _Name: str
    _ini: str
    _len: int
    def __init__(self, name: str):
        self._Name = name
        AAA = name.strip().split()
        self._ini = ''.join(word[0].upper() for word in AAA)
        self._len = len(' '.join(word for word in AAA))
    def get_name(self):
        return self._Name
    def get_aaa(self):
        return self._ini
    def get_len(self):
        return self._len

def main():
    try:
        someone = Human(input("ФИО:"))
        print(f"Нициалы: {someone.get_aaa()}")
        print(f"Длина (символов): {someone.get_len()}")
    except Exception as e:
        print(f"Еррор: {e}")
if __name__ == "__main__":
    main()