# THIS IS JUST A TEMPLATE

# cars-machine-learning-project


## Goal

El objetivo de este proyecto es predecir precios de coches de segunda mano.
El proyecto es parte de una competición de [Kaggle](https://www.kaggle.com/c/datamad0819-vehicles/).


## Files

### Input files

Son los archivos de train y test, descargados de Kaggle.
* cars_train_csv
* cars_test_csv


### Output files

Son los archivos resultantes de cada modelo, que hay que submitir en Kaggle.
Cada archivos tiene dos columnas: el índice único del coche y la predicción del precio.
* cars_submission_gradboost.csv
* cars_submission_kneigh.csv
* cars_submission_dectree.csv
* cars_submission_linreg.csv
* cars_submission_randfor.csv


### Source files

Son los archivos necesarios para ejecutar el pipeline. Cada uno de los archivos contiene funciones en su mayoría documentadas.
* **main.py**: ejecuta el pipeline.
* **extractor.py**: contiene funciones para importar.
* **explorer**: funciones para la exploración.
* **cleaner.py**: funciones de limpieza (eliminación de columnas irrelevantes y eliminación/edición de nulls).
* **transformer.py**: funciones de transformación de columnas.
* **spliter.py**: contiene la función para dividir el train en dos: X, y.
* **scaler.py**: funciones para rescalar.
* **dim_reductor.py**: funciones para reducir la dimensionalidad.
* **trainer.py**: algoritmos de entrenamiento y predicción.
* **loader.py**: funciones para exportar, ya sea a un json o a un csv.
* **main.ipynb**: lo he incluido por si se quiere probar con jupyter en lugar de con el .py.


## A few thoughts before we begin

El target de nuestro dataset de train es "price". Es decir, esta va a ser la variable dependiente. Dado que conocemos el target, el proyecto es de supervised learning.

Además, esta variable es numérica, por lo que tendremos que usar técnicas y modelos de regresión.


## Pipeline description

A continuación, se describen cada una de las funciones principales del pipeline, siguiendo una estructura ETL. Estas funciones, a su vez, llaman a los archivos anteriormente descritos.


### Importación de los datasets (función *extract*)

Se importan los archivos csv (train y test) como dataframes, para trabajar con ellos en las siguientes fases de exploración, análisis y manipulación de datos.


### Exploratorio (función *explore*)

Se hace el exploratorio de los datos. Este exploratorio consiste en:
* **ANOVA** de cada variable independiente (centrado sobre todo en las variables categóricas). Permite identificar cuáles de estas variables tienen máyor significancia estadística con la variable dependiente price. En definitiva, obtenemos aquellas variables cuyos valores en la muestra no son representativos en la población.
* Identificación y conteo de **nulls**.
* Representación de **correlaciones** y conclusiones.
* Boxplot con los valores de "price", para visualizar **outliers**. Nota: una futura mejora será aplicar la técnica del IQRx1.5, para identificar y descartar directamente los outliers existentes en cualquiera de las columnas numéricas.
* Nota: he incluido la función pass_to_bins para discretizar variables numéricas de cara a hacer ANOVA. Este ha sido el caso de "odometer", cuyo análisis no he incluido porque no era significativo. Categoricé "odometer" en 10 bins y concluí que igualmente no influía en el precio. No obstante, seria mejor aplicar **Jenks Natural Breaks**, ya que los cortes de clase agrupan mejor los valores similares y maximizan las diferencias entre clases.


### Limpieza (función *clean*)

Esta función limpia los datos del dataframe tras las conclusiones del exploratorio, y los deja listos para la posterior transformación.

Las funciones de limpieza son:
* **Eliminar columnas** que hemos establecido como irrelevantes.
* **Eliminar nulls** del train.
* **Modificar nulls** del test.


### Transformación (función *transform*)

Se llevan a cabo las siguientes transformaciones:
* Se pasa la variable **"cylinders"** de categorías a valores numéricos.
* Se hace **One Hot Encoding** de train y test, para crear tantas variables como categorías diferentes tienen las variables categóricas. Esto genera nuevas columnas con valores 0 o 1, que sustituyen a las variables categóricas.
* **Unificamos la dimensión** de train y test, cuando ambos dataframes tienen diferente número de columnas. Esto ocurre cuando, tras haber hecho One Hot Encoding, en un dataframe hay más columnas que el otro porque en una variable categórica había diferentes valores únicos.
* Nota: también está programada la transformación de **"manufacturer"**, para unificar valores, por ejemplo, unificar "chevrolet" y "chevy" en un único valor. Al final no se usa porque según el ANOVA, "manufacturer" no explica la variable "price".


###  División del train (función *train_split*)

Divide train en X_train, y_train.


### Rescalado (función *rescale*)

Se puede hacer alguno de estos dos tipos de rescalado:
* **StandardScaler**. Basado en: Z = (X - u) / s
* **MinMaxScaler**. Basado en: Z = (X - min(X)) / (max(X) - min(X))

Es recomendable rescalar las variables en las siguientes situaciones:
* Antes de aplicar PCA.
* De cara a algoritmos basados en distancia euclídea. Estos pueden ser K-Means, K-Neighbors...


### Reducción dimensional (función *reduce_dimension*)

Realiza un **PCA**.


### Entrenamiento y predicción (función *train_and_predict*)

Llama a los modelos y los aplica.
Modelos disponibles:
* sklearn.linear_model.**LinearRegression**
* sklearn.ensemble.**RandomForestRegressor**
* sklearn.tree.**DecisionTreeRegressor**
* sklearn.neighbors.**KNeighborsRegressor**
* sklearn.ensemble.**GradientBoostingRegressor**

### Exporación (función *load*)

Por último, prepara el archivo de submission (id, price) y exporta el dataframe en un archivo csv (sin index).


### Función principal (función *main*)

La función main es la directora de orquesta. Va llamando a cada una de las funciones anteriores. 


## Conclusiones


### Resultados

Los resultados son la predicción del modelo sobre el precio, es decir, y_pred.
Una vez hecha la submission, Kaggle evalúa el resultado en función del **mean squared error** resultante entre la predicción (y_pred) y la realidad.


### Problemas encontrados

Tanto los datasets de train como de test requieren muchas tareas de limpieza. Una de las conclusiones es que el modelo no repercute tanto como la limpieza exhaustiva a realizar, eliminación de outliers, y la elección correcta de variables.

Por tanto, en principio no existe mucha diferencia entre un modelo u otro, si no se realiza antes una buena limpieza. Es solo en ese caso cuando el rescalado y los modelos, funcionan mejor.


## Cómo ejecutar el proyecto


### Librerías

En el proyecto se usan las siguientes librerías, que habrá que instalar antes de ejecutar el archivo principal:
* pandas
* numpy
* sklearn
* statsmodels
* matplotlib


### Archivos

Descargar todos los archivos en la misma carpeta y ejecutar el archivo main.py (o main.ipynb).



## Next steps

* Identificar **outliers** mediante el rango intercuartil (IQR).
* Probar [selectKBest](https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectKBest.html#sklearn.feature_selection.SelectKBest) para feature selction en función de los K con mejoes scores.
* Aplicar **GridSearchCV** para RandomForestRegressor, y sacar el modelo más óptimo en función del estimador qu le indiquemos.
* ¿Conviene usar **RobustScaler** en lugar de los scalers que he usado?

