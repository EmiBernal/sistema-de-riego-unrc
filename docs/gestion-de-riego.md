**GESTIÓN DE RIEGO**

**En este documento podemos plasmar ideas y funcionalidades que tendrá un futuro módulo para la gestión del riego en las vecinales…por cada punto a incorporar sugerimos que hagan una descripción inicial en un lenguaje natural y lo más detallado posible.** 

**Roles:** 3 tipos diferentes. 

**SUPER ADMINISTRADORES**   
CRUD: Registro de regadores

- Información personal 

CRUD: Registro de camiones

- patente

Sección Recorridos   
Recorridos quien lo define (? Dependiendo los caminos cortos se definira el recorrido optimo (?

Sección Estadísticas (?  
\-\> calificar recorrido (verde, amarillo, rojo) \- advertencia cuando es rojo

**USUARIOS REGADORES**

Sección Recorridos   
Sugerencias de recorridos: única óptima   
Registro de calle que se van recorriendo (pintando) \- hora 

(Todos los choferes para vista de los administradores municipal )  
(Solo recorridos propios de cada chofer para usuarios regadores)  
Historial de recorrido:   
\-\> tiempo recorrido   
\-\> recorrido dado  
\-\> calles faltantes   
\-\> chofer \- camion (X)  
\-\> Gestion de choferes y camiones

**USUARIOS COMUNES**  
Sección Vista General

- Recorrido en vivo  
- Portal de quejas (?  
- Horario de riego (?  
- 

**Preguntas:**  
¿ Único punto de entrada para el inicio de recorrido?   
¿ Qué datos necesitan los camiones y regadores?  
¿ Vecinales ya delimitadas, o nosotros hacemos?  
¿ A qué funciones pueden acceder cada tipo de usuario ?  
¿ Qué información tiene la API?  
¿ Los camiones se comparten entre vecinales?

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## **Vecinales y recorridos**

1. ¿Las vecinales ya tienen sus límites y calles definidos?

Sí, están definidas.

* Las vecinales se encuentran delimitadas en un mapa.  
* Cada vecinal tiene un **ejido**, es decir, un límite de calles definido.  
* Se utiliza un sistema de GPS que permite trabajar con **geocercas**.

Una geocerca es un perímetro virtual trazado sobre un mapa digital que utiliza tecnología GPS o satelital para enviar alertas automáticas cuando un dispositivo o vehículo ingresa o sale de esa zona

* Se cuenta con acceso al sistema de GPS.  
* La información de las vecinales también puede buscarse en la página del Gobierno/Municipalidad.  
* Tienen una API y un superusuario

---

2. ¿Todas las calles dentro de una vecinal deben ser regadas o existen calles que quedan excluidas?

No todas las calles deben ser regadas.

* Se excluyen las **calles pavimentadas**.  
* Por defecto, se riegan las **calles de tierra**.

---

3. ¿Hay calles o sectores que tengan mayor prioridad o frecuencia de riego que otros?

Sí.

* Las calles normales deben tener una frecuencia de riego de **2 veces**.  
* Las calles por donde circula el **colectivo** deben tener una frecuencia de **3 veces**.

---

## **Regadores y camiones**

4. ¿Cómo se determina actualmente qué recorrido debe realizar un regador?

Por defecto se deben cubrir todas las **calles de tierra** y pasajes correspondientes.

Existen algunas situaciones particulares que pueden modificar el recorrido, por ejemplo:

* Pasajes o sectores de difícil acceso.  
* Problemas o amenazas de vecinos que pueden provocar que el regador evite pasar por determinadas calles.

---

5. ¿El regador recibe un recorrido previamente definido o decide el camino a medida que realiza el trabajo?

Los regadores:

* Conocen las calles de la zona.  
* No necesariamente siguen un recorrido fijo.  
* Van adaptando el recorrido a medida que realizan el trabajo. Tambien se basan en si necesitan mas agua, si necesitan cargar, etc. Es variable

---

6. ¿Qué sería un “recorrido óptimo”?

El objetivo principal **no es hacer el recorrido en el menor tiempo posible**.

Un recorrido correcto debe:

* Cubrir todas las calles designadas.  
* Realizar el riego con la frecuencia correspondiente.  
* En condiciones normales, cada calle debe ser recorrida **2 veces**.

Que un regador tarde menos tiempo no significa necesariamente que sea más eficiente. Incluso podría significar que está realizando incorrectamente el trabajo.

Por lo tanto, la eficiencia debe medirse principalmente en función de la **calidad y cumplimiento del trabajo realizado**, y no solamente por el tiempo utilizado.

**Dato adicional:**

* Los camiones trabajan aproximadamente a una velocidad de **15 km/h**.

---

7. ¿Existe un único punto de inicio para los recorridos? ¿También existe un punto de finalización?

No.

* Los recorridos pueden comenzar y terminar en distintos lugares.  
* No existe un punto fijo de inicio o finalización.  
* Lo importante es controlar la **cantidad de horas que el vehículo se encuentra en movimiento/trabajando**.  
* El punto de inicio y finalización puede variar completamente entre recorridos.

---

8. Si durante el recorrido una calle no puede ser regada, ¿cómo se procede actualmente?

La calle **no se riega**.

---

9. ¿Los camiones pertenecen a una vecinal o se comparten entre ellas?

La distribución no necesariamente es de un camión por vecinal.

* Actualmente existen aproximadamente **15 vecinales**.  
* Hay casos en los que una vecinal puede disponer de varios camiones.  
* Por ejemplo, una de las vecinales cuenta con **3 camiones**.

A MI NO ME QUEDO MUY CLARO ESTO PORQUE CUANDO VOLVIO A EXPLICAR DIJO LOS NUMEROS AL REVES

---

10. ¿Un regador tiene siempre asignado el mismo camión o esto puede cambiar?

La organización se realiza principalmente según las zonas de trabajo.

* Un regador trabaja sobre un **grupo de calles**.  
* Ese grupo de calles puede abarcar **una o dos vecinales**.

> Queda pendiente definir con mayor precisión si el regador mantiene siempre el mismo camión o si el vehículo puede cambiar.

---

11. ¿Qué información consideran importante registrar de los regadores y de los camiones?

#### **Información del regador**

* Nombre.  
* Apellido.  
* DNI.  
* Carnet/licencia de conducir con foto.  
* Información relacionada con el seguro correspondiente.

#### **Información del camión**

* Patente.  
* VTV.  
* Estado de las luces.  
* Estado de los frenos.  
* Estado de la dirección.  
* Seguro.  
* Póliza.  
* Condición mecánica general.

---

## **3\. Control del trabajo**

12. ¿Qué información necesitan conocer sobre un recorrido una vez realizado?

Uno de los principales objetivos es saber si se logró regar correctamente todo el barrio con la frecuencia establecida.

Se plantean al menos dos variables principales:

#### **Primera variable**

Porcentaje de calles que fueron regadas **al menos una vez**.

#### **Segunda variable**

Porcentaje de calles que fueron regadas **dos veces**.  
 El control debería expresarse mediante **porcentajes de cumplimiento**.  
 El **100 % de cumplimiento** representaría que todas las calles correspondientes fueron regadas las **2 veces requeridas**.

---

### **Indicadores necesarios**

El sistema debería permitir consultar el porcentaje de cumplimiento:

* Por **regador**.  
* Por **camión**.  
* Por **día**.  
* Por **semana**.  
* Por **mes**.

---

### **Control de camiones**

El sistema debería permitir:

* **Habilitar** un camión.  
* **Deshabilitar** un camión temporalmente.

Esto sería necesario, por ejemplo, cuando un vehículo se encuentre:

* En reparación.  
* Fuera de servicio.  
* No disponible temporalmente.

La deshabilitación debería poder manejarse durante un período determinado para mejorar el control de disponibilidad de la flota.

Cuando se deshabilite un vehículo, se guarda la fecha, empieza un contador y una descripción del pq se deshabilita

---

13. ¿Qué situaciones consideran problemáticas y les gustaría que el sistema permitiera detectar?

Entre las situaciones a contemplar se encuentran:

* Camiones fuera de servicio.  
* Camiones en reparación.  
* Días en los que no es posible realizar normalmente el riego.  
* Días de lluvia.  
* El sistema debería contar con un **contador o registro de días**.

#### **Días de lluvia**

Cuando llueve:

* El día debe quedar registrado como **día de lluvia**.  
* Ese día debería contabilizarse como **día trabajado/cumplido**, aunque no se haya realizado el recorrido normal de riego.

---

## **4\. Usuarios comunes / vecinos**

14. ¿Quieren incorporar un portal de reclamos o quejas? En caso afirmativo, ¿quién gestionaría esos reclamos?

La funcionalidad podría ser útil, pero requiere mayor análisis.

Se considera una característica interesante, aunque también existe preocupación respecto a que pueda generar inconvenientes o tener un impacto político negativo.

> La funcionalidad debe analizarse con mayor profundidad antes de decidir si se incorpora.

---

### **Información posible para identificar al vecino**

En caso de implementarse un sistema de reclamos, podría solicitarse:

* Nombre.  
* Apellido.  
* Dni.  
* Dirección.  
* Telefono.

---

## **5\. GPS y geolocalización**

El sistema actual de GPS podría ser una fuente importante de información para el nuevo sistema.

Se mencionó la posibilidad de utilizar una **API** asociada al sistema de GPS.

Datos a investigar:

* Acceso mediante API.  
* Cuenta necesaria para utilizar el GPS.  
* Uso de **geocercas**.  
* Posibilidad de obtener posición y recorridos de los camiones.

> Se cuenta actualmente con acceso al sistema de GPS, pero es necesario investigar técnicamente qué información puede obtenerse y de qué manera integrarla con el nuevo sistema.

---

## **6\. Información adicional registrada**

Se mencionaron las siguientes referencias durante la reunión:

* GPS.  
* Geocercas.  
* `RGB 180`. //Nombre clave para uno de los camiones regadores  
* `LA AGUSTINA`. //Vecinal

