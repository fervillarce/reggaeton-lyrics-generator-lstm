# reggaeton-lyrics-generator-lstm


## Goal

El objetivo de este proyecto es generar canciones de reggaeton con una red neuronal recurrente (RNN), concretamente con LSTM (Long Short-Term Memory).
Este trabajo corresponde al proyecto de fin de bootcamp de Data Analytics, cursado en Ironhack durante 2019.

La presentación está disponible en este repositorio, en el archivo 20191026_Proyecto_IH.pdf.


## Files

### Input

Solo contiene el archivo **lyrics.txt**. Este archivo contiene todas las canciones de reggaeton de la web www.letras.com de aquellos artistas que tienen más de 20 canciones. Está en bruto, pero se ha hecho una limpieza posterior al scraping para eliminar canciones que estuvieran en cualquier otro idioma diferente al español. No obstante, puede quede alguna traza, debido a la complejidad de la tarea.


### Output

Son los archivos resultantes de la ejecución del pipeline main.py.
* **examples_file.txt**. Contiene las generaciones de las letras en cada uno de los epochs y para cada valor de diversity (temperature).
* **model.h5**. Es la exportación del modelo tras su entrenamiento (40 epochs).


### Source

Son los archivos necesarios para ejecutar el pipeline. Cada uno de los archivos contiene funciones en su mayoría documentadas.
* **main.ipynb**. Ejecuta el pipeline relacionado con la generación del modelo (model.h5) y las lyrics (examples_file.txt).
* **main_colab.ipynb**. Hace lo mismo que main.ipynb, pero el código está adaptado para correrlo en Google Colab.
* **object_manager.ipynb**. Contiene funciones para exportar e importar en un .pickle.
* **nicky.py** _(este archivo se encuentra actualmente bajo testeo)_. La función nicky.predict recibe una frase de reggaeton y el modelo devuelve otra frase generada de máximo 8 palabras.
* **reggaeton_app.py** _(este archivo se encuentra actualmente bajo testeo)_. Ejecuta una aplicación web que permite la ejecución de nicky.py en una GUI (Streamlit). Para ello, antes es necesario instalar streamlit y ejecutar el siguiente comando `$ streamlit run reggaeton_app.py` en la línea de comandos.
* **scraper.py**. Hace web scraping de todas las canciones de reggaeton de aquellos artistas que tengan más de 20 canciones en www.letras.com. El output de este scraping es el archivo lyrics.txt en bruto, que será limpiado y dispuesto en la carpeta _Input_ de cara al entrenamiento del modelo.


### Checkpoints

Contiene todos los checkpoints del último modelo. Hay tantos checkpoints como epochs tiene el modelo.


### obj

Contiene los siguientes tres archivos en formato pickel, que han sido exportados durante el pipeline:
* **char_indices_dict.pkl**. Diccionario con la relación numérica de los 45 chars únicos en las lyrics.
* **indices_char_dict.pkl**. Diccionario con la misma relación pero con las keys y values invertidos.
* **chars_list.pkl**. Lista con todos los chars únicos de las lyrics.


## A few tips before we begin

El código contenido en el archivo main.ipynb sigue las pautas recomendadas en la documentación de Keras sobre Text Generation. Estas son las recomendaciones:
* At least 20 epochs are required before the generated text starts sounding coherent.
* It is recommended to run this script on GPU, as recurrent networks are quite computationally intensive.
* If you try this script on new data, make sure your corpus has at least ~100k characters. ~1M is better.

Los resultados de este proyecto se han obtenido bajo las siguientes directrices:
* 40 epochs.
* Se ha corrido tanto en CPU como en GPU (Google Colab). La experiencia de Google Colab ha resultado ser más satisfactoria.
* A pesar de disponer de un corpus con más de 15 millones de caracteres, se han utilizado solo 3 millones de caracteres para acelerar el proceso de entrenamiento del modelo.


## Pipeline description

A continuación, se describen cada una de las funciones principales del pipeline, siguiendo una estructura ETL. Algunas de estas funciones, a su vez, pueden llamar a archivos anteriormente descritos.


### Importación del dataset (función *get_text*)

Recibe el archivo lyrics.txt y devuelve una string con todo su contenido.


### Limpieza (función *clean_text*)

Esta función limpia los datos de la string y los deja limpios para su análisis.
La limpieza consiste en:
* Eliminar **etiquetas de html** y añadir saltos de línea al final de los versos.
* Eliminar cualquier string contenida dentro de paréntesis, corchetes o llaves, incluídos los propios paréntesis, corchetes o llaves.
* Eliminar **caracteres extraños**. En este aspecto, para facilitar el entrenamiento, se han considerado caracteres extraños a aquellos diferentes a vocales, consonantes, números, coma y punto.
* Consolidar un criterio para las **tildes** en aquellas vocales con tildes diferentes a la aguda (´).


### Análisis (función *string_analysis*)

Imprime el siguiente resumen del corpus:
* Corpus length in characters
* Corpus length in words
* Unique chars

Además exporta el archivo chars_list.pkl.


###  Creación de diccionarios char-indices (función *char_dictionaries*)

Crea y exporta a la carpeta _obj_ los siguientes diccionarios:
* **char_indices_dict.pkl**
* **indices_char_dict.pkl**

Estos diccionarios serán necesarios en las funciones _vectorize_ y _on_epoch_end_ de cara a la vectorización y "desvectorización" de X, y.


### Creción del dataset (función *cut_text*)

Recibe el texto (lyrics) limpio, y lo transforma, devolviendo en dos variables:
* **sentences**. Lista de secuencias (strings) de 40 caracteres que se va formando con un step de 3 caracteres a lo largo de todo el texto.
* **next_chars**. Lista con cada uno de los caracteres que siguen a cada una de las secuencias anteriores.


### Vectorización del dataset (función *vectorize*)

Genera X e y (vectores) a partir de sentences y next_chars (listas de strings).
* **X** es un array booleano con 3 dimensiones: posición de sentence, posición del char, nº equivalente al char.
* **y** es un array booleano con 2 dimensiones: posición de sentence, nº equivalente al char.


### Definición y construcción del modelo (función *build_model*)

Estas son las diferentes funciones:
* **Definir el modelo** (Sequential)
* Definir el **input layer**
* Añadir el **hidden layer** (LSTM)
* Añadir el **output layer** (Dense)
* **Compilar** el modelo con el tipo de pérdida, optimizador y métrica a evaluar


### Obtención del valor más probable (función *sample*)

Recibe las predicciones y devuelve el valor más probable.


### Generación de canciones (función *on_epoch_end*)

Imprime el texto generado. Esta función se invoca al final de cada epoch.


### Función principal (función *main*)

La función main es la directora de orquesta. Va llamando a cada una de las funciones anteriores y al final realiza las siguientes funciones:
* **Entrena** el modelo
* Genera los **checkpoints** para cada epoch
* **Guarda el modelo** una vez terminado el último epoch
* Imprime un **resumen del modelo**


## Conclusiones


### Resultados

Los resultados son la generación de nuevas canciones de reggaeton a partir de una frase semilla y de las propias predicciones del modelo. Estos resultados están disponibles en el archivo examples_file.txt de la carpeta Output.

Como el modelo se ha entrenado con 40 epochs, se han obtenido 40 predicciones diferentes, en cada una de ellas con 4 temperatures diferentes. La temperature es el hiperparámetro de LSTM que controla la aleatoriedad de las predicciones. Se puede apreciar que a valores más grandes de temperature, los resultados son peores.

Los resultados son relativamente satisfactorios teniendo en cuenta los parámetros seleccionados. Los resultados son mejores en los epochs finales, pero aún siguen sacando algunas frases sin sentido. Un entrenamiento con más epochs, obtendrá mejores resultados.

Asimismo, se han introducido en el modelo 3 millones de caracteres. No se han podido introducir los más de los 15 millones disponibles porque no disponía de tiempo suficiente para el correspondiente entrenamiento. Con los parámetros asignados, el tiempo de computación en la GPU han sido de unas 10 horas.


### Problemas encontrados

Dado el alto coste computacional, he necesitado correr el script en Google Colab, conectándome a una GPU. La experiencia ha sido satisfactoria, aunque Colab no permite estar conectado a una misma GPU más de 12 horas seguidas.

He tenido que instalar una app (Amphetamine) para evitar el cierre de sesión del ordenador e introducir el siguiente código en la consola del inspector del navegador para mantener la página activa mediante clicks automáticos:
```
function ClickConnect(){console.log("Working");document.querySelector("colab-toolbar-button#connect").click()}setInterval(ClickConnect,60000)
```


## Next steps

* Entenar el modelo con epochs > 100
* Entrenar el modelo con corpus > 15M caracteres
* Entrenar el modelo con valores del hiperparámetro temperature más pequeños (0.3, 0.4…)
* Plantear el proyecto para la generación de palabras en lugar de caracteres
* Verificar la GUI utilizada (Streamlit) y probar alguna alternativa (Tkinter) en caso necesario
* Añadir audio y ritmo para reproducir las letras como canción



## Cómo ejecutar el proyecto


### Librerías

En el proyecto se usan las siguientes librerías, que habrá que instalar antes de ejecutar el archivo principal:
* numpy
* keras
* pickle
Estas librerías se pueden instalar directamente mediante el siguiente comando en la línea de comandos:
`$ pip install -r requirements.txt`


### Archivos

En caso de querer ejecutarlo en local porque se dispone de una GPU, descargar todos los archivos en la misma carpeta y ejecutar el archivo main.ipynb. Si no se dispone de una GPU, se puede subir el archivo main_colab.ipynb a Google Colab, y conectarse a una GPU de forma gratuita.





