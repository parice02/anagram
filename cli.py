if __name__ == "__main__":
    from pprint import pprint

    from anagram import Anagram

    ana = Anagram()

    print("Le input doit être au format suivant")
    letters, count = input("letters <space> count:\t").split()
    if count.isalnum():
        count = int(count)
    else:
        raise TypeError(f"count doit être un int et non {type(count)}")

    results = ana.process(letters, count)

    pprint(results, stream=open("results.txt", "w"))
    pprint("Les résultats ont été écrit dans './results.txt'")
