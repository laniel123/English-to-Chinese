import os
from pathlib import Path

# Pinyin tone mark mapping
tone_marks = {
    'a': ['ā', 'á', 'ǎ', 'à'],
    'e': ['ē', 'é', 'ě', 'è'],
    'i': ['ī', 'í', 'ǐ', 'ì'],
    'o': ['ō', 'ó', 'ǒ', 'ò'],
    'u': ['ū', 'ú', 'ǔ', 'ù'],
    'ü': ['ǖ', 'ǘ', 'ǚ', 'ǜ']
}

def convert_pinyin(pinyin):
    def mark_syllable(syl):
        if syl[-1] not in '12345':
            return syl  # no tone number
        tone = int(syl[-1]) - 1
        syl_base = syl[:-1]
        for vowel in 'a e o i u ü'.split():
            if vowel in syl_base:
                return syl_base.replace(vowel, tone_marks[vowel][tone])
        return syl  # fallback if no vowel found
    return ' '.join(mark_syllable(s) for s in pinyin.split())

def load_dictionary():
    dict_path = Path(__file__).resolve().parent.parent / "data" / "cedict_ts.u8"
    dictionary = {}

    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                continue
            try:
                traditional, simplified, rest = line.strip().split(' ', 2)
                pinyin_start = rest.find('[')
                pinyin_end = rest.find(']')
                pinyin = rest[pinyin_start + 1:pinyin_end]
                english_defs = [d.strip().lower() for d in rest[pinyin_end+1:].split('/') if d.strip()]
                for definition in english_defs:
                    if definition not in dictionary:
                        dictionary[definition] = (simplified, pinyin)
            except:
                continue
    return dictionary

cedict = load_dictionary()

def translate_to_chinese(word):
    word = word.strip().lower()

    # 1. Try exact dictionary key match
    if word in cedict:
        hanzi, raw_pinyin = cedict[word]
        return hanzi, convert_pinyin(raw_pinyin)

    # 2. Try match ignoring parentheses
    cleaned_dict = {key.split('(')[0].strip(): val for key, val in cedict.items()}
    if word in cleaned_dict:
        hanzi, raw_pinyin = cleaned_dict[word]
        return hanzi, convert_pinyin(raw_pinyin)

    # 3. Fuzzy fallback (exact word match inside phrases)
    matches = []
    for key in cedict:
        if word in key.split():
            matches.append((key, cedict[key]))

    matches.sort(key=lambda x: len(x[0]))
    if matches:
        hanzi, raw_pinyin = matches[0][1]
        return hanzi, convert_pinyin(raw_pinyin)

    return 'N/A', 'N/A'