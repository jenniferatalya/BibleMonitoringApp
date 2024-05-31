import re
import csv
import warnings
import pandas as pd
from utils import TO_BE_CHANGED, APP_DICTIONARY, BOOKNAMES, ABBREVIATIONS, EXPANSION, BIBLE_CHAPTERS
from unidecode import unidecode
from jaro import jaro_winkler_metric
warnings.filterwarnings("ignore")

class Parser:
    def __init__(self):
        self.to_be_changed = TO_BE_CHANGED
        self.app_dictionary = APP_DICTIONARY
        self.booknames = BOOKNAMES
        self.abbreviations = ABBREVIATIONS
        self.expansion = EXPANSION
        self.bible_chapters = BIBLE_CHAPTERS

    def remove_colon_number(self, text):
        pattern = r"\s*:\s*\d+"
        return re.sub(pattern, "", text)

    def remove_diacritics(self, text):
        cleaned_text = unidecode(' '.join(text.split()))
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s-]', '', cleaned_text)
        return cleaned_text

    def add_space_between_number_and_alphabet(self, text):
        pattern = r'(\d)([a-zA-Z])|([a-zA-Z])(\d)'
        result = re.sub(pattern, r'\1\3 \2\4', text)
        return result

    def fix_numbers(self, text):
        text = text.strip()
        pattern = r'\b0+(\d+)\b'
        result = re.sub(pattern, lambda x: x.group(1), text)
        return result

    def remove_single_alphabets(self, text):
        # Use regular expression to find single alphabets
        pattern = r'\b[a-zA-Z]\b'
        # Replace single alphabets with empty string
        return re.sub(pattern, '', text)

    def jaro_function(self, bookname_input, booknames):
        max_score = 0.75
        current_bookname = bookname_input

        for bookname in booknames:
            similarity_score = jaro_winkler_metric(bookname_input, bookname)
            if similarity_score > max_score:
                max_score = similarity_score
                current_bookname = bookname

        return current_bookname

    def fix_typo(self, text, app_dictionary):
        text = text.replace('--', '-').replace('-', ' - ').replace(',', ' ').replace('I ', '1 ').replace('II ', '2 ').replace('III ', '3 ').replace('  ', ' ')
        text = text.lower().replace('hakim2', 'hakim').replace('raja2', 'raja')
        text = self.remove_colon_number(text)
        text = self.remove_diacritics(text)
        text = self.add_space_between_number_and_alphabet(text)
        text = self.fix_numbers(text)
        text = self.remove_single_alphabets(text)
        text_list = text.split(" ")
        result = list()

        for word in text_list:
            current = self.jaro_function(word, app_dictionary)
            if current != word:
                pass
            else:
                if current in app_dictionary:
                    pass
                else:
                    for word2 in app_dictionary:
                        if word2 in word:
                            current = word2
                            break
                        else:
                            continue
            result.append(current)

        return ' '.join(result)

    def remove_space_in_bookname(self, text):
        text = text.lower()
        for before, after in self.to_be_changed:
            text = text.replace(before, after)
        return text

    def clean_report(self, text, booknames):
        text_list = text.split()
        new_value = list()

        for word in text_list:
            if word in booknames or word.isdigit() or word == '-':
                new_value.append(word)

        for i, word in enumerate(new_value):
            if word == 'kisah':
                if i + 1 < len(new_value) and new_value[i+1] in booknames:
                    new_value[i] = ''

        return ' '.join(new_value).strip()

    def change_abbreviation(self, text, abbreviation, booknames):
        text_list = text.split()

        for i, word in enumerate(text_list):
            if word in abbreviation:
                new_word = booknames[abbreviation.index(word)]
                text_list[i] = new_word
            else:
                continue
        result = ' '.join(text_list).strip()
        return result.replace(' - ', '-')

    def expand_chapter_range(self, input_str):
        parts = str(input_str).split()
        if len(parts) > 2:
            book = parts[0] + " " + parts[1]
            chapters = parts[2].split('-')
        elif len(parts) < 2:
            return input_str
        else:
            book = parts[0]
            chapters = parts[1].split('-')

        if len(chapters) == 1:
            return input_str

        start_chapter = chapters[0]
        end_chapter = chapters[1]
        output = f"{book} {start_chapter} - {book} {end_chapter}"
        return re.sub(r'(\d+)-(\w+)', r'\1 - \2', output)

    def parse_messages(self, text, chapters, booknames):
        parsed_text = ""

        if len(text.split()) == 1:
            if all(book in booknames for book in text.split('-')):
                parsed_line = ''
                parsed_books = text.split('-')
                for book in parsed_books:
                    for chapter in chapters:
                        if chapter.startswith(book):
                            parsed_line += f"{chapter}, "
                parsed_text = parsed_line[:-2]
            else:
                parsed_line = ''
                for chapter in chapters:
                    if text in chapter:
                        parsed_line += f"{chapter}, "
                parsed_text = parsed_line[:-2]

        else:
            matches = re.findall(r'(\w+\s\d+)(?:\s*-\s*(\w+\s\d+))?', text)
            parsed_line = ''
            for match in matches:
                start_event, end_event = match[0], match[1]

                start_index = chapters.index(start_event.lower()) if start_event.lower() in chapters else None
                end_index = chapters.index(end_event.lower()) if end_event and end_event.lower() in chapters else start_index
                if start_index is not None and end_index is not None:
                    for i in range(start_index, end_index + 1):
                        parsed_line += f"{chapters[i]}, "
            parsed_text = parsed_line[:-2]

        return parsed_text

    def fix_parsing_spaces(self, text):
        return text.replace('hakimhakim', 'hakim-hakim').replace('1samuel', '1 samuel').replace('2samuel', '2 samuel').replace('1rajaraja', '1 raja-raja').replace('2rajaraja', '2 raja-raja').replace('1tawarikh', '1 tawarikh').replace('2tawarikh', '2 tawarikh').replace('kidungagung', 'kidung agung').replace('kisahpararasul', 'kisah para rasul').replace('1korintus', '1 korintus').replace('2korintus', '2 korintus').replace('1tesalonika', '1 tesalonika').replace('2tesalonika', '2 tesalonika').replace('1timotius', '1 timotius').replace('2timotius', '2 timotius').replace('1petrus', '1 petrus').replace('2petrus', '2 petrus').replace('3petrus', '3 petrus').replace('1yohanes', '1 yohanes').replace('2yohanes', '2 yohanes').replace('3yohanes', '3 yohanes')

    def run(self, text):
        text = self.fix_typo(text, self.app_dictionary)
        text = self.remove_space_in_bookname(text)
        text = self.clean_report(text, self.booknames)
        text = self.change_abbreviation(text, self.abbreviations, self.expansion)
        text = self.expand_chapter_range(text)
        text = self.parse_messages(text, self.bible_chapters, self.expansion)
        text = self.fix_parsing_spaces(text)
        return text

if __name__ == "__main__":
    parser = Parser()
    text_to_parse = "yos 34-hak 1 done"
    output = parser.run(text_to_parse)