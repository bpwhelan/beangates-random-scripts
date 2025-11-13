import re


def create_srt_file_flexible(text_data, output_filename="output.srt"):
    """
    Converts a string of timed dialogue into an SRT subtitle file.
    Handles time ranges on their own line, followed by dialogue on subsequent lines.

    Args:
        text_data (str): A string where each line contains either a time range
                         (e.g., "HH:MM - HH:MM") or dialogue text.
        output_filename (str): The name of the SRT file to create.
    """
    # Regex to match time ranges like '1:21 - 1:23', '01:21 - 01:23', '1:21:00 - 1:23:59'
    # This pattern only needs to capture the start and end time.
    time_range_pattern = re.compile(r'^\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*$')

    def format_time_srt(time_str):
        """Formats a time string (e.g., '1:21' or '1:21:00') to 'HH:MM:SS,ms'."""
        parts = [int(p) for p in time_str.split(':')]
        h, m, s = 0, 0, 0
        if len(parts) == 2:
            m, s = parts
        elif len(parts) == 3:
            h, m, s = parts

        return f"{h:02d}:{m:02d}:{s:02d},000"

    with open(output_filename, 'w', encoding='utf-8') as f:
        subtitle_number = 1
        current_dialogue_lines = []
        current_start_time = None
        current_end_time = None

        def write_current_subtitle():
            nonlocal subtitle_number
            if current_dialogue_lines and current_start_time and current_end_time:
                f.write(f"{subtitle_number}\n")
                f.write(f"{current_start_time} --> {current_end_time}\n")
                f.write(f"{' '.join(current_dialogue_lines).strip()}\n\n")
                subtitle_number += 1

        for line in text_data.strip().split('\n'):
            line = line.strip()
            if not line:
                continue

            match = time_range_pattern.match(line)
            if match:
                # If a new time range is found, write the previous subtitle (if any)
                write_current_subtitle()

                # Reset for the new subtitle
                start_time_raw, end_time_raw = match.groups()
                current_start_time = format_time_srt(start_time_raw)
                current_end_time = format_time_srt(end_time_raw)
                current_dialogue_lines = []  # Start fresh for the new time range
            else:
                # If it's a raw string, append it to the current dialogue
                current_dialogue_lines.append(line)

        # Write any remaining subtitle at the end of the file
        write_current_subtitle()


# Your input text with dates on separate lines
input_text = """
1:21 - 1:23
¡Buenas señor! Tenemos un casting.
1:23 - 1:26
Sí claro con mucho gusto.
1:26 - 1:29
Bien puedan sigan señoritas.
1:29 - 1:34
A la orden.
Vengo a una entrevista de trabajo. Siga por allá.
1:47 - 1:48
Buenas tardes, Buenas tardes.
1:49 - 1:50
Venimos a una casting.
1:50 - 1:52
¡Sí! Con el sr. Hugo Lombardi
1:52 - 1:54
Y ¿ustedes son modelos? Sí
1:54 - 1:56
Segundo piso, al fondo. Gracias.
1:58 - 2:03
¡Modelos! Flacas, desgarbadas.
Más tengo yo de modelo mamitas.
2:03 - 2:06
Buenas. Vengo a una entrevista de trabajo.
2:06 - 2:09
Sí. Segundo piso sala de juntas.
2:46 - 2:48
Eso, lindo. Muy bonito. Arriba.
2:49 - 2:53
¿Qué hubo? Sí gorda. Llegue tarde y verá.
2:53 - 2:56
¡Inesita! Atiéndame ahí a estas modelos.
2:56 - 2:57
Sí, Don Hugo. Ya voy.
2:57 - 2:58
¿Dónde está mi tinto? Mi tinto.
3:01 - 3:05
¿Usted qué hace aquí? ¿Usted quién es?
¿Qué agencia me la mandó?
3:05 - 3:07
Estoy buscando la sala de juntas.
3:07 - 3:09
La sala de juntas queda allá al fondo.
3:09 - 3:11
Aquí no venga que estamos ensayando.
3:11 - 3:13
Ni se le ocurra. Ni por chiste. ¿Oyó?
3:17 - 3:19
Patricia Fernandez. Soy yo.
Siga por favor.
3:20 - 3:22
Tengo que dejarte. Ya me llamaron.
3:23 - 3:24
Beatriz Pinzón.
3:24 - 3:25
Soy yo.
3:26 - 3:27
Soy yo
3:29 - 3:31
Yo soy Beatriz Pinzón.
3:33 - 3:34
Siga, siga.
3:34 - 3:36
Doctor, llegó Beatriz Pinzón.
3:37 - 3:38
Ahora sí. Buenos días.
3:38 - 3:40
Buenos días. Siéntese.
3:40 - 3:41
Gracías.
3:44 - 3:46
Siéntese, por favor.
3:47 - 3:48
¿Su nombre? Patricia Fernández.
3:50 - 3:54
¿Y el suyo? Beatriz Pinzón Solano.
3:55 - 3:58
Bien. Como saben,
estamos buscando una secretaria
3:58 - 4:01
para la presidencia de esta compañía.
4:02 - 4:08
y me gustaría saber porqué creen que son
las personas indicadas para este cargo.
4:09 - 4:11
A ver Patricia. Comencemos por usted.
4:12 - 4:14
¿Qué experiencia tiene? y
¿por qué está aquí?
4:14 - 4:18
Bueno, yo en realidad no
tengo ninguna experiencia como secretaria
4:18 - 4:24
es más, nunca he trabajado, pero yo hice
semestres de finanzas en la San Marino
4:24 - 4:27
Y bueno, estoy aquí porque
Marcela Valencia me dijo
4:27 - 4:30
que Armando estaba buscando una secretaria
4:30 - 4:34
Ah claro, entiendo. ¿Y usted?
4:34 - 4:37
Bueno, yo tampoco tengo
experiencia como secretaria
4:37 - 4:40
pero permítame le explico:
4:40 - 4:44
Yo estudié economía en la Universidad de
Estudios Económicos y Finanzas.
4:44 - 4:47
Y como podrá ver en mi hoja de vida,
salí con tesis laureada
4:47 - 4:50
y tuve el promedio
más alto en la Universidad
4:50 - 4:53
Ahí están el Rector y el Decano de
la Facultad como referencias personales
4:54 - 4:58
Luego hice un curso de contabilidad
y después un posgrado en finanzas.
4:59 - 5:02
También fui auxiliar del área
internacional del Banco Montreal
5:02 - 5:06
siendo vicepresidente de esa área
el Doctor Manuel José Becerra.
5:06 - 5:08
También está como referencia.
5:08 - 5:12
Manejo base de datos, sistemas financieros
análisis de proyectos de inversión
5:12 - 5:16
comercio exterior, estudios de
factibilidad, costos, y presupuestos.
5:16 - 5:18
También conozco el mercado bursátil.
5:18 - 5:20
Ahí aparece toda la información.
5:22 - 5:22
Sí, sí veo.
5:25 - 5:27
Lo que no veo es su foto.
5:28 - 5:32
¿Por qué no le adjuntó foto
a su hoja de vida?
5:34 - 5:38
Bueno, como me he presentado a
tantas entrevistas se me acabaron.
5:38 - 5:41
pero si quiere mañana le traigo una.
5:41 - 5:42
No, tranquila.
5:43 - 5:49
Dígame una cosa:
Si tiene semejante hoja de vida,
5:49 - 5:52
¿por qué está buscando puesto
como secretaría?
5:52 - 5:56
como usted sabe, hay mucha competencia,
y como no tengo gran experiencia,
5:57 - 6:00
me llama la atención
iniciar mi carrera
6:00 - 6:03
como una secretaria ejecutiva
en una empresa como esta.
6:03 - 6:07
Demostrar mis capacidades,
ascender dentro de la empresa,
6:08 - 6:11
y por el trabajo como secretaria,
no tengo ningún problema.
6:11 - 6:16
Puedo atender llamadas telefónicas,
manejar una agenda, redactar cartas.
6:16 - 6:18
Es muy sencillo para mi.
6:18 - 6:20
Sí claro. ¿Y cómo estamos de idiomas?
6:21 - 6:22
Bueno yo hablo más o menos inglés.
6:25 - 6:29
Yo hablo inglés, francés
y un poco de italiano.
6:29 - 6:34
¿y son separadas, casadas,
viudas, solteras?
6:36 - 6:38
Bueno yo soy separada.
6:38 - 6:40
Yo estuve casada con Mauricio Brickhman.
6:40 - 6:46
Brickhman. Of course! I know him.
El presidente de Coltex Corporation.
6:46 - 6:47
Sí el mismo.
6:48 - 6:52
Yo lo conocí cuando estudiaba
altas finanzas en la San Marino.
6:52 - 6:54
Nos enamoramos, nos casamos.
6:54 - 6:56
Por él me retiré de la universidad.
6:56 - 6:58
Y bueno, hace un año que
nos separamos
6:58 - 7:02
Me fui a vivir un tiempo a España
y regresé hace como un mes.
7:02 - 7:04
Así que estoy libre de compromisos.
7:07 - 7:08
¿Y usted?
7:09 - 7:12
Yo soy soltera, soltera.
7:12 - 7:13
Sí claro.
7:13 - 7:16
Bueno, nosotros tenemos sus hojas de vida.
7:17 - 7:19
Gracias por venir. Las estaremos llamando.
7:24 - 7:28
¡Espere! Patricia, quédese un momento.
7:29 - 7:32
Gracias por venir. La estaremos llamando.
7:32 - 7:33
No se preocupe. Gracias.
7:37 - 7:39
Niñas, niñas, no me hagan tanta bulla
7:40 - 7:43
¡Ay perdón!
Ay muchachita, ¡por Dios!
7:45 - 7:47
Buenos días todo el mundo. Buenos días.
7:49 - 7:51
No mija. Venga. Mejor ayúdeme a tapar.
7:51 - 7:54
Ay que no se vayan a dar cuenta de
este reguero.
7:54 - 7:57
¿Quiénes son? Es don Roberto Mendoza,
el presidente de la compañía.
7:57 - 8:00
y el hijo, don Armando,
que va a ser el nuevo Presidente.
8:00 - 8:02
Y su jefe si es que usted pasa.
8:02 - 8:03
y ¿por qué hay tanta gente aquí?
8:03 - 8:07
Hugo, que está ensayando a las modelos
para el Fashion de compradores.
8:07 - 8:09
y Gutiérrez, que está entrevistando
a las aspirantes a
8:09 - 8:11
secretaria de presidencia, papá.
8:11 - 8:13
y ¿por qué no lo estás haciendo
tú personalmente?
8:13 - 8:16
Uno debería escoger personalmente
a su secretaria. ¿o no?
8:16 - 8:20
Papá ¿me dedico a entrevistar secretarias
o a hacer el empalme contigo?
8:20 - 8:25
deja que Gutiérrez se encargue de eso.
Él sabe perfectamente qué estoy buscando.
8:25 - 8:29
Sí, yo también sé perfectamente
lo que tú estás buscando.
8:29 - 8:30
Hola
8:30 - 8:32
Don Roberto, ¿cómo le va?
8:40 - 8:43
¿Qué significa esto? Berta
8:44 - 8:46
Doctor, es que yo ... yo ...
8:47 - 8:49
Esto no tiene ninguna justificación
8:49 - 8:52
¿Acaso no se da cuenta de la cantidad de
gente que nos está visitando hoy?
8:52 - 8:57
¿Cómo vamos a parecer una empresa de
modas si el corredor está lleno de basura?
8:57 - 8:59
Sí doctor, pero lo que pasa es ...
8:59 - 9:03
¡Nada!, me llama ya a Aseo,
y tiene diez minutos
9:03 - 9:06
para dejar este corredor
como si fuera un espejo.
9:06 - 9:09
¿Me entendió? Berta
9:09 - 9:10
Sí doctor.
9:11 - 9:13
Vaya, recoja, ¡vaya hombre!
9:17 - 9:18
Lo siento mucho.
9:18 - 9:20
No, no se preocupe
9:20 - 9:24
Entonces nosotros la llamamos para
que venga y firme su contrato.
9:25 - 9:27
¡Bertica!
¿Sí doctor?
9:27 - 9:29
Despache a la gente, no más entrevistas.
9:29 - 9:32
Niñas, no va a haber más
entrevistas por hoy.
9:33 - 9:35
Cualquier cosa las estamos llamando.
9:35 - 9:37
¿y esta a qué se quedó aquí?
9:38 - 9:41
Seguramente aún guardaba la
esperanza de que la contrataramos.
9:41 - 9:45
Oiga Gutiérrez, ¿está seguro que
hizo bien contratando la bonita?
9:46 - 9:48
La fea es mucho más preparada.
9:48 - 9:51
Sí hermanito pero no le sirve de nada.
9:51 - 9:56
Armando me pidió que le contratara a su
secretaria. Yo sé muy bien lo que él busca
9:57 - 10:01
Y donde le presente a ese chimbilá,
me hace echar.
10:01 - 10:05
Yo me puedo sacrificar teniendo
una secretaria fea como Berta,
10:05 - 10:09
¡pero un Presidente no!
y mucho menos don Armando
10:09 - 10:13
Le da sarpullido cuando ve a una mujer fea
11:37 - 11:38
Hola Betty, mija. ¿Cómo le fue?
11:39 - 11:42
Yo creo que bien mamá, pero hay que esperar.
11:42 - 11:45
Su papá no ha hecho sino llamar todo el día, mamita.
11:45 - 11:46
preguntando por usted.
11:46 - 11:49
Hay que tener paciencia mamá.
11:49 - 11:53
¡Sí! Vea mamita yo ya le puse otra velita a San Pancracio.
11:53 - 11:54
¿Y ese quién es?
11:55 - 11:58
¡Ay mi amor! ¿cómo así? El Santo que busca trabajo.
11:59 - 12:04
Mira mi amor, ¿la empresa donde usted fue a pedir trabajo se llama como Ecomoda?
12:04 - 12:06
Sí ¿por qué?
12:06 - 12:07
Porque me leí un artículo mija,
12:07 - 12:10
que si usted entra a trabajar allá le va a servir
12:10 - 12:12
Espere se lo traigo.
12:17 - 12:19
Seño! Una miradita señorita!
12:22 - 12:25
Nicolás! Nicolás!
12:26 - 12:31
Reaccione!
Estaba divina, Betty. ¿No la vió?
12:35 - 12:36
¿Cómo le fue hoy?
12:36 - 12:38
¿Dónde estuvo Betty?
12:38 - 12:40
En una empresa de moda.
12:41 - 12:42
¿y?
12:42 - 12:44
Lo mismo de siempre.
12:44 - 12:48
Me ganó el puesto una bonita.
15:32 - 15:34
pero volando hermano
15:34 - 15:35
A ver Betty ... cuente
15:36 - 15:37
A Ecomoda
15:37 - 15:41
Ecomoda ... Mendoza, Valencia y Asociados
15:51 - 15:53
mire mi amor, ésta es la revista Jet Set
15:53 - 15:55
donde sale el artículo de Ecomoda, mi amor
15:55 - 15:57
Quihubo Nico! Doña Julia!
15:58 - 16:00
Ellos son los dueños de la empresa
16:06 - 16:07
En la Presidencia.
16:10 - 16:11
Ah... y eso ¿por qué?
16:11 - 16:12
Yo que voy a saber
16:20 - 16:22
Voy a hacerle la comida a su papá mi amor
16:22 - 16:23
Ya le traigo algo Niquito
16:23 - 16:25
Gracias doña Julia.
16:27 - 16:30
Betty, ¿está segura que la descartaron?
16:30 - 16:31
Es una tremenda empresa.
16:31 - 16:35
Usted ahí queda vea
16:35 - 16:36
Sí no hay opción, Nicolás.
16:54 - 16:56
Voy a traer doce fileteadoras más.
17:01 - 17:03
por traer más máquinas, puras máquinas.
17:04 - 17:06
Papá yo no voy a hacer eso.
17:12 - 17:13
Eso es todo.
17:44 - 17:46
del área internacional del Banco.
17:46 - 17:50
Manuel José Becerra ... sí ... sí doctor.
18:00 - 18:01
¿Quién es ella?
18:06 - 18:10
Es economista con una tesis en finanzas.
18:50 - 18:52
ella prefería empezar como secretaría
19:04 - 19:08
Eso es fácil de averigúar con Manuel José.
19:26 - 19:30
lo que pasa es que tiene un problemita
19:31 - 19:32
¿cuál problemita?
19:34 - 19:35
¿fea? ¿qué tan fea?
19:35 - 19:38
Muéstreme la foto de la hoja de vida.
19:39 - 19:40
¿Por qué?
19:47 - 19:48
Sí es cierto, Nicolás.
19:58 - 20:00
pero ven la foto y me rechazan.
20:00 - 20:02
Es un problema de casting.
20:04 - 20:05
¿Casting?
20:05 - 20:09
Sí, mejor dicho todos me rechazan por fea.
20:10 - 20:11
No, no Betty no es eso.
20:34 - 20:35
menos nosotros dos
20:39 - 20:40
No, no Betty. Tampoco!
20:45 - 20:47
No hemos pedido trabajo en un circo.
21:04 - 21:06
cuando se pongan rebeldes
21:13 - 21:16
Sí Nicolás. Nadie nos quiere por feos.
21:29 - 21:30
Hasta luego
21:31 - 21:32
¿Qué dijo? papá
21:41 - 21:43
Pero me la recomendó muchísimo.
21:43 - 21:46
Me dijo que era una mujer extraordinaria.
22:02 - 22:08
Cuénteme, ¿es más fea que usted?
22:08 - 22:10
Un poquito más don Armando.
22:10 - 22:12
A ver ... como les explico
22:28 - 22:33
por eso la descalifique
22:39 - 22:42
Tú decides.
22:48 - 22:50
Vamos a ver que tan fea es
23:02 - 23:05
Demasiado fea para un mundo como éste
23:09 - 23:12
Es gente bella, de clase.
23:24 - 23:25
Siga leyendo Betty
23:40 - 23:44
como siempre muy unidos y sonrientes
23:44 - 23:46
Se ven una pareja feliz
23:52 - 23:54
Roberto, ¿qué te pasa? por Dios
23:54 - 23:56
Te he notado preocupado toda la noche
24:13 - 24:17
yo no voy a poder descansar
24:17 - 24:19
Gracias.
24:19 - 24:20
Mira a Armando y a Daniel
24:31 - 24:34
Porque posiblemente sea la última
24:42 - 24:44
Y sus 35 años de trabajo
25:05 - 25:08
para que haga juego con tu ataúd
25:28 - 25:31
que prometió, tú asumirás la presidencia
25:34 - 25:36
Ojalá quede algo para administrar
25:54 - 25:57
cuando Armando asuma la presidencia
26:15 - 26:18
Pues eso está por verse.
26:25 - 26:26
y un poco más arrugado
26:34 - 26:36
sonríe!
26:46 - 26:49
a partir de la próxima semana y que comparte alegre con Daniel Valencia
26:49 - 26:53
accionista de la empresa y quien también sonó como sucesor de Roberto
26:54 - 26:57
los Mendoza y los Valencia, dos familias inseparables.
26:58 - 27:04
Yo pensé que este señor y su hijo eran los únicos dueños de la empresa
27:04 - 27:07
Hasta lo que tengo entendido, Betty, la familia Valencia es dueña de la mitad de la empresa.
27:07 - 27:10
Y ese tal Daniel Valencia no trabaja en esa empresa
27:10 - 27:13
sino que es un alto funcionario del gobierno
27:13 - 27:15
sí yo sé. Él es el gerente de recursos financieros.
27:15 - 27:20
De todas manera se ven dos familias muy unida, ¿no?
27:20 - 27:21
Y no sólo por la empresa
27:21 - 27:23
Vea, mire
27:23 - 27:27
Armando Mendoza y su bella prometida Marcela Valencia
27:27 - 27:31
además de unir los lazos de la sociedad en Ecomoda, los une el amor desde hace dos años
27:31 - 27:33
suenan campanas de boda
27:34 - 27:37
Ah ... se van a casar
27:40 - 27:44
Gracias. A ustedes.
27:44 - 27:47
Tus novias te van a matar cuando te vean abrazándome
27:47 - 27:48
Pero ¿por qué mi amor? ¿cuáles novias?
27:48 - 27:52
si tú estás hablando con tu futuro monogámico esposo
27:52 - 27:54
no con el propietario de un harem
27:54 - 27:57
Bravo, bravo. Quedaron muy bonitos en la foto
27:57 - 28:00
¿Sabes qué tienen un romance de revista?
28:00 - 28:05
Las únicas veces que lo he visto cariñoso contigo es cuando se acercan los fotógrafos de las revistas
28:05 - 28:10
Buenísimo ... no nos gusta la melosería y no juzques
28:10 - 28:12
no nos has visto en la intimidad
28:12 - 28:16
Claro que si quieres, te mandamos unas fotos para que goces.
28:16 - 28:17
Pero ojalá que sea con Marcela
28:17 - 28:21
y no vaya a ser que se te cufundan con las que estás explícito con alguna de tus modelos
28:23 - 28:29
Me voy. No soporto tanto carnaval de sonrisas.
28:29 - 28:31
¿Por qué tan pronto?
28:31 - 28:33
No mi amor, por favor déjalo ir
28:33 - 28:36
Mira que a esta hora los vampiros están buscando refugio para que no los coja el amanecer
28:38 - 28:41
Ay Dios mío
28:41 - 28:45
Esta ribalidad entre ustedes me está matando, Daniel.
28:45 - 28:48
Tú tienes que entender que él va a ser el presidente de la empresa
28:48 - 28:51
ustedes dos tienen que hacer las paces
28:51 - 28:56
No sólo porque nos críamos con los Mendozas como hermanos sino porque en poco tiempo Armando va a ser mi marido
28:56 - 28:59
Todavía te puede dejar plantada en el altar.
28:59 - 29:01
No has pensado en eso
29:01 - 29:06
¿Ya acordaron fecha de matrimonio?
29:06 - 29:09
No. Simplemente acordamos que nos casaríamos.
29:09 - 29:13
Sí claro! Dos días antes de la junta que eligió a Armando como presidente
29:13 - 29:16
Y por supuesto, contó con tu voto.
29:16 - 29:21
Sí, ya lo sé. Eso también lo hablamos.
29:21 - 29:27
Daniel, tú estás sugiriendo que Armando me propuso matrimonio para asegurarse la presidencia de Ecomoda
29:27 - 29:29
Yo no estoy sugiriendo nada.
29:29 - 29:33
Utilizó todo lo que tenía a mano para hacerse con la presidencia
29:33 - 29:38
Y ahora que lo logró, quién sabe si cumpla su promesa de matrimonio.
29:39 - 29:41
Bueno hermanita, buenas noches.
29:41 - 29:43
Buenas noches.
29:46 - 29:52
Me voy a casar. Entiéndalo. Sí sí no lo dudo pero no con Marcela
29:52 - 29:54
Claro que debo admitir que proponerle matrimonio con una fecha
29:54 - 29:58
incierta fue una jugada maestra de política
29:58 - 30:01
Prometen el cielo y la tierra mientras los eligen
30:01 - 30:04
y después, arrasan con el cielo y la tierra prometida
30:04 - 30:10
Bueno, yo prometo matrimonio pero sólo cuando una mujer está renuente a pasar la noche conmigo
30:10 - 30:13
Y tú, no tienes necesidad de hacer eso con Marcela.
30:13 - 30:17
Claro, yo sé. Necesitas el voto de ella para la junta directiva.
30:17 - 30:20
Pero por ese voto no puedes hacer voto de castidad
30:20 - 30:23
Mario, yo no me voy a casar con ella por eso.
30:23 - 30:26
Me voy a casar porque lo quiero así
30:26 - 30:27
Además tengo que cambiar de vida.
30:27 - 30:32
No se ría. Es que yo voy a hacer el presidente de Ecomoda
30:32 - 30:35
No me la puedo pasar toda la vida como usted, bobiando.
30:35 - 30:36
Sí Fraile Armando, sí sí
30:36 - 30:39
Hay cuidado que ahí llega la primavera
30:39 - 30:45
Armando, venimos a que nos confirmes un chisme
30:45 - 30:47
¿Es verdad que te casas?
30:52 - 30:54
¿Sí? Ay es cierto, lo perdimos chicas.
30:54 - 30:55
Bueno, no importa.
30:55 - 30:57
De todas formas, felicitaciones.
30:57 - 31:00
Cuidado con esas uñas se le rompen.
31:00 - 31:05
Ay, ¿cuál es el temor? ¿qué te vean abrazado conmigo?
31:05 - 31:07
¿o qué las mujeres piensen que tú eres de la colonia?
31:07 - 31:11
¿Qué importa que lo confunda? Gay o casado es lo mismo.
31:11 - 31:12
Ninguna se le va a acercar.
31:12 - 31:14
¿O no? mi amor
31:14 - 31:18
Ay Mario, como se te ve de bien el azul.
31:27 - 31:45
Foto, foto. Tranquilos no se pongan nerviosos, y sonrían.
31:46 - 31:50
Armando Mendoza comparte alegre con el diseñador estrella de Ecomoda
31:50 - 31:54
Hugo Lombardi y con Mario Calderon, vicepresidente comercial y
31:54 - 31:59
quien parece celebrar divertido con el diseñador la existosa presentación de la colección.
31:59 - 32:02
Claro, Betty. Cuando uno reposa sobre 50 millones de dólares
32:02 - 32:05
la vida es un chiste, ¿cierto?
32:06 - 32:08
Buenas tardes.
32:08 - 32:10
Don Ermés, ¿cómo le va?
32:10 - 32:12
Bien. ¿Qué hubo mija?
32:12 - 32:16
Hola papi. ¿Ustedes dos están sólos aquí?
32:16 - 32:19
No, papá. Mi mamá está en la cocina.
32:19 - 32:21
¿Cómo le fue en la entrevista de hoy, mija?
32:21 - 32:24
Bien, quedaron en llamarme.
32:24 - 32:25
Y ¿quién la entrevistó?
32:25 - 32:29
Me entrevistaron dos altos ejecutivos de la empresa.
32:29 - 32:30
¿Cómo así? ¿dos tipos?
32:30 - 32:31
Usted entró sóla a la oficina.
32:31 - 32:35
No papá. Entré con otra niña que también se iba a presentar a la entrevista.
32:35 - 32:40
En ningún momento yo estuve sola con ellos y se comportaron muy bien conmigo.
32:45 - 32:48
Mija.
32:48 - 32:52
Mi papá todavía sueña con que algún tipo se sobrepase conmigo.
32:52 - 32:54
Él es el único hombre que me ve bonita.
32:54 - 32:56
No se ha dado cuenta que tiene una hija fea.
32:56 - 33:00
Lo que pasa es que no tuvo otra hija para poder compararla
33:05 - 33:08
¿Quién es esta? Deje ver.
33:08 - 33:10
Cuidado con la revista que es de mi mamá.
33:10 - 33:13
Pero vea que mujer tan bella, que mamacita
33:13 - 33:15
Ah ... pues esta fue la que me quito el puesto
33:15 - 33:19
Esta fue la que quedó finalmente como secretaría de presidencia
33:19 - 33:22
Lo que yo no entiendo es porque una mujer como ésta
33:22 - 33:26
amiga de la accionista de la empresa, y futura esposa del presidente de la compañía
33:26 - 33:30
se pone a buscar trabajo, si ella pudo pedirla por derecha
33:30 - 33:31
sin exámenes ni nada
33:31 - 33:36
y además como secretaria ella hizo 6 semestres de finanzas y dice que en la San Marino
33:36 - 33:38
eso está muy raro Betty
33:38 - 33:39
se le ve la plata
33:39 - 33:48
vea si ve el collarcito. Con ese collar podemos vivir usted y su familia y yo y mi familia como un año.
33:52 - 33:55
Y ya le dijiste a Armando que me de trabajo
33:55 - 33:57
Ay no te preocupes por eso
33:57 - 33:59
Mira si yo le digo a Armando que te de trabajo por derecha
33:59 - 34:03
Me va a decir que no. Que tienes que presentarte como todas las demás
34:03 - 34:06
y eso es lo que tienes que hacer.
34:06 - 34:07
Presentarte como una más. Yo me encargo del resto.
34:07 - 34:09
Bueno, tú sabrás porque lo dices.
34:09 - 34:11
y ¿dónde hay campo para mi? ¿en qué área?
34:11 - 34:14
sólo hay una vacante
34:14 - 34:15
ay ... lo que sea Marce
34:15 - 34:16
necesito ingresos urgentemente o la próxima vez
34:16 - 34:19
que me veas será en la cárcel de mujer
34:19 - 34:21
y tú por allá no te arrimarías
34:21 - 34:23
y ¿de qué es el trabajo?
34:23 - 34:27
de secretaria ... secretaria de la presidencia
34:27 - 34:30
la secretaria de Roberto se jubila con él
34:30 - 34:39
¿secretaria? Marcela no me está hablando en serio
34:39 - 34:42
Mi familia no me metió en la San Marino para terminar de secretaria
34:43 - 34:47
Yo no estudié 6 semestres de finanzas en la San Marino para terminar de secretaria
34:47 - 34:50
ni me casé con Mauricio Brichman porque tenía perfil de secretaria
34:50 - 34:52
ni me separé de él para buscar puesto de secretaria
34:52 - 34:54
así sea de presidencia, no es para mi
34:54 - 34:55
Marcela, tú no me puedes hacer esto.
34:55 - 34:57
Búscame otra cosa
34:57 - 34:58
Pues sí es para ti y no hay más
34:58 - 35:01
Vas a ser la secretaria de Armando y te necesito ahí
35:01 - 35:06
Patricia, él y yo nos vamos a casar. No sé cuando pero ya comprometió.
35:06 - 35:11
y dijo que iba a cambiar, que iba a ser fiel, y yo necesito cercionarme de eso
35:11 - 35:13
Ay sí claro, eso suena muy lindo para ti
35:13 - 35:17
¿Qué tal? Una espía con sueldo de secretaria
35:17 - 35:21
pero olvídalo ... lo aceptaría si por lo menos fuera bien remunerado
35:21 - 35:24
pero Marcela tú sabes muy bien mi situación.
35:24 - 35:27
Me van a quitar la acción del club porque no he tenido con qué pagar la administración.
35:27 - 35:30
Me van a sacar del apartamento
35:30 - 35:33
Me cancelaron todas mis tarjetas de crédito
35:33 - 35:36
el carro, en cualquier momento llega una grúa y se lo lleva
35:36 - 35:37
y Mauricio no me quiere dar un peso
35:37 - 35:41
Ah ... ¿por qué te separaste mal de Mauricio? yo te lo advertí
35:41 - 35:45
te dije que gritándole que era el hombre más abominable del planeta que habías conocido,
35:45 - 35:49
y que lo odiabas no te iba a castigar con el corazón sino con la chequera
35:49 - 35:51
Bueno sí ... ya ... ya sé
35:51 - 35:53
Ya no me lo digas más que yo sé que manejé muy mal mis cosas con él
35:53 - 35:56
pero bueno ahora mismo no puedo hacer nada
35:56 - 35:58
sabes que la fotografía de mi matrimonio la tiene para tirar dardos
36:01 - 36:05
yo sé que debo resolver mi situación sola
36:05 - 36:07
¿sabes hace cuanto no me compro un vestido nuevo?
36:07 - 36:11
Me acaba de decir la Mercedes Dominguez que cada vez que me ve le gusta más este vestido.
36:11 - 36:15
Se están empezando a burlar de mi, Marcela.
36:15 - 36:17
Me están viendo repetir ropa.
36:17 - 36:19
Mira si yo no tengo una entrada decorosa de dinero,
36:19 - 36:22
voy a tener que salir de lo último digno y sagrado que me queda
36:22 - 36:24
este collar que me lo regaló mi mamá
36:24 - 36:28
Ay no fue lo único que te dejo
36:28 - 36:32
Bueno los otros los saco de la casa de empeño cuando me entre plata
36:32 - 36:34
Pero no de verdad
36:34 - 36:36
Sí salgo de este collar con la misma plata que me dan
36:36 - 36:38
me pagan mi entierro
36:38 - 36:40
No, no lo soportaría, no.
36:40 - 36:42
No vas a tener que hacerlo.
36:42 - 36:45
Mira, el hecho de que tengas un cargo de secretaria
36:45 - 36:47
no significa que tengas un sueldo de secretaria
36:47 - 36:50
vas a tener un sueldo de ejecutiva pero te necesito ahí
36:52 - 36:55
¿y si él no me acepta? Ay claro que te va a aceptar
36:55 - 36:57
como accionista de esta empresa y como su futura esposa
36:57 - 36:59
eso te lo garantizo
37:09 - 37:11
donde las pongan se ven divinas
37:11 - 37:19
¿sabes qué fue lo que más me gustó? cuando haces ese meneaito así que tal ... mi amor eres la mejor
37:19 - 37:22
Tigre, tigre ... no un segundo ... de verdad fue la locura
37:22 - 37:26
estabamos puestas las miradas ... un momento .. mi amor te lo digo eres la mejor ... de verdad
37:26 - 37:28
mi amor eres la mejor
37:28 - 37:31
estaba precisamente comentándoles acerca del desfile
37:31 - 37:33
y que ellas pensaban que a nosotros no nos había gustado
37:33 - 37:36
y yo les decía que mi esposo ... digo mi futura ... digo mi novia
37:36 - 37:40
es la mejor y a ella sí le gustó
37:40 - 37:42
ella sabe de esto
37:42 - 37:43
claro ... a mi me encantó
37:43 - 37:47
no, no se preocupen. A ellos les gustan desfilen o no desfilen
37:47 - 37:49
desfilen bien o desfilen mal
37:49 - 37:55
y por la ropa ningún problema, les gusta con o sin ropa
37:57 - 37:58
ahorita nos vemos
38:01 - 38:04
Marcelita no te había felicitado por tu matrimonio
38:04 - 38:06
Este miserable por fín decidió casarse contigo
38:06 - 38:09
Qué bueno! Ven acá. Un beso.
38:09 - 38:12
Muchas gracias. Aprovecho la ocasión para darte mis condolencias
38:12 - 38:18
Acaba de perder la libertad tu compañero de aventuras. Lo siento tanto.
38:18 - 38:21
Y tú, me puedes soltar. No necesitabas abrazarme.
38:21 - 38:23
Pero ¿qué pasó? ¿por qué, mi amor?
38:23 - 38:26
Voy por un whisky.
38:26 - 38:29
Las modelos van a pensar que sigues enamorado de mi.
38:29 - 38:31
Ay mi amor por favor. Tú sabes que estoy enamorado de ti.
38:31 - 38:35
Además yo no tengo nada con ninguna mujer, con ninguna modelo.
38:35 - 38:38
Deja la paranoia.
38:38 - 38:40
¿Ellas saben que nos vamos a casar?
38:40 - 38:44
Yo que voy a saber. Sabes como son las modelos. Tienen un ego como las actrices
38:44 - 38:45
no les cabe en el mundo
38:45 - 38:48
Además qué? Voy a ir por todos lados cada vez que me encuentro a alguien
38:48 - 38:50
¿Qué hubo? ¿Cómo le va? Me caso, anunciando ahí
38:53 - 38:54
No, ¿para qué?
38:54 - 38:55
Y ¿por qué eres tan cruel?
38:55 - 38:58
¿por qué no les dices? al fin y al cabo se van a tener que enterar
39:01 - 39:03
y a más de tres les va a dar un infarto cuando vean la foto de nuestra boda.
39:03 - 39:06
Si es que nos casamos
39:06 - 39:08
Claro que nos casamos.
39:08 - 39:09
Pero ¿cuándo? Armando
39:09 - 39:13
Tú dijiste que nos íbamos a casar cuando subieras a la presidencia
39:13 - 39:16
que querías fortalecer nuestra relación
39:16 - 39:19
que querías aterrizar tu vida
39:19 - 39:21
pero de la fecha ... eso quedó en la nebulosa
39:21 - 39:23
bueno ven
39:23 - 39:24
¿Adónde me llevas?
39:24 - 39:26
Ven y cállate
39:26 - 39:32
Permiso, por favor acérquense acá. Todo el mundo. Vengan.
39:32 - 39:34
Vengan y silencio. Necesito silencio. Un momento.
39:34 - 39:39
Silencio un momento por favor.
39:39 - 39:44
Bueno muchas gracias por estar aquí con nosotros.
39:44 - 39:47
Quiero agradecerle a la gente de la prensa
39:47 - 39:50
a los proveedores, a los compradores, a la gente de Ecomoda
39:50 - 39:53
por estár aquí con nosotros compartiendo nuestra última colección
39:53 - 39:58
y quiero aprovechar este momento para compartir con ustedes
39:58 - 40:01
una noticia muy especial
40:01 - 40:04
en Septiembre me caso con esta hermosa mujer
40:06 - 40:07
Un momento, un momento
40:07 - 40:11
Ahora si hay un cura aquí o un juez
40:11 - 40:14
nos casamos ya mismo
40:28 - 40:31
Mi amor, esto va a ser publicado en todas las revistas.
40:31 - 40:34
Espero que estés satisfecha
40:34 - 40:38
Si estás jugando conmigo jamás te lo perdonaría.
41:01 - 41:03
Armando Mendoza y su novia Marcela
41:03 - 41:08
sorprendieron a los invitados anunciando en público su compromiso de matrimonio
41:08 - 41:11
la boda será en Septiembre
41:11 - 41:13
Ay tan romántico
41:13 - 41:15
Sí Betty, se ve que se quieren
41:15 - 41:17
Bueno están hechos el uno para el otro
41:17 - 41:19
son una pareja de bellos
41:19 - 41:21
Sí, sí ahí todos son bellos
41:21 - 41:24
A usted o a mí nunca nos van a invitar a un cóctel de esos
41:24 - 41:26
Si ni siquiera nos invitan a las fiestas del barrio
41:26 - 41:30
que nos van a invitar a un cóctel de esos
41:34 - 41:37
No ese es el mundo de los bellos y yo no puedo estár ahí
41:37 - 41:42
Ellos son felices, no tienen problemas, no son feos.
41:46 - 41:51
Aló. ¿Quién la necesita?
41:51 - 41:55
De Ecomoda. Un momento.
41:55 - 41:57
Dios mío es de la empresa que se presentó la niña hoy, mijo
41:57 - 42:02
Betty, mija, corra que es de Ecomoda mamita.
42:02 - 42:05
Ya tranquila mamá.
42:05 - 42:08
¿De verdad es Ecomoda? Sí.
42:08 - 42:12
Aló. Sí con ella habla.
42:12 - 42:16
Mañana a las nueve. Bueno muchas gracias. Adiós.
42:19 - 42:22
Le salió el trabajo.
Pues todavía no estoy segura.
42:22 - 42:27
Pero me citaron mañana a las nueve para hablar con el presidente de la compañía.
42:27 - 42:28
Pues le salió mamita, le salió.
42:28 - 42:31
Porque el presidente no la va a citar para decirle en la cara que no la va a recibir.
42:31 - 42:35
Ay gracias San Pancracio, gracias.
42:39 - 42:41
Mija, y ese trabajo de qué es.
42:41 - 42:46
Es como asistente de presidencia.
43:04 - 43:05
¿Por qué no le dijo que era de secretaria?
43:05 - 43:08
Usted conoce a mi papá, donde le diga que es para secretaria
43:08 - 43:09
no me deja hacerlo
43:09 - 43:12
me va a decir que para eso no me pagó un postgrado y una carrera
43:12 - 43:13
que siga buscando
43:13 - 43:15
No, si ellos me aceptan como secretaria, yo acepto.
43:15 - 43:17
Y después veo que hago con mi papá.
43:17 - 43:19
Felicitaciones Betty.
43:24 - 43:26
No acepto que me impongas a Patricia.
43:26 - 43:29
Lo único que quieres es resolverle el problema económico a Patricia
43:29 - 43:31
y montarme un policía a mi.
43:31 - 43:35
Una vigilante que esté dando cuenta detallada de cada uno de mis movimientos
43:35 - 43:36
de mis acciones, de mis llamadas, de todo
43:36 - 43:40
Eso no es así. Y si así fuera, ¿qué pasaría?
43:40 - 43:44
No disque ibas a cambiar cuando subieras a la presidencia
43:45 - 43:49
Tú me juraste cuando me pediste que me casara contigo
43:49 - 43:52
que no me preocupara que iba a encontrar en ti a un hombre
43:52 - 43:54
fiel, juicioso ¿cuál es el temor?
43:56 - 43:59
entonces ¿qué es lo que vas a hacer?
43:59 - 44:02
Marcela, a mi no me gusta que me estén vigilando todo el tiempo.
44:02 - 44:04
Bien, por algo será.
44:04 - 44:08
Patricia presentó la entrevista y la ganó limpiamente.
44:09 - 44:13
Tiene más estudio que cualquiera de las que se presentó aquí.
44:13 - 44:17
Tiene seis semestres en la San Marino, es bella, tiene clase, es una mujer de confianza
44:18 - 44:21
No hay otra alternativa.
44:22 - 44:23
En eso te equivocas.
44:23 - 44:25
Sí la ahí, y ya la cité.
44:26 - 44:30
Claro, ella no estudió 6 semestres de finanzas en la San Marino, no.
44:31 - 44:41
Ella en cambio se graduó en economía, con una tesis laureada, hizo un postgrado en finanzas, habla dos idiomas,
44:41 - 44:44
trabajo con el Banco de Montreal, maneja sistemas, en fin, para que te sigo numerando
44:44 - 44:46
las maravillas que ella hace
44:47 - 44:49
No, la mujer maravilla.
44:50 - 44:52
Pues de pronto no lo es, pero está bien.
44:52 - 44:53
Vamos a hacer un trato.
44:54 - 44:58
Yo simplemente la cité. Quiero hablar con ella y hacerle unas preguntas,
44:58 - 45:01
y si no me gusta listo contratamos a Patricia
45:01 - 45:05
¿Estás de acuerdo? Está bien
45:08 - 45:10
Perdóname
45:12 - 45:16
Aló, Carmencita ¿cómo está?
45:16 - 45:19
Cuénteme, ya llegó Beatriz Pinzón.
45:19 - 45:23
Sí señor, ya se la hago pasar.
45:23 - 45:27
Que siga por favor.
45:35 - 45:36
Siga por favor.
45:36 - 45:39
Gracias. Siéntese, siéntese
45:40 - 45:44
Buenos dias. Hola papá mira esta es la aspirante. De la que nos habló Gutierrez.
45:45 - 45:50
Ya, mucho gusto. Usted es la niña que trabajaba para Manuel José Becerra
45:50 - 45:52
en el Banco Montreal. ¿No es cierto?
45:52 - 45:56
Sí señor. Trabajé con él durante un año para el área internacional.
45:56 - 46:00
Ya. Gracias, siéntese por favor.
46:01 - 46:05
Trabajé con él durante un año en el área internacional mientras hacía un postgrado en finanzas.
46:06 - 46:10
Entré al Banco por recomendación del rector de la Universidad.
46:10 - 46:13
Sí, sí. De eso nos pudimos dar cuenta en la hoja de vida.
46:13 - 46:14
Tiene más que méritos para ser secretaria de presidencia.
46:14 - 46:18
Pero cuénteme una cosa, ¿usted sí conoce algo del mundo de la moda?
46:19 - 46:22
No, en realidad no. Pero conozco esta empresa.
46:23 - 46:26
Sé que es una de la de mayor crecimiento en el área de la confección.
46:26 - 46:32
Que tuvo ventas por más de 60.000 millones de pesos, tuvo una utilidad operacional de 10.000 millones y 4.000 millones de utilidad neta,
46:33 - 46:37
que cuenta con un patrimonio de alrededor de 50 millones de dólares
46:37 - 46:40
y que tiene 14 puntos de ventas en todo el país.
46:40 - 46:42
también sé que están exportando a varios países
46:42 - 46:45
y que hacen presencia constante en las ferias internacionales
46:45 - 46:46
un momento ... un momento señorita
46:46 - 46:48
¿de dónde saca usted todos esos datos?
46:48 - 46:51
Lo he leído en las revistas económicas
46:53 - 46:56
Yo no tengo experiencia en el mundo de la moda pero sé lo que
46:56 - 46:59
usted necesitaría y en lo que le podría ser útil
46:59 - 47:03
además de mis funciones como secretaria puedo llevarle un control presupuestal
47:03 - 47:05
puedo vigilar el movimiento bancario
47:05 - 47:09
manejo informática y también algunos programas de análisis como excell
47:09 - 47:12
ya ... ya ... tranquila nos imaginamos perfectamente
47:12 - 47:14
de que es capaz de hacer usted
47:14 - 47:16
sólo me queda una pregunta
47:16 - 47:19
¿usted está segura que quiere ser secretaria?
47:19 - 47:23
En una empresa como esta y con gente como ustedes sí.
47:23 - 47:28
Yo sé que puedo hacer un buen trabajo y quiero aprender de este sector de la economía
47:28 - 47:33
Además que a su lado puedo aprender mucho doctor.
47:37 - 47:39
Muy bien, de verdad, muy bien.
47:40 - 47:42
Nos dispensa un momento por favor.
47:42 - 47:44
Nos podría esperar afuera.
47:44 - 47:45
Claro, permiso.
47:45 - 47:46
Gracias.
47:48 - 47:52
Es más fea que Gutierrez, pero Marcela en todo caso esa mujer
47:52 - 47:53
está fuera de cualquier discusión
47:53 - 47:57
Te equivocas. No está libre de discusión.
47:57 - 48:01
Tiene muchas cualidades, pero no puede ser la secretaria de presidencia.
48:02 - 48:03
¿Por qué no?
48:03 - 48:07
Porque es muy fea. Ay Marcela que comentario tan femenino el tuyo
48:07 - 48:10
Ay Armando como si no te conocieramos.
48:10 - 48:12
O no te parece muy fea para ser la secretaria de presidencia
48:12 - 48:16
A ti quien te dijo que yo pedí una mujer bonita para secretaria
48:16 - 48:19
yo quiero alguien eficiente y esa mujer es la precisa
48:19 - 48:22
Eso no es suficiente. Afortunadamente Roberto está aquí
48:22 - 48:24
para que diga si tengo la razón o no.
48:24 - 48:28
Tú vas a ser el presidente de una casa de moda y una casa de moda debe reflejar
48:28 - 48:32
elegancia, sofisticación, belleza
48:32 - 48:34
Mira la secretaria de Roberto, Carmencita.
48:35 - 48:39
Si no es una modelo, es una mujer que tiene mucha presencia.
48:40 - 48:41
O me equivoco, Roberto.
48:42 - 48:46
Esta muchachita podría ser perfectamente la secretaria de una metalúrgica
48:46 - 48:50
Si tanto te impresionó su hoja de vida y si tiene tantas capacidades
48:50 - 48:53
porque no la pones en otro sitio, en otra oficina
48:53 - 48:55
pero en esta no, Armando.
48:55 - 48:57
No yo no tengo en donde más ubicarla.
48:58 - 49:02
Ah bueno como estamos de acuerdo que necesitas una mujer que tenga cierta presencia
49:02 - 49:06
aprovechando que Roberto está aquí y que tenemos que definir esto
49:07 - 49:11
me tomé el libertad de llamar a Patricia.
49:11 - 49:12
Patricia, ven.
49:16 - 49:17
Niña, venga.
49:18 - 49:21
Hola, Armando ¿cómo te ha ido? Roberto.
"""

# Create the SRT file using the flexible function
create_srt_file_flexible(input_text)
print("SRT file 'output.srt' created successfully, handling dates on separate lines!")