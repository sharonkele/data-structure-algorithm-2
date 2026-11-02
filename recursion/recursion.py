import random

#Generate random list
def generate_list(word_list, extra_count=3):
    shuffled_words = list(word_list)
    random.shuffle(shuffled_words)
    if word_list:
        extra_words = random.choices(word_list, k=extra_count)
        shuffled_words.extend(extra_words)

    return shuffled_words


def follow_instructions(instructions: list[str]) -> list[int]:
    visited = []
    def follow(i: int) -> list[int]:
        #base case: stop if the index is outside the list
        if i < 0 or i >= len(instructions):
            return visited
        #record the index current index
        visited.append(i)
        #find the next index based on the colour
        if instructions[i] == "blue":
            next_blue = -1
            #search for the next blue after index i
            for j in range(i + 1, len(instructions)):
                if instructions[j] == "blue":
                    next_blue = j
                    break
             #stop if there is no next blue
            if next_blue == -1:
                return visited
            next_index = next_blue + 1
        elif instructions[i] == "red":
            next_index = 2 * i + 1
        else:  # green
            next_index = i + 1
        #recursively visit the next index
        return follow(next_index)
    return follow(0)

def main():
    words = ["blue", "green", "red"]
    instructions = generate_list(word_list=words,extra_count=20)
    print("Generated instructions:")
    print(instructions)
    visted_indexes = follow_instructions(instructions)
    print("\nVisted indexes:")
    print(visted_indexes)
    print("\n Instructions visited:")
    print([instructions[i] for i in visted_indexes])

if __name__ == "__main__":
      main()

            

        