import pickle

def pickle_to_text(pickle_file, text_file):
    with open(pickle_file, "rb") as fin:
        word_vectors = pickle.load(fin)
    
    with open(text_file, "w", encoding="utf-8") as fout:
        for target_word, co_words in word_vectors.items():
            fout.write(f"{target_word}:\n")
            for co_word, t_score in co_words.items():
                fout.write(f"\t{co_word}: {t_score}\n")
            fout.write("\n")

# Example usage:
pickle_file = "all.pickle"  # replace with your pickle file path
text_file = "output_m.txt"  # replace with your desired output text file path
pickle_to_text(pickle_file, text_file)
