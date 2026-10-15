"""Resumen extractivo con NLTK para reducir el tiempo de lectura."""
from collections import Counter
import re
from nltk.tokenize import PunktSentenceTokenizer, wordpunct_tokenize

STOP = set('a al algo ante bajo como con contra cual cuando de del desde donde el ella ellas ellos en entre era es esa ese eso esta este esto fue ha hasta hay la las le les lo los más me mi muy no nos o para pero por porque que qué se ser si sin sobre son su sus también te tu un una unas uno unos y ya'.split())

def summarization(text, n=2):
    """Devuelve hasta n frases importantes, conservando el orden original."""
    if not isinstance(text, str):
        raise TypeError('El texto debe ser una cadena')
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('El número de frases debe ser un entero positivo')
    sentences = PunktSentenceTokenizer().tokenize(text.strip())
    if not sentences:
        return ''
    def tokens(sentence):
        return [w.casefold() for w in wordpunct_tokenize(sentence) if w.isalpha() and w.casefold() not in STOP]
    frequencies = Counter(tokens(text))
    scores = [(i, sum(frequencies[w] for w in tokens(s)) / max(1, len(tokens(s)))) for i, s in enumerate(sentences)]
    selected = sorted(i for i, _ in sorted(scores, key=lambda pair: (-pair[1], pair[0]))[:n])
    return ' '.join(sentences[i] for i in selected)

def resumen_publicable(text, max_words=25):
    """Limita el extracto compartido; el texto íntegro no se almacena."""
    words = summarization(text, 1).split()
    return ' '.join(words[:max_words]) + ('…' if len(words) > max_words else '')

def main():
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archivo', type=Path)
    parser.add_argument('--frases', type=int, default=2)
    parser.add_argument('--salida', type=Path, default=Path('resumen.txt'))
    args = parser.parse_args()
    result = summarization(args.archivo.read_text(encoding='utf-8'), args.frases)
    args.salida.write_text(result, encoding='utf-8')
    print(result or 'El archivo no contiene texto para resumir.')

if __name__ == '__main__':
    main()
