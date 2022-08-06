from pprint import pprint

from anagram import Anagram


def main(letters: str, count: int, verbose: bool):
    ana = Anagram()
    results = ana.process(letters, count)
    if verbose:
        pprint(results)
    else:
        pprint(results, stream=open("results.txt", "w"))
        pprint("Les résultats ont été écrit dans './results.txt'")


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("letters", help="Les lettres à rechercher", type=str)
    parser.add_argument("count", help="Le nombre lettre", type=int)
    parser.add_argument(
        "-v",
        "--verbose",
        help="Afficher les résultat sur la console",
        action="store_true",
    )
    args = parser.parse_args()

    main(args.letters, args.count, args.verbose)
