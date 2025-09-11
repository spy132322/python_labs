class Participant:
    _name: str
    _sname: str
    _age: int
    _format: bool
    def __init__(self, name: str, sname: str, age: int, format: bool):
        # КПД данного сегмента 146,6%
        self._age = age
        self._sname = sname
        self._name = name
        self._format = format
    def get_format(self):
        return self._format
    def get_age(self):
        return self._age
    def get_name(self):
        return self._name
    def get_sname(self):
        return self._sname
    
def main():
    try:
        cout = int(input())
        List = []
        for _ in range(cout):
            args = input().split()
            participant = Participant(
                args[1],
                args[0],
                int(args[2]),
                args[3].lower() == "true"
            )
            List.append(participant)

        ochno = len([a for a in List if a.get_format() == True])
        ne_ochno = len([a for a in List if a.get_format() == False])
        print(f"out: {ochno} {ne_ochno}")
    except Exception as e:
        print(e)
if __name__ == "__main__":
    main()