import codecs
import math
import string

import matplotlib.pyplot as plt
import requests


def count_words(words):
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

        word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
    return word_count


def get_ranks(word_count):
    ranks = {}
    word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
    for i, word in enumerate(word_count):
        ranks[word] = i + 1
    return ranks


def get_zipf(word_count, ranks):
    zipf = {}
    for word in word_count:
        zipf[word] = ranks[word] * word_count[word]
    return zipf

def get_words_top10_table(words, title):
    word_count = count_words(words)
    ranks = get_ranks(word_count)
    zipf = get_zipf(word_count, ranks)

    print(
        f'{"Pos":<5} {"Word":<15} {"Count":<15} {"Rank":<15} {"Zipf":<15}')
    for i, word in enumerate(word_count):
        if i == 10:
            break
        print(
            f'{i+1:<5} {word:<15} {word_count[word]:<15} {ranks[word]:<15} {zipf[word]:<15}')

    plt.loglog([ranks[word] for word in word_count], [word_count[word] for word in word_count], marker='.', linestyle='none')
    plt.xlabel('Rank')
    plt.ylabel('Log of Frequency')
    plt.title(f"Zipf's Law for {title}")
    plt.show()

def get_words_graph(words, title):
    words_set = set()
    for i in range(0, len(words)-1):
        words_set.add((words[i], words[i+1]))

    word_connections = {}
    for word_connection in words_set:
        if word_connection[0] in word_connections:
            word_connections[word_connection[0]] += 1
        else:
            word_connections[word_connection[0]] = 1
    # word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
    word_connections = dict(sorted(word_connections.items(), key=lambda item: item[1], reverse=True))
    print(f"Word connections for: {title}")
    print(f'{"Pos":<5} {"Word":<15} {"Unique Connections":<15}')
    for i, word in enumerate(word_connections):
        if i == 10:
            break
        print(f'{i+1:<5} {word:<15} {word_connections[word]:<15}')


def get_n_grams(words, title):
    for N in range(2, 10):
        grams = [words[i: i + N] for i in range(len(words) - N + 1)]
        grams = [" ".join(gram) for gram in grams]

        unique_grams = {}
        for gram in grams:
            if gram in unique_grams:
                unique_grams[gram] += 1
            else:
                unique_grams[gram] = 1

        filtered_words = {k: v for k, v in unique_grams.items() if v > 1}
        filtered_words = dict(sorted(filtered_words.items(), key=lambda item: item[1], reverse=True))

        print(f"{N}-gram for: {title}")
        print(f'{"Pos":<5} {"Gram":<15} {"Occurences":<15}')
        for i, word in enumerate(filtered_words):
            if i == 5:
                break
            print(f'{i + 1:<5} {word:<15} {filtered_words[word]:<15}')

def solve(words, title):
    get_words_top10_table(words, title)
    get_words_graph(words, title)
    get_n_grams(words, title)

def main():
    word_count = {}
    words_voynich = []
    with open('voynich.txt', 'r') as file:
        for line in file:
            if(line.startswith("#")):
                continue
            for word in line.replace("-\n", "").replace("=\n", "").split(","):
                words_voynich.append(word.strip())

    words_croatian = []
    with codecs.open("harry_potter.txt", 'r', 'utf-8') as file:
        for line in file:
            for word in line.split(" "):
                words_croatian.append(word.strip())

    # solve(words_voynich, "Voynich Manuscript")
    solve(words_croatian, "Croatian")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

