La demostración matemática del cálculo de la **matriz de varianzas y covarianzas** ($\text{Var}(\hat{\beta})$) del estimador de Mínimos Cuadrados Ordinarios (MCO), $\hat{\beta}$, se desarrolla en varios pasos. Esta matriz es de tamaño $k \times k$, donde $k$ es el número de coeficientes beta. Los elementos de la diagonal son las varianzas de cada coeficiente ($\beta_1$ hasta $\beta_k$), y los elementos fuera de la diagonal son las covarianzas entre los diferentes coeficientes.

El cálculo de $\text{Var}(\hat{\beta})$ requiere primero demostrar que $\hat{\beta}$ es un estimador insesgado (Paso 1) y entender la matriz de varianza de los errores (Paso 2), para luego proceder al cálculo final (Paso 3).

---

### Paso 1: Demostrar que $\hat{\beta}$ es un estimador insesgado de $\beta$

Para demostrar que $\hat{\beta}$ es insesgado, debemos mostrar que su valor esperado es igual a $\beta$ ($\text{E}(\hat{\beta}) = \beta$).

1.  **Fórmula inicial del estimador $\hat{\beta}$**:
    $$\hat{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$

2.  **Sustitución del vector dependiente $\mathbf{y}$**:
    Se utiliza la relación del modelo $\mathbf{y} = \mathbf{X}\beta + \epsilon$ (donde $\epsilon$ es el término de error) y se sustituye $\mathbf{y}$ en la fórmula de $\hat{\beta}$:
    $$\hat{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T (\mathbf{X}\beta + \epsilon)$$

3.  **Distribución y simplificación**:
    Se distribuye el término $\mathbf{X}\beta + \epsilon$:
    $$\hat{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{X}\beta + (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon$$
    El término $(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{X}$ se simplifica. Aplicando la regla de que el inverso de una matriz multiplicado por la matriz original es la matriz identidad ($\mathbf{A}^{-1}\mathbf{A} = \mathbf{I}$), este término se vuelve la matriz identidad.
    Esto resulta en una expresión simplificada para $\hat{\beta}$:
    $$\hat{\beta} = \beta + (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon$$

4.  **Cálculo del valor esperado**:
    Se calcula el valor esperado de $\hat{\beta}$:
    $$\text{E}(\hat{\beta}) = \text{E}\left[\beta + (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon\right]$$
    Dado que $\beta$ es una constante, puede sacarse del valor esperado:
    $$\text{E}(\hat{\beta}) = \beta + \text{E}\left[(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon\right]$$

5.  **Aplicación del supuesto OLS**:
    Se utiliza el supuesto de los MCO que establece que el valor esperado de $\epsilon$ condicional en $\mathbf{X}$ es cero ($\text{E}(\epsilon | \mathbf{X}) = 0$). Esto implica que $\epsilon$ es independiente de $\mathbf{X}$.
    Debido a esta independencia, se puede separar el valor esperado de la multiplicación:
    $$\text{E}\left[(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon\right] = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T \text{E}(\epsilon)$$
    Dado que $\text{E}(\epsilon) = 0$, toda esta expresión se anula.
    **Conclusión del Paso 1**:
    $$\text{E}(\hat{\beta}) = \beta$$
    Se demuestra así que $\hat{\beta}$ es un estimador insesgado.

---

### Paso 2: Análisis de la matriz de varianza de los errores

La matriz de varianza de los errores ($\mathbf{\Sigma}$) es el valor esperado de $\epsilon\epsilon^T$:
$$\mathbf{\Sigma} = \text{E}(\epsilon \epsilon^T)$$

1.  **Estructura de la matriz**:
    $\epsilon$ es un vector de $n$ observaciones, por lo que $\text{E}(\epsilon \epsilon^T)$ es una matriz de tamaño $n \times n$. El valor esperado se aplica a cada elemento de la matriz.

2.  **Elementos fuera de la diagonal (Covarianzas)**:
    Los elementos fuera de la diagonal representan la covarianza entre $\epsilon_i$ y $\epsilon_j$ (donde $i \neq j$).
    Los supuestos de MCO incluyen que las observaciones son IID (independientes e idénticamente distribuidas). La **independencia** entre las observaciones implica que la covarianza entre los términos de error de diferentes observaciones es cero.
    Por lo tanto, todos los elementos fuera de la diagonal son cero.

3.  **Elementos en la diagonal (Varianzas)**:
    Los elementos en la diagonal representan el valor esperado de $\epsilon_i^2$.
    Se utiliza el supuesto de **homoscedasticidad** de MCO, que establece que la varianza de cualquier $\epsilon_i$ es igual a una constante $\sigma^2$. Es decir, $\text{E}(\epsilon_i^2) = \sigma^2$.

4.  **Resultado de la matriz de errores**:
    Dado que los elementos de la diagonal son $\sigma^2$ y los demás son cero, la matriz $\text{E}(\epsilon \epsilon^T)$ es igual a la matriz identidad ($\mathbf{I}$) multiplicada por $\sigma^2$:
    $$\mathbf{\Sigma} = \text{E}(\epsilon \epsilon^T) = \sigma^2 \mathbf{I}$$

---

### Paso 3: Cálculo de la matriz de varianza-covarianza de $\hat{\beta}$

La varianza de un vector de estimadores ($\hat{\beta}$) se define como:
$$\text{Var}(\hat{\beta}) = \text{E}\left[(\hat{\beta} - \text{E}(\hat{\beta}))(\hat{\beta} - \text{E}(\hat{\beta}))^T\right]$$

1.  **Sustitución del valor esperado**:
    Dado que $\hat{\beta}$ es insesgado (Paso 1), $\text{E}(\hat{\beta}) = \beta$:
    $$\text{Var}(\hat{\beta}) = \text{E}\left[(\hat{\beta} - \beta)(\hat{\beta} - \beta)^T\right]$$

2.  **Sustitución de la diferencia $\hat{\beta} - \beta$**:
    Según el resultado del Paso 1, la diferencia $\hat{\beta} - \beta$ es igual al término de ruido:
    $$\hat{\beta} - \beta = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon$$

3.  **Expresión de la Varianza**:
    Sustituyendo esta diferencia en la fórmula de la varianza:
    $$\text{Var}(\hat{\beta}) = \text{E}\left[\left((\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon\right) \left((\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon\right)^T\right]$$

4.  **Aplicación de la transposición (Traspuesta)**:
    Se aplica la regla de transposición de una multiplicación de matrices $(\mathbf{ABC})^T = \mathbf{C}^T\mathbf{B}^T\mathbf{A}^T$.
    El término traspuesto es:
    $$\left((\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\epsilon\right)^T = \epsilon^T (\mathbf{X}^T)^{T} ((\mathbf{X}^T\mathbf{X})^{-1})^{T}$$
    *   $\epsilon$ se convierte en $\epsilon^T$.
    *   $(\mathbf{X}^T)^T$ se convierte en $\mathbf{X}$ (una matriz transpuesta dos veces vuelve a la matriz inicial).
    *   $(\mathbf{X}^T\mathbf{X})^{-1})^T$ se convierte en $(\mathbf{X}^T\mathbf{X})^{-1}$, ya que la transposición de una inversa es igual a la inversa de la transpuesta, y $\mathbf{X}^T\mathbf{X}$ es simétrica.

    Sustituyendo esto de nuevo en la fórmula de la varianza:
    $$\text{Var}(\hat{\beta}) = \text{E}\left[(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T \epsilon \epsilon^T \mathbf{X} (\mathbf{X}^T\mathbf{X})^{-1}\right]$$

5.  **Separación del Valor Esperado**:
    Debido a la independencia entre el término de error $\epsilon$ y las variables explicativas $\mathbf{X}$, el valor esperado solo se aplica a la parte aleatoria ($\epsilon \epsilon^T$):
    $$\text{Var}(\hat{\beta}) = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T \left[\text{E}(\epsilon \epsilon^T)\right] \mathbf{X} (\mathbf{X}^T\mathbf{X})^{-1}$$

6.  **Sustitución del resultado del Paso 2**:
    Se sustituye $\text{E}(\epsilon \epsilon^T)$ por $\sigma^2 \mathbf{I}$ (el resultado de la homoscedasticidad):
    $$\text{Var}(\hat{\beta}) = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T [\sigma^2 \mathbf{I}] \mathbf{X} (\mathbf{X}^T\mathbf{X})^{-1}$$

7.  **Simplificación final**:
    Se saca la constante $\sigma^2$ (la varianza del término de error) al inicio y se elimina la matriz identidad $\mathbf{I}$:
    $$\text{Var}(\hat{\beta}) = \sigma^2 (\mathbf{X}^T\mathbf{X})^{-1} (\mathbf{X}^T \mathbf{X}) (\mathbf{X}^T\mathbf{X})^{-1}$$
    El término central $\mathbf{X}^T \mathbf{X} (\mathbf{X}^T\mathbf{X})^{-1}$ es igual a la matriz identidad $\mathbf{I}$.
    Finalmente, la **matriz de varianzas y covarianzas de $\hat{\beta}$** es:
    $$\text{Var}(\hat{\beta}) = \sigma^2 (\mathbf{X}^T\mathbf{X})^{-1}$$

### Uso práctico de la Matriz

Para aplicar esta fórmula en la práctica, $\sigma^2$ (la varianza de los errores) debe ser estimada, ya que es desconocida. Se utiliza un estimador $\hat{\sigma}^2$ (o $\sigma_{gorro}^2$) que es igual a la suma de los cuadrados de los residuos sobre los grados de libertad ($n-k$):
$$\hat{\sigma}^2 = \frac{\sum \text{residuo}_i^2}{n-k}$$

El resultado final $\text{Var}(\hat{\beta}) = \hat{\sigma}^2 (\mathbf{X}^T\mathbf{X})^{-1}$ es la matriz $k \times k$ que contiene las varianzas de $\hat{\beta}$ en la diagonal. La raíz cuadrada de estos elementos diagonales proporciona el **error estándar** de cada coeficiente, utilizado típicamente para las pruebas de significancia (pruebas $t$).