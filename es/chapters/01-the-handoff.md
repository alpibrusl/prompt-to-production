# El traspaso

> **Parte I — El terreno**

Describió lo que quería. Algo lo construyó. Funciona.

Está mirando una pantalla donde algo que imaginó está ocurriendo — un formulario que se envía, una lista que se ordena, una página que muestra sus datos colocados como usted pidió. Hace veinte minutos no existía. Hay una sensación particular en ese momento, y si la ha tenido sabe que ninguna descripción le hace justicia.

Llámelo Ledgerly, si ayuda ponerle nombre — una herramienta de facturación para autónomos, pongamos, construida igual que acaba de construir usted algo. Los ejemplos de este libro volverán a ella una y otra vez. Lo que viene a continuación es lo mismo sea lo que sea lo que usted haya construido.

Luego llega la segunda pregunta, y es mucho más difícil que la primera: *¿y ahora qué?*

Este libro trata de la distancia entre esos dos momentos. Es una distancia grande. Ahí es donde vive casi toda la disciplina real de la ingeniería de software, y casi nada de ella se ve en lo que acaba de construir. El agente se ha ocupado de la parte que parece el trabajo. Lo que le ha entregado es la parte que no parece nada.

## Lo que hay en su pantalla no es la cosa

Esta es la primera idea del libro y la más importante, y todo lo demás se deriva de ella.

Lo que el agente escribió es **código fuente**: texto que describe lo que un programa debería hacer. El código fuente es una receta. Son instrucciones, escritas, en una forma lo bastante precisa como para que una máquina pueda seguirlas. No es el plato.

Para pasar de la receta a algo que una persona pueda usar tiene que ocurrir una segunda cosa. El código fuente se convierte en un **programa** — algo que un ordenador puede ejecutar de verdad — mediante un proceso llamado ***build***. Cocinar la receta. Según el lenguaje que haya de por medio, esto puede tardar una fracción de segundo o varios minutos, y puede ser tan automático que usted nunca lo note. Pero ocurre, todas las veces.

Lo que sale de un build es un **artefacto**: un fichero o un paquete que se le puede entregar a una máquina para que lo ejecute — y una vez está ejecutándose se dice que está en **tiempo de ejecución**, el estado de un programa mientras corre de verdad en lugar de estar en disco como texto, que es donde ocurren casi todos los fallos interesantes de este libro. Y aquí viene la parte que a la gente le sorprende genuinamente la primera vez: *el artefacto es derivado, no escrito*. Usted no lo edita directamente, y no lo trata como la fuente de la verdad — los sistemas reales suelen guardar artefactos una temporada, en un registro, para un *rollback*, para una auditoría o para reproducir lo que estaba funcionando el martes pasado, y eso está bien. Lo que importa es que guardar uno es una comodidad, no una responsabilidad: si lo pierde, debería poder reproducir uno equivalente a partir de la fuente y de las entradas del build registradas. La receta es lo que se protege. El plato es fácil de volver a hacer.

Y por último, ese artefacto tiene que ponerse en algún sitio donde funcione de forma continua y donde otras personas puedan llegar a él. Eso es un **despliegue**. Y el lugar donde corre la versión que la gente usa de verdad tiene un nombre que carga más peso que cualquier otra palabra de este libro: **producción**.

Código fuente. Build. Artefacto. Despliegue. Producción. Cinco palabras, una dirección. Si no se lleva nada más de este capítulo, llévese la forma de esa flecha, porque todos los capítulos posteriores tratan de algo que se tuerce en algún punto de ella.

<div style="margin:1.6rem 0;">
<svg viewBox="0 0 680 120" width="100%" style="display:block;" xmlns="http://www.w3.org/2000/svg">
<defs>
<marker id="ptp1-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
<path d="M0,0 L6,3 L0,6" fill="none" stroke="#1a1a1a" stroke-width="1.1"/>
</marker>
</defs>
<rect x="6" y="30" width="112" height="56" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="62" y="63" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="11" font-weight="600" fill="#1a1a1a">CÓDIGO FUENTE</text>
<line x1="118" y1="58" x2="146" y2="58" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp1-arrow)"/>
<rect x="146" y="30" width="112" height="56" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="202" y="63" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="12.5" font-weight="600" fill="#1a1a1a">BUILD</text>
<line x1="258" y1="58" x2="286" y2="58" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp1-arrow)"/>
<rect x="286" y="30" width="112" height="56" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="342" y="63" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="12.5" font-weight="600" fill="#1a1a1a">ARTEFACTO</text>
<line x1="398" y1="58" x2="426" y2="58" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp1-arrow)"/>
<rect x="426" y="30" width="112" height="56" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="482" y="63" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="12.5" font-weight="600" fill="#1a1a1a">DESPLIEGUE</text>
<line x1="538" y1="58" x2="566" y2="58" stroke="#1a1a1a" stroke-width="1.1" marker-end="url(#ptp1-arrow)"/>
<rect x="566" y="30" width="108" height="56" fill="none" stroke="#1a1a1a" stroke-width="1.2"/>
<text x="620" y="63" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="12.5" font-weight="600" fill="#1a1a1a">PRODUCCIÓN</text>
<text x="340" y="110" text-anchor="middle" font-family="EB Garamond, Georgia, serif" font-size="10.5" font-style="italic" fill="#444">Cada capítulo posterior trata de algo que se tuerce en algún punto de esta flecha.</text>
</svg>
</div>

## Dos maneras de estar mal

Cuando construía en su propia pantalla había exactamente una forma de que las cosas estuvieran mal: el código estaba mal. Usted pedía algo, el agente lo entendía mal, o se equivocaba, y el resultado no hacía lo que usted quería. Lo miraba, lo veía, pedía que lo arreglara.

Esta forma de estar mal es *visible* e *inmediata*. La tiene delante.

Ahora piense en otra distinta. El código es perfecto. Cada instrucción es correcta. Y aun así:

- Funciona para usted y falla para un usuario en Argentina.
- Funcionaba ayer y hoy falla, aunque nadie ha cambiado nada.
- Funciona para una persona y se cae cuando llegan cuarenta a la vez.
- Funciona, y este mes le cobra 2.000 € en silencio en lugar de 20 €.
- Funciona, y lleva once días sirviéndole la factura de un cliente a otro — exactamente el fallo que el capítulo 12 pilla cometiendo a Ledgerly.

Ninguno de estos es un problema de código en el sentido al que usted está acostumbrado. Son problemas del **sistema** — y *sistema* aquí significa todo lo que tiene que estar funcionando para que un usuario consiga aquello a lo que vino. El programa, sí, pero también la máquina que hay debajo, la red que hay en medio, la base de datos que guarda los datos, el servicio de terceros al que llama, los ajustes que cambian entre su portátil y el mundo real, y las suposiciones que hizo todo el mundo sobre cuánto tráfico habría.

El sistema es suyo. No solo el código.

Ese es el traspaso de verdad. El agente le dio código. El sistema es suyo, y lo era desde el momento en que una persona real pudo llegar a él.

## Por qué nadie se lo había contado

Merece la pena ser preciso sobre por qué existe esta laguna, y no es que los ingenieros estuvieran escondiendo nada.

La ingeniería de software como profesión tendrá unos setenta años. Durante casi todo ese tiempo, la única forma de conseguir código era escribirlo, y escribirlo llevaba años aprenderlo. Para cuando alguien era capaz de producir un programa que funcionase, ya había absorbido — despacio, y sobre todo sufriendo — todo lo demás: que se guarda un historial de los cambios, que nunca se prueba sobre el sistema en vivo, que los secretos no van en el código fuente, que hace falta enterarse de que algo se ha roto antes de que se lo digan los clientes.

Nada de eso se enseñaba como asignatura aparte. Venía en el paquete. Era el agua.

Lo que ha cambiado es que el paquete se ha desatado. Ahora se puede conseguir código que funciona sin los años, lo cual es genuinamente maravilloso, y significa que el agua ya no está. Nadie la quitó a propósito. Sencillamente nunca fue una cosa aparte que se pudiera entregar, así que cuando el código llegó sin ella, nadie notó la ausencia.

Las personas que podrían contárselo suelen ser las peor situadas para hacerlo. Pregúntele a un ingeniero con experiencia qué necesita saber y recibirá o un encogimiento de hombros — porque para él eso no es conocimiento, es sencillamente cómo son las cosas — o una manguera de detalles sobre herramientas que a usted no tienen por qué importarle. La forma general es difícil de ver desde dentro — y esa forma es de lo que trata este libro.

## Lo que necesita

Voy a ser honesto sobre el alcance de lo que afirmo, porque en esta materia se escribe mucho de forma deshonesta.

Una palabra sobre para quién es esto, porque es más amplio de lo que parece al principio. El lector evidente es alguien que no sabe programar y ha descubierto que un agente puede construirle cosas. Pero la condición real de la que trata este libro es más general: **ahora puede construir software más deprisa de lo que su criterio de ingeniería ha tenido tiempo de desarrollarse.** Eso describe a fundadores, jefes de producto, científicos, analistas y diseñadores — y describe igual de bien a un desarrollador competente trabajando dos capas fuera de su terreno habitual, que hoy le pasa a casi todo el mundo. Si ha publicado algo de lo que no podría dar cuenta del todo, está en el sitio correcto, sea cual sea su oficio.

Este libro no le va a enseñar a programar. No lo terminará siendo capaz de leer un trozo de código complicado y decir si es bueno. Eso es una habilidad de verdad, lleva tiempo de verdad, y fingir lo contrario le haría perder el suyo.

Lo que sí hará es darle el **vocabulario y el mapa**. Al terminar sabrá cómo se llaman las partes de un sistema, para qué sirve cada una, qué se tuerce en cada una y qué aspecto tiene «hecho como es debido» — lo bastante bien como para pedirlo. Resulta que ahí está casi todo el valor, por una razón concreta:

**Un agente construirá casi cualquier cosa que le pida, y rara vez le dirá qué se le ha olvidado pedir.**

Pida una página de acceso y tendrá una página de acceso. Si además tendrá una contraseña bien guardada, una forma de recuperar la olvidada, un registro de quién entró y cuándo, y un límite de cuántas contraseñas pueden probarse por minuto — eso depende enteramente de si usted sabía que esas cosas existían.

El agente no se está guardando nada. Está respondiendo a la pregunta que le hizo. La habilidad que necesita no es escribir código. Es saber qué preguntas existen.

## De qué no trata este libro

No trata de Claude Code, ni de Codex, ni de Cursor, ni de lo que anuncien el mes que viene — trata del terreno sobre el que se apoyan esas herramientas.

Es una renuncia deliberada, no un descuido. Las herramientas son la parte que más deprisa se mueve de todo este paisaje: sus interfaces cambian cada mes, sus capacidades cada trimestre, y la mitad de lo concreto que se escribe sobre ellas está equivocado en menos de un año. Un libro organizado alrededor de una de ellas sería un libro con una caducidad de meses, y usted tendría que desconfiar de cada página para cuando lo terminase.

Lo que el agente le entrega se mueve en una escala de tiempo completamente distinta. La idea de que los cambios deben quedar registrados y ser reversibles tiene cincuenta años. La forma en que los navegadores hablan con los servidores tiene treinta. La idea de que uno debería poder reproducir un build a partir de la fuente es más antigua que casi toda la industria. Nadie va a declarar obsoleto el concepto de copia de seguridad.

Así que: nada de capturas de pantalla, nada de instrucciones que copiar, nada de indicaciones específicas de una herramienta. Cuando este libro dice «el agente», se refiere al que usted use. Todo lo de aquí debería aplicarse igual a una herramienta que todavía no existe — y si deja de aplicarse, eso será una noticia de verdad y no un cambio de versión.

## Lo que este libro no cubre

El libro da por hecho que usted está construyendo una **aplicación web o un servicio** — algo con una pantalla o una interfaz, un *backend* y una base de datos, funcionando en los ordenadores de otra persona. Es lo que más a menudo se le pide construir a un agente, y es donde las prácticas se trasladan más lejos.

Varias cosas quedan fuera de ahí, y son genuinamente distintas más que simplemente omitidas:

- **Aplicaciones móviles nativas.** Buena parte de la parte III no sobrevive al contacto con una tienda de aplicaciones. No puede desplegar en cuatro minutos, no puede revertir una versión que la gente ya se ha instalado en el móvil, y otro decide cuándo sale su *release*. Los conceptos siguen aplicándose; la mecánica es un asunto aparte.
- **Software de escritorio y empotrado**, por lo mismo y más.
- **Sistemas de aprendizaje automático.** Entrenar modelos, versionar conjuntos de datos y darse cuenta de que un modelo empeora en silencio son una disciplina propia, con una práctica operativa que este libro no toca.
- **Videojuegos**, que tienen su propio todo.
- **Muy gran escala.** Todo lo de aquí está escrito para un sistema que sirve hasta unos cientos de miles de personas, llevado por un puñado de gente. Pasado eso, varios capítulos dejan de ser suficientes.
- **Trabajo regulado** — dispositivos médicos, aviación, banca más allá de lo básico — donde las normas son concretas, jurídicamente vinculantes, y no algo que se aprenda de un libro general.

## Una nota sobre las palabras

Hay mucha jerga por delante. Unos ciento cincuenta términos, y todos se definirán la primera vez que aparezcan y se recogerán en el glosario del final.

Quiero decir algo sobre la jerga, porque la gente se disculpa por ella con demasiada facilidad. La jerga no es una barrera que los ingenieros levantaran para dejarle fuera. Sobre todo es *compresión*: una palabra que ahorra una frase. «Idempotente» (capítulo 8) no es presumir; significa «se puede ejecutar dos veces sin peligro», y una vez tiene la palabra puede expresar en un adjetivo una propiedad que si no le llevaría un párrafo y saldría confusa.

La razón de que la jerga resulte excluyente no son las palabras. Es que la gente las usa sin que a nadie le hayan dicho nunca qué significan, y preguntar parece una confesión. Así las palabras se convierten en una prueba de pertenencia en lugar de en una herramienta.

Aquí no hay prueba. Cada término se define, en lenguaje corriente, una vez, y luego se usa de forma consistente. Cuando me comprometa con una analogía para algo — y lo haré, para las ideas donde una buena analogía trabaja más que una definición — usaré siempre la misma, en lugar de echar mano de una metáfora nueva en cada capítulo y dejarle a usted la tarea de reconciliarlas.

Esa consistencia la impone, por cierto, un programa. Este libro está escrito de la misma forma que el libro describe: el texto es fuente, guardado en un repositorio (capítulo 2) con todo su historial, comprobado automáticamente en busca de términos usados antes de definirse, y convertido en lo que usted está leyendo por una tubería de construcción. Si un capítulo usa una palabra que todavía no ha enseñado, el build falla. No es un truco. Es la demostración más barata posible de que las ideas de aquí no son teoría.

## Una cosa que llevarse de este capítulo

Si recuerda una sola frase, que sea esta:

**El código es lo que le da el agente. El sistema es lo que se encuentran sus usuarios, y es suyo.**

Todo lo que sigue es una respuesta a la pregunta de qué implica realmente ser dueño de un sistema.

## Qué pedir

Al final de cada capítulo sugeriré cosas que pedirle a su agente, redactadas tal como usted puede decirlas de verdad. Esta es la primera, y es deliberadamente modesta:

> «Antes de añadir nada más — explícame en qué consiste ahora mismo este proyecto. Cuáles son las piezas, qué funciona dónde, y qué tendría que ser cierto para que alguien que no sea yo pudiera usarlo.»

Todavía no entenderá cada palabra de la respuesta. Pídala igualmente, y guárdela. Al terminar este libro sabrá leerla, y es útil haber visto cómo cambiaba.
