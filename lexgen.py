import os
import time
import sys
import itertools
import random
from datetime import datetime
from typing import List, Set, Dict, Tuple
import string

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_loading_animation():
    """Display a loading animation."""
    animation = "|/-\\"
    for i in range(20):
        sys.stdout.write(f"\rInitializing LexGen {animation[i % len(animation)]}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n")

def print_banner():
    """Display the LexGen ASCII art banner."""
    banner = """
    \033[36m
    ██╗     ███████╗██╗  ██╗ ██████╗ ███████╗███╗   ██╗
    ██║     ██╔════╝╚██╗██╔╝██╔════╝ ██╔════╝████╗  ██║
    ██║     █████╗   ╚███╔╝ ██║  ███╗█████╗  ██╔██╗ ██║
    ██║     ██╔══╝   ██╔██╗ ██║   ██║██╔══╝  ██║╚██╗██║
    ███████╗███████╗██╔╝ ██╗╚██████╔╝███████╗██║ ╚████║
    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
    \033[0m
    \033[32m[ Created by Root3301 | Advanced Wordlist Generator ]\033[0m
    """
    print(banner)

class WordlistGenerator:
    def __init__(self):
        self.keywords: List[str] = []
        self.numbers: List[str] = []
        self.special_chars: List[str] = []
        self.max_combinations: int = 1000000
        self.min_length: int = 1
        self.max_length: int = 20
        self.language: str = "FR"
        
        # Create necessary directories
        self.source_dir = "source"
        self.output_dir = "wordlistgen"
        self._create_directories()
        
        # Common words for auto mode
        self.common_words = [
            "password", "admin", "root", "user", "login",
            "welcome", "secure", "123456", "qwerty", "letmein",
            "dragon", "monkey", "football", "baseball", "abc123"
        ]
        
        # Leet speak mappings
        self.leet_map = {
            'a': '@', 'e': '3', 'i': '1', 'o': '0',
            's': '$', 't': '7', 'b': '8', 'g': '9',
            'l': '1', 'z': '2'
        }

    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def get_source_files(self) -> List[str]:
        """Get list of available wordlist files in source directory."""
        try:
            files = [f for f in os.listdir(self.source_dir) if f.endswith('.txt')]
            return files
        except Exception:
            return []

    def auto_generate(self, word_count: int) -> Set[str]:
        """Automatically generate wordlist with specified number of words."""
        words = set()
        base_words = self.common_words.copy()
        numbers = ['123', '456', '789', '000', '111', '222', '333']
        special_chars = ['!', '@', '#', '$', '%', '&', '*']
        
        while len(words) < word_count:
            # Generate a random word combination
            word = random.choice(base_words)
            if random.random() > 0.5:
                word += random.choice(numbers)
            if random.random() > 0.7:
                word += random.choice(special_chars)
            
            # Add variations
            words.add(word)
            words.add(word.upper())
            words.add(word.capitalize())
            words.add(self.to_leet(word))
            
            # Add reversed versions
            if random.random() > 0.8:
                words.add(word[::-1])
            
            # Combine two words
            if random.random() > 0.6:
                word2 = random.choice(base_words)
                words.add(word + word2)
                words.add(word2 + word)
        
        return set(list(words)[:word_count])

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
            with open(os.path.join(self.source_dir, filepath), 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.add_keyword(word)
            print(f"\033[32m✓ Successfully imported wordlist: {filepath}\033[0m")
        except Exception as e:
            print(f"\033[31m✗ Error importing wordlist: {str(e)}\033[0m")

    def merge_wordlists(self, filepaths: List[str]) -> Set[str]:
        """Merge multiple wordlist files, removing duplicates."""
        merged = set()
        for filepath in filepaths:
            try:
                with open(os.path.join(self.source_dir, filepath), 'r', encoding='utf-8') as f:
                    merged.update(line.strip() for line in f if line.strip())
                print(f"\033[32m✓ Successfully merged: {filepath}\033[0m")
            except Exception as e:
                print(f"\033[31m✗ Error merging wordlist {filepath}: {str(e)}\033[0m")
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

        # Show progress animation
        total_combinations = sum(1 for _ in range(self.min_length, min(self.max_length + 1, len(elements) + 1)))
        print("\nGenerating combinations:")
        
        # Generate combinations within length constraints
        current = 0
        for length in range(self.min_length, min(self.max_length + 1, len(elements) + 1)):
            current += 1
            progress = int((current / total_combinations) * 20)
            sys.stdout.write(f"\r[{'=' * progress}{' ' * (20-progress)}] {current}/{total_combinations}")
            sys.stdout.flush()
            
            for combo in itertools.permutations(elements, length):
                if len(combinations) >= self.max_combinations:
                    break
                word = ''.join(combo)
                if self.min_length <= len(word) <= self.max_length:
                    combinations.add(word)

        print("\n")
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
        filename = os.path.join(self.output_dir, f"wordlist_{timestamp}.txt")
        stats = self.get_statistics(wordlist)
        
        with open(filename, 'w', encoding='utf-8') as f:
            for word in sorted(wordlist):
                f.write(f"{word}\n")
                
        if preview:
            print("\n\033[36mAperçu des 10 premiers mots :\033[0m" if self.language == "FR" 
                  else "\n\033[36mPreview of first 10 words:\033[0m")
            for word in sorted(list(wordlist))[:10]:
                print(f"\033[33m{word}\033[0m")
                
        return filename, stats

def display_menu(msgs, lang):
    """Display the main menu."""
    clear_screen()
    print_banner()
    print("\n" + msgs[lang]["main_menu"])
    choice = input("\n\033[36m>>> \033[0m")
    return choice

def main():
    generator = WordlistGenerator()
    
    # Initialize with loading animation
    clear_screen()
    print_loading_animation()
    clear_screen()
    print_banner()
    
    # Set language
    print("\n1. \033[36mFrançais\033[0m")
    print("2. \033[36mEnglish\033[0m")
    lang_choice = input("\nChoose your language / Choisissez votre langue (1/2): ")
    generator.language = "FR" if lang_choice == "1" else "EN"
    
    # Messages dictionary
    msgs = {
        "FR": {
            "main_menu": """
\033[36m[ Menu Principal ]\033[0m

1. Générer une nouvelle wordlist
2. Importer et fusionner des wordlists
3. Voir les statistiques
4. Quitter
""",
            "mode": "\n1. Mode Simple\n2. Mode Avancé\n3. Mode Auto\nChoisissez le mode (1/2/3): ",
            "auto_words": "Nombre de mots à générer: ",
            "keyword_prompt": "Entrez un mot-clé (ou 'q' pour terminer): ",
            "number_prompt": "Entrez un nombre (ou 'q' pour terminer): ",
            "special_prompt": "Entrez un caractère spécial (ou 'q' pour terminer): ",
            "min_length": "Longueur minimum des combinaisons (défaut: 1): ",
            "max_length": "Longueur maximum des combinaisons (défaut: 20): ",
            "max_combinations": "Nombre maximum de combinaisons (défaut: 1000000): ",
            "import_prompt": "Fichiers disponibles dans le dossier source:",
            "import_select": "Sélectionnez un fichier (numéro) ou 0 pour annuler: ",
            "generating": "\033[32mGénération de la wordlist en cours...\033[0m",
            "saved": "\n\033[32mWordlist sauvegardée dans le fichier: \033[0m",
            "stats": """\n\033[36mStatistiques :\033[0m
- Nombre total de combinaisons : \033[33m{}\033[0m
- Longueur moyenne : \033[33m{}\033[0m caractères
- Taille estimée : \033[33m{}\033[0m KB"""
        },
        "EN": {
            "main_menu": """
\033[36m[ Main Menu ]\033[0m

1. Generate new wordlist
2. Import and merge wordlists
3. View statistics
4. Quit
""",
            "mode": "\n1. Simple Mode\n2. Advanced Mode\n3. Auto Mode\nChoose mode (1/2/3): ",
            "auto_words": "Number of words to generate: ",
            "keyword_prompt": "Enter a keyword (or 'q' to finish): ",
            "number_prompt": "Enter a number (or 'q' to finish): ",
            "special_prompt": "Enter a special character (or 'q' to finish): ",
            "min_length": "Minimum combination length (default: 1): ",
            "max_length": "Maximum combination length (default: 20): ",
            "max_combinations": "Maximum number of combinations (default: 1000000): ",
            "import_prompt": "Available files in source directory:",
            "import_select": "Select a file (number) or 0 to cancel: ",
            "generating": "\033[32mGenerating wordlist...\033[0m",
            "saved": "\n\033[32mWordlist saved to file: \033[0m",
            "stats": """\n\033[36mStatistics:\033[0m
- Total combinations: \033[33m{}\033[0m
- Average length: \033[33m{}\033[0m characters
- Estimated size: \033[33m{}\033[0m KB"""
        }
    }
    
    lang = generator.language
    
    while True:
        choice = display_menu(msgs, lang)
        
        if choice == "1":
            # Generate new wordlist
            clear_screen()
            print_banner()
            
            mode_choice = input(msgs[lang]["mode"])
            
            if mode_choice == "3":  # Auto Mode
                try:
                    word_count = int(input(msgs[lang]["auto_words"]))
                    print(msgs[lang]["generating"])
                    wordlist = generator.auto_generate(word_count)
                    filename, stats = generator.save_wordlist(wordlist, preview=True)
                    print(f"{msgs[lang]['saved']}{filename}")
                    print(msgs[lang]["stats"].format(
                        stats["total_combinations"],
                        stats["average_length"],
                        stats["estimated_size_kb"]
                    ))
                except ValueError:
                    print("\033[31mErreur: Veuillez entrer un nombre valide.\033[0m" if lang == "FR"
                          else "\033[31mError: Please enter a valid number.\033[0m")
            else:  # Simple or Advanced Mode
                advanced_mode = mode_choice == "2"
                
                print("\n\033[36m[ Keywords ]\033[0m")
                while True:
                    keyword = input(msgs[lang]["keyword_prompt"])
                    if keyword.lower() == 'q':
                        break
                    generator.add_keyword(keyword)
                
                print("\n\033[36m[ Numbers ]\033[0m")
                while True:
                    number = input(msgs[lang]["number_prompt"])
                    if number.lower() == 'q':
                        break
                    generator.add_number(number)
                
                print("\n\033[36m[ Special Characters ]\033[0m")
                while True:
                    char = input(msgs[lang]["special_prompt"])
                    if char.lower() == 'q':
                        break
                    generator.add_special_char(char)
                
                print("\n\033[36m[ Configuration ]\033[0m")
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
                
                try:
                    max_comb = int(input(msgs[lang]["max_combinations"]))
                    generator.max_combinations = max_comb
                except ValueError:
                    pass
                
                print(msgs[lang]["generating"])
                wordlist = generator.generate_wordlist(advanced_mode)
                filename, stats = generator.save_wordlist(wordlist, preview=True)
                print(f"{msgs[lang]['saved']}{filename}")
                print(msgs[lang]["stats"].format(
                    stats["total_combinations"],
                    stats["average_length"],
                    stats["estimated_size_kb"]
                ))
            
            input("\n\033[32mAppuyez sur Entrée pour continuer...\033[0m")
            
        elif choice == "2":
            # Import and merge wordlists
            clear_screen()
            print_banner()
            
            # Show available files
            files = generator.get_source_files()
            print(f"\n{msgs[lang]['import_prompt']}")
            if files:
                for i, file in enumerate(files, 1):
                    print(f"{i}. {file}")
                try:
                    file_choice = int(input(f"\n{msgs[lang]['import_select']}"))
                    if 0 < file_choice <= len(files):
                        generator.import_wordlist(files[file_choice - 1])
                except ValueError:
                    pass
            else:
                print("\033[33mAucun fichier trouvé dans le dossier source.\033[0m" if lang == "FR"
                      else "\033[33mNo files found in source directory.\033[0m")
            
            input("\n\033[32mAppuyez sur Entrée pour continuer...\033[0m")
            
        elif choice == "3":
            # View statistics
            clear_screen()
            print_banner()
            print("\n\033[36m[ Current Statistics ]\033[0m")
            print(f"Keywords: {len(generator.keywords)}")
            print(f"Numbers: {len(generator.numbers)}")
            print(f"Special chars: {len(generator.special_chars)}")
            print(f"\nSource files: {len(generator.get_source_files())}")
            input("\n\033[32mAppuyez sur Entrée pour continuer...\033[0m")
            
        elif choice == "4":
            # Quit
            clear_screen()
            print_banner()
            print("\n\033[32mMerci d'avoir utilisé LexGen!\033[0m" if lang == "FR" 
                  else "\n\033[32mThank you for using LexGen!\033[0m")
            time.sleep(1)
            clear_screen()
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
    except Exception as e:
        print(f"\n\033[31mAn error occurred: {str(e)}\033[0m")


