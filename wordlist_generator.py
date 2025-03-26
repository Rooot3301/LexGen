import itertools
import os
from datetime import datetime
from typing import List, Set, Dict, Tuple
import string

class WordlistGenerator:
    def __init__(self):
        self.keywords: List[str] = []
        self.numbers: List[str] = []
        self.special_chars: List[str] = []
        self.max_combinations: int = 1000000
        self.min_length: int = 1
        self.max_length: int = 20
        self.language: str = "FR"
        
        # Leet speak mappings
        self.leet_map = {
            'a': '@', 'e': '3', 'i': '1', 'o': '0',
            's': '$', 't': '7', 'b': '8', 'g': '9',
            'l': '1', 'z': '2'
        }

    def add_keyword(self, keyword: str) -> None:
        """Add a keyword to the generator."""
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword.lower())

    def add_number(self, number: str) -> None:
        """Add a number to the generator."""
        if number and number not in self.numbers:
            self.numbers.append(number)

    def add_special_char(self, char: str) -> None:
        """Add a special character to the generator."""
        if char and char not in self.special_chars:
            self.special_chars.append(char)

    def to_leet(self, word: str) -> str:
        """Convert a word to leet speak."""
        result = ""
        for char in word.lower():
            result += self.leet_map.get(char, char)
        return result

    def generate_variations(self, word: str) -> Set[str]:
        """Generate variations of a word including leet speak and reverse."""
        variations = {word}
        
        # Add lowercase and uppercase variations
        variations.add(word.lower())
        variations.add(word.upper())
        variations.add(word.capitalize())
        
        # Add leet speak variations
        leet = self.to_leet(word)
        variations.add(leet)
        
        # Add reversed variations
        variations.add(word[::-1])
        variations.add(leet[::-1])
        
        return variations

    def import_wordlist(self, filepath: str) -> None:
        """Import words from an existing wordlist file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.add_keyword(word)
        except Exception as e:
            print(f"Error importing wordlist: {str(e)}")

    def merge_wordlists(self, filepaths: List[str]) -> Set[str]:
        """Merge multiple wordlist files, removing duplicates."""
        merged = set()
        for filepath in filepaths:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    merged.update(line.strip() for line in f if line.strip())
            except Exception as e:
                print(f"Error merging wordlist {filepath}: {str(e)}")
        return merged

    def generate_wordlist(self, advanced_mode: bool = False) -> Set[str]:
        """Generate the complete wordlist."""
        base_words = set()
        
        # Add base keywords and their variations
        for keyword in self.keywords:
            if advanced_mode:
                base_words.update(self.generate_variations(keyword))
            else:
                base_words.add(keyword)

        # Generate combinations with numbers and special characters
        combinations = set()
        elements = list(base_words)
        
        if self.numbers:
            elements.extend(self.numbers)
        if self.special_chars:
            elements.extend(self.special_chars)

        # Generate combinations within length constraints
        for length in range(self.min_length, min(self.max_length + 1, len(elements) + 1)):
            for combo in itertools.permutations(elements, length):
                if len(combinations) >= self.max_combinations:
                    break
                word = ''.join(combo)
                if self.min_length <= len(word) <= self.max_length:
                    combinations.add(word)

        return combinations

    def get_statistics(self, wordlist: Set[str]) -> Dict[str, any]:
        """Calculate statistics for the generated wordlist."""
        total_chars = sum(len(word) for word in wordlist)
        avg_length = total_chars / len(wordlist) if wordlist else 0
        
        return {
            "total_combinations": len(wordlist),
            "average_length": round(avg_length, 2),
            "estimated_size_kb": round(total_chars / 1024, 2)
        }

    def save_wordlist(self, wordlist: Set[str], preview: bool = False) -> Tuple[str, Dict[str, any]]:
        """Save the wordlist to a file and return the filename and statistics."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wordlist_{timestamp}.txt"
        stats = self.get_statistics(wordlist)
        
        with open(filename, 'w', encoding='utf-8') as f:
            for word in sorted(wordlist):
                f.write(f"{word}\n")
                
        if preview:
            print("\nAperçu des 10 premiers mots :" if self.language == "FR" 
                  else "\nPreview of first 10 words:")
            for word in sorted(list(wordlist))[:10]:
                print(word)
                
        return filename, stats

def main():
    generator = WordlistGenerator()
    
    # Set language
    print("1. Français")
    print("2. English")
    lang_choice = input("Choose your language / Choisissez votre langue (1/2): ")
    generator.language = "FR" if lang_choice == "1" else "EN"
    
    # Messages dictionary
    msgs = {
        "FR": {
            "mode": "\n1. Mode Simple\n2. Mode Avancé\nChoisissez le mode (1/2): ",
            "keyword_prompt": "Entrez un mot-clé (ou 'q' pour terminer): ",
            "number_prompt": "Entrez un nombre (ou 'q' pour terminer): ",
            "special_prompt": "Entrez un caractère spécial (ou 'q' pour terminer): ",
            "min_length": "Longueur minimum des combinaisons (défaut: 1): ",
            "max_length": "Longueur maximum des combinaisons (défaut: 20): ",
            "max_combinations": "Nombre maximum de combinaisons (défaut: 1000000): ",
            "import_prompt": "Voulez-vous importer une wordlist existante ? (o/n): ",
            "import_path": "Chemin du fichier à importer: ",
            "generating": "Génération de la wordlist en cours...",
            "saved": "Wordlist sauvegardée dans le fichier: ",
            "stats": "\nStatistiques :\n- Nombre total de combinaisons : {}\n- Longueur moyenne : {} caractères\n- Taille estimée : {} KB"
        },
        "EN": {
            "mode": "\n1. Simple Mode\n2. Advanced Mode\nChoose mode (1/2): ",
            "keyword_prompt": "Enter a keyword (or 'q' to finish): ",
            "number_prompt": "Enter a number (or 'q' to finish): ",
            "special_prompt": "Enter a special character (or 'q' to finish): ",
            "min_length": "Minimum combination length (default: 1): ",
            "max_length": "Maximum combination length (default: 20): ",
            "max_combinations": "Maximum number of combinations (default: 1000000): ",
            "import_prompt": "Do you want to import an existing wordlist? (y/n): ",
            "import_path": "Path to import file: ",
            "generating": "Generating wordlist...",
            "saved": "Wordlist saved to file: ",
            "stats": "\nStatistics:\n- Total combinations: {}\n- Average length: {} characters\n- Estimated size: {} KB"
        }
    }
    
    lang = generator.language
    
    # Import existing wordlist
    if input(msgs[lang]["import_prompt"]).lower() in ['o', 'y']:
        filepath = input(msgs[lang]["import_path"])
        generator.import_wordlist(filepath)
    
    # Choose mode
    mode_choice = input(msgs[lang]["mode"])
    advanced_mode = mode_choice == "2"
    
    # Get keywords
    while True:
        keyword = input(msgs[lang]["keyword_prompt"])
        if keyword.lower() == 'q':
            break
        generator.add_keyword(keyword)
    
    # Get numbers
    while True:
        number = input(msgs[lang]["number_prompt"])
        if number.lower() == 'q':
            break
        generator.add_number(number)
    
    # Get special characters
    while True:
        char = input(msgs[lang]["special_prompt"])
        if char.lower() == 'q':
            break
        generator.add_special_char(char)
    
    # Get length constraints
    try:
        min_length = int(input(msgs[lang]["min_length"]))
        generator.min_length = min_length
    except ValueError:
        pass

    try:
        max_length = int(input(msgs[lang]["max_length"]))
        generator.max_length = max_length
    except ValueError:
        pass
    
    # Get max combinations
    try:
        max_comb = int(input(msgs[lang]["max_combinations"]))
        generator.max_combinations = max_comb
    except ValueError:
        pass
    
    print(msgs[lang]["generating"])
    wordlist = generator.generate_wordlist(advanced_mode)
    filename, stats = generator.save_wordlist(wordlist, preview=True)
    print(f"\n{msgs[lang]['saved']}{filename}")
    print(msgs[lang]["stats"].format(
        stats["total_combinations"],
        stats["average_length"],
        stats["estimated_size_kb"]
    ))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")