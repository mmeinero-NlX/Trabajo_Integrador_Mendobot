from sqlalchemy import select
from models import create_tables, get_session, Location, Career, Subject

#                                       DATA

# (id, name, city, address)
locations = [
    (1, "Sede Regional Río Cuarto", "Río Cuarto", "Belgrano esq. Hipólito Yrigoyen"),
    (2, "Sede Central", "Mendoza", "Boulogne Sur Mer 683"),
    (3, "Sede Regional San Rafael", "San Rafael", "Bernardo de Irigoyen y España"),
]

# (id, code, name, mode, duration_years, location_id)
careers = [
    (1, "TDS", "Tecnicatura en Desarrollo de Software", "presencial", 3, 1),
    (2, "AU", "Arquitectura y Urbanismo", "presencial", 5, 1),
    (3, "DG", "Diseño Gráfico", "presencial", 3, 1),
    (4, "LK", "Licenciatura en Kinesiología", "a distancia", 5, 1),
    (5, "CIyMP", "Corredor Inmobiliario y Martillero Público", "presencial", 3, 2),
]

subjects = [
        # Tecnicatura en desarrollo de software
    # Primer año
    (1, "Matematica Discreta y Diseño Logico",  1,1),
    (2, "Analisis de Sistemas 1",               1,1),
    (3, "Álgebra y Geometria Analitica",        1,1),
    (4, "Ingles Técnico",                       1,1),
    (5, "Informática",                          1,1),

        # Corredor Inmobiliario y Martillero Público
    # Primer año
    (6, "Comunicación 1 (Psicología Social Básica)",    1, 5),
    (7, "Corretaje 1 (Contexto Ocupacional)",           1, 5),
    (8, "Derecho 1 (Propedéutica Jurídica)",            1, 5),
    (9, "Diseño 1 (Logística Disciplinar)",             1, 5),
    (10, "Idioma 1 (Inglés Básico)",                    1, 5),
    (11, "Inmobiliario 1 (Valoración Edilicia)",        1, 5),
    (12, "Marketing 1 (Posicionamiento)",               1, 5),
    (13, "Valuación 1 (Técnicas Operacionales)",        1, 5),
    (14, "Práctica Integrada 1 (Módulo Introductorio)", 1, 5),
    # Segundo año
    (15, "Comunicación 2 (Psicología Social Aplicada)",    2, 5),
    (16, "Corretaje 2 (Gestión de Negocios)",              2, 5),
    (17, "Derecho 2 (Logística Jurídica)",                 2, 5),
    (18, "Diseño 2 (Intermediación Creativa)",             2, 5),
    (19, "Idioma 2 (Inglés Aplicado)",                     2, 5),
    (20, "Inmobiliario 2 (Desarrollo Urbano)",             2, 5),
    (21, "Marketing 2 (Riesgos Inmobiliarios)",            2, 5),
    (22, "Valuación 2 (Técnicas Procesales)",              2, 5),
    (23, "Práctica Integrada 2 (Módulo Instrumental)",     2, 5),
    # Tercer año
    (24, "Comunicación 3 (Oratoria)",                      3, 5),
    (25, "Derecho 3 (Procesal)",                           3, 5),
    (26, "Diseño 3 (Organizacional)",                      3, 5),
    (27, "Gestión 3 (Jurídica)",                           3, 5),
    (28, "Marketing 3 (Remate)",                           3, 5),
    (29, "Práctica Integrada 3",                           3, 5),
    (30, "Prácticas",                                      3, 5),

        # Licenciatura en kinesiologia
    # Primer año
    (31, "Anatomía",                                       1, 4),
    (32, "Fisiología",                                     1, 4),
    (33, "Histología",                                     1, 4),
    (34, "Física Biológica",                               1, 4),
    (35, "Inglés I (Promocional)",                         1, 4),
    (36, "Seminario I (Bioquímica)",                       1, 4),
    # Segundo año
    (37, "Biomecánica",                                    2, 4),
    (38, "Semiopatología Médico Kinésica",                 2, 4),
    (39, "Kinefilaxia",                                    2, 4),
    (40, "Inglés II (Promocional)",                        2, 4),
    (41, "Órtesis y Prótesis",                             2, 4),
    (42, "Psicomotricidad",                                2, 4),
    (43, "Seminario II (Diagnóstico por Imagen)",          2, 4),
    # Tercer año
    (44, "Semiopatología Quirúrgico Kinésica",             3, 4),
    (45, "Kinesiología Médica",                            3, 4),
    (46, "Fisioterapia",                                   3, 4),
    (47, "Inglés III (Promocional)",                       3, 4),
    (48, "Kinefisiatría Estética",                         3, 4),
    (49, "Bioinformática y Rehabilitación Computacional",  3, 4),
    (50, "Seminario III (Neurología)",                     3, 4),
    # Cuarto año
    (51, "Kinesiología Quirúrgica",                                             4, 4),
    (52, "Kinesiología Legal",                                                  4, 4),
    (53, "Deportismo",                                                          4, 4),
    (54, "Inglés IV (Promocional)",                                             4, 4),
    (55, "Farmacología Electrofisiokinésica",                                   4, 4),
    (56, "Organización Hospitalaria Institucional y Centros de Rehabilitación", 4, 4),
    (57, "Kinefisiatría Ocupacional y Laboral",                                 4, 4),
    (58, "Metodología de la Investigación",                                     4, 4),
    (59, "Seminario IV (Prácticas Profesionales)",                              4, 4),

        # Diseño Grafico
    # Primer año
    (60, "Dibujo y Expresión Visual I",                 1, 3),
    (61, "Dibujo y Expresión Visual II",                1, 3),
    (62, "Informática I",                               1, 3),
    (63, "Informática II",                              1, 3),
    (64, "Taller de Introducción al Diseño I",          1, 3),
    (65, "Taller de Introducción al Diseño II",         1, 3),
    # Segundo año
    (66, "Materialización I",                           2, 3),
    (67, "Materialización II",                          2, 3),
    (68, "Taller de Diseño Integral I",                 2, 3),
    (69, "Taller de Diseño Integral II",                2, 3),
    # Tercer año
    (70, "Introducción a la Investigación",             3, 3),
    (71, "Opcional Específica I (Diseño Editorial)",    3, 3),
    (72, "Opcional Específica II",                      3, 3),
    (73, "Taller Especial de Diseño I",                 3, 3),
    (74, "Taller Especial de Diseño II",                3, 3),
    (75, "Presentación Final",                          3, 3),

        # Arquitectura y Urbanismo
    # Primer año
    (76, "Arquitectura 1",                                    1, 2),
    (77, "Construcciones 1",                                  1, 2),
    (78, "Cultura Arquitectónica",                            1, 2),
    (79, "Dibujo y Expresión",                                1, 2),
    (80, "Estructuras 1",                                     1, 2),
    (81, "Matemáticas",                                       1, 2),
    (82, "Sistemas de Representación",                        1, 2),
    # Segundo año
    (83, "Ambiente 1",                                        2, 2),
    (84, "Arquitectura 2",                                    2, 2),
    (85, "Construcciones 2",                                  2, 2),
    (86, "Estructuras 2",                                     2, 2),
    (87, "Historia de la Arquitectura y el Urbanismo 1",      2, 2),
    (88, "Teoría de la Arquitectura y el Urbanismo 1",        2, 2),
    # Tercer año
    (89, "Ambiente 2",                                        3, 2),
    (90, "Arquitectura 3",                                    3, 2),
    (91, "Construcciones 3",                                  3, 2),
    (92, "Estructuras 3",                                     3, 2),
    (93, "Historia de la Arquitectura y el Urbanismo 2",      3, 2),
    (94, "Teoría de la Arquitectura y el Urbanismo 2",        3, 2),
    # Cuarto año
    (95, "Ambiente 3",                                        4, 2),
    (96, "Arquitectura 4",                                    4, 2),
    (97, "Construcciones 4",                                  4, 2),
    (98, "Estructuras 4",                                     4, 2),
    (99, "Historia de la Arquitectura y el Urbanismo 3",      4, 2),
    (100, "Teoría de la Arquitectura y el Urbanismo 3",       4, 2),
    # Quinto año
    (101, "Arquitectura 5",                                    5, 2),
    (102, "Organización, Administración y Legislación",        5, 2),
    (103, "Practicantado",                                     5, 2),
    (104, "Proyectos Inmobiliarios",                           5, 2),
    (105, "Urbanismo",                                         5, 2),
    (106, "Proyecto Final",                                    5, 2),
    (107, "Proyecto Final (Primer Tramo)",                     5, 2),
    (108, "Proyecto Final (Segundo Tramo)",                    5, 2),
    # Optativas: el plan las ubica en 5º año
    (109, "Diseño Arquitectónico (Optativa)",                  5, 2),
    (110, "Diseño Urbano (Optativa)",                          5, 2),
    (111, "Marketing para Arquitectos (Optativa)",             5, 2),
]


#                                           SEED

def seed():
    create_tables()
    with get_session() as s:
        if s.scalars(select(Location)).first() is not None:
            print("The database already has data.")
            return
        
        # 1) parents first: locations
        for id, name, city, address in locations:
            s.add(Location(id=id, name=name, city=city, address=address))
        s.commit()

        # 2) careers (they point to a location)
        for id, code, name, mode, duration_years, location_id in careers:
            s.add(Career(id=id, code=code, name=name, mode=mode, duration_years=duration_years, location_id=location_id))
        s.commit()

        # 3) subjects (they point to a career)
        for id, name, year, career_id in subjects:
            s.add(Subject(id=id, name=name, year=year, career_id=career_id))
        s.commit()

        print("Data loaded.")

if __name__ == "__main__":
    seed()