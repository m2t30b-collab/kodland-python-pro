# Lectura rápida con NLTK
Público objetivo propuesto: estudiantes que necesitan revisar textos extensos.
Hipótesis de necesidades (no una encuesta realizada): elegir longitud, usar archivos UTF-8 y guardar el resultado.

Uso: python resumidor.py texto.txt --frases 2 --salida resumen.txt
La función summarization(text, n) tokeniza frases y palabras, elimina palabras vacías, puntúa por frecuencia y conserva el orden original. No necesita modelos descargables.
Se probaron texto vacío, tipos incorrectos, longitud inválida, texto corto, acentos, orden y exportación. Los resúmenes son extractivos; conviene revisar el contexto.
