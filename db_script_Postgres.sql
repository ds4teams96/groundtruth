CREATE TYPE _mt_dane_censo_2018 (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = mt_dane_censo_2018,
	DELIMITER = ',');

CREATE TYPE _mt_dane_estrato (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = mt_dane_estrato,
	DELIMITER = ',');

CREATE TYPE _mt_dane_geo (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = mt_dane_geo,
	DELIMITER = ',');

CREATE TYPE _mt_sentencia (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = mt_sentencia,
	DELIMITER = ',');

CREATE TYPE _tt_area (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_area,
	DELIMITER = ',');

CREATE TYPE _tt_carga_pdf (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_carga_pdf,
	DELIMITER = ',');

CREATE TYPE _tt_cedula_catastral (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_cedula_catastral,
	DELIMITER = ',');

CREATE TYPE _tt_encabezado (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_encabezado,
	DELIMITER = ',');

CREATE TYPE _tt_grupo_familiar (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_grupo_familiar,
	DELIMITER = ',');

CREATE TYPE _tt_indice_sentencia (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_indice_sentencia,
	DELIMITER = ',');

CREATE TYPE _tt_juez_magristrado (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_juez_magristrado,
	DELIMITER = ',');

CREATE TYPE _tt_localizacion (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_localizacion,
	DELIMITER = ',');

CREATE TYPE _tt_matricula_inmobiliaria (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_matricula_inmobiliaria,
	DELIMITER = ',');

CREATE TYPE _tt_model_predict (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_model_predict,
	DELIMITER = ',');

CREATE TYPE _tt_opositor (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_opositor,
	DELIMITER = ',');

CREATE TYPE _tt_ordena_beneficios (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_ordena_beneficios,
	DELIMITER = ',');

CREATE TYPE _tt_ordena_entidades (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_ordena_entidades,
	DELIMITER = ',');

CREATE TYPE _tt_radicado (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_radicado,
	DELIMITER = ',');

CREATE TYPE _tt_resuelve (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_resuelve,
	DELIMITER = ',');

CREATE TYPE _tt_resuelve_rest (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_resuelve_rest,
	DELIMITER = ',');

CREATE TYPE _tt_resuelve_text (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_resuelve_text,
	DELIMITER = ',');

CREATE TYPE _tt_sentencia_geo (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_sentencia_geo,
	DELIMITER = ',');

CREATE TYPE _tt_solicitante (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_solicitante,
	DELIMITER = ',');

CREATE TYPE _vw_pendiente_modelo (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = vw_pendiente_modelo,
	DELIMITER = ',');

CREATE TYPE _vw_rol_beneficiario (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = vw_rol_beneficiario,
	DELIMITER = ',');

CREATE TYPE _vw_tipo_sentencia_grupo (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = vw_tipo_sentencia_grupo,
	DELIMITER = ',');

CREATE TYPE _vw_tipo_zona (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = vw_tipo_zona,
	DELIMITER = ',');

CREATE TABLE public."BK_tt_radicado" (
	radicado text NULL,
	principal text NULL,
	"key" text NULL
);

CREATE TABLE public.mt_dane_censo_2018 (
	codane text NULL,
	departamento text NULL,
	municipio text NULL,
	total int4 NULL,
	hombre int4 NULL,
	mujer int4 NULL,
	sin_estrato int4 NULL,
	estrato_1 int4 NULL,
	estrato_2 int4 NULL,
	estrato_3 int4 NULL,
	estrato_4 int4 NULL,
	estrato_5 int4 NULL,
	estrato_6 int4 NULL,
	no_sabe int4 NULL,
	not_applicable int4 NULL,
	hombre_sin_estrato int4 NULL,
	hombre_estrato_1 int4 NULL,
	hombre_estrato_2 int4 NULL,
	hombre_estrato_3 int4 NULL,
	hombre_estrato_4 int4 NULL,
	hombre_estrato_5 int4 NULL,
	hombre_estrato_6 int4 NULL,
	hombre_no_sabe int4 NULL,
	hombre_not_applicable int4 NULL,
	mujer_sin_estrato int4 NULL,
	mujer_estrato_1 int4 NULL,
	mujer_estrato_2 int4 NULL,
	mujer_estrato_3 int4 NULL,
	mujer_estrato_4 int4 NULL,
	mujer_estrato_5 int4 NULL,
	mujer_estrato_6 int4 NULL,
	mujer_no_sabe int4 NULL,
	mujer_not_applicable int4 NULL
);

CREATE TABLE public.mt_dane_estrato (
	codane text NULL,
	departamento text NULL,
	municipio text NULL,
	total int4 NULL,
	sin_estrato int4 NULL,
	estrato_1 int4 NULL,
	estrato_2 int4 NULL,
	estrato_3 int4 NULL,
	estrato_4 int4 NULL,
	estrato_5 int4 NULL,
	estrato_6 int4 NULL,
	no_sabe int4 NULL
);

CREATE TABLE public.mt_dane_geo (
	codigo_dep text NULL,
	codigo_mun text NULL,
	codigo_cp text NULL,
	nombre_dep text NULL,
	nombre_mun text NULL,
	nombre_cp text NULL,
	tipo_cp text NULL,
	longitud float8 NULL,
	latitud float8 NULL,
	nombre_distrito text NULL,
	municipio_anm text NULL,
	nombre_area_metrop text NULL
);

CREATE TABLE public.mt_sentencia (
	certificado text NULL,
	clase text NULL,
	descargar text NULL,
	ciudad text NULL,
	estado text NULL,
	paginas text NULL,
	tipo_archivo text NULL
);

CREATE TABLE public.tt_area (
	"key" text NULL,
	area text NULL,
	conteo int8 NULL
);

CREATE TABLE public.tt_carga_pdf (
	"key" text NULL,
	probability float8 NULL,
	error_ratio float8 NULL,
	low_quality text NULL
);

CREATE TABLE public.tt_cedula_catastral (
	cedula_catastral text NULL,
	principal text NULL,
	"key" text NULL
);

CREATE TABLE public.tt_encabezado (
	"key" text NULL,
	clase text NULL,
	descripcion text NULL,
	fecha text NULL,
	fecha_formato text NULL
);

CREATE TABLE public.tt_grupo_familiar (
	grupo text NULL,
	n_persona text NULL,
	"name" text NULL,
	"key" text NULL,
	cedula text NULL
);

CREATE TABLE public.tt_indice_sentencia (
	"key" text NULL,
	numeral text NULL,
	texto text NULL,
	linea int4 NULL,
	tipo text NULL
);

CREATE TABLE public.tt_juez_magristrado (
	"key" text NULL,
	"index" int8 NULL,
	parte text NULL,
	original float8 NULL,
	nombre_jm text NULL,
	ponente int4 NULL,
	lead_sentence text NULL
);

CREATE TABLE public.tt_localizacion (
	certificado text NULL,
	departamento text NULL,
	codigo_departamento text NULL,
	municipio text NULL,
	codigo_municipio text NULL,
	corregimiento text NULL,
	codigo_corregimiento text NULL,
	vereda text NULL,
	codigo_vereda text NULL
);

CREATE TABLE public.tt_matricula_inmobiliaria (
	matricula_inmobiliaria text NULL,
	principal text NULL,
	"key" text NULL
);

CREATE TABLE public.tt_model_predict (
	accuracy float8 NULL,
	"precision" float8 NULL,
	sensitivity float8 NULL,
	specificity float8 NULL,
	f1_score float8 NULL,
	model text NULL,
	auc float8 NULL
);

CREATE TABLE public.tt_opositor (
	"key" text NULL,
	"index" int8 NULL,
	nombre_opositor text NULL,
	cedula text NULL
);

CREATE TABLE public.tt_ordena_beneficios (
	"key" text NULL,
	contador int8 NULL,
	beneficio text NULL
);

CREATE TABLE public.tt_ordena_entidades (
	"key" text NULL,
	contador int8 NULL,
	entidad text NULL
);

CREATE TABLE public.tt_radicado (
	certificado text NULL,
	radicacion text NULL,
	nombre_predio text NULL,
	municipio_vereda text NULL,
	fecha_providencia text NULL,
	id_despacho text NULL,
	despacho_judicial text NULL,
	anio text NULL,
	cantidad_sentencias text NULL,
	adiciona_complementa text NULL,
	fecha_ultima_sentencia text NULL
);

CREATE TABLE public.tt_resuelve (
	certificado text NULL,
	resuelve text NULL,
	radicado text NULL,
	orden_vivienda text NULL,
	proyectos_productivos_beneficiarios_restitucion text NULL,
	compensacion_victimas text NULL,
	compensacion_terceros text NULL,
	segundos_ocupantes text NULL,
	alivio_predial text NULL,
	alivio_servicios_publicos text NULL,
	alivio_pasivos_financieros text NULL,
	pagos_costas_gastos_judiciales text NULL,
	administracion_proyectos_productivos_agroindustriales text NULL,
	otras_ordenes text NULL,
	ordenes_direccion_social text NULL,
	ordenes_catastrales text NULL,
	usa_modelo text NULL DEFAULT 'NO'::text
);

CREATE TABLE public.tt_resuelve_text (
	"key" text NULL,
	contador int8 NULL,
	texto text NULL,
	orderna text NULL,
	beneficios text NULL,
	articulos text NULL
);

CREATE TABLE public.tt_sentencia_geo (
	"key" text NULL,
	latitud text NULL,
	longitud text NULL
);

CREATE TABLE public.tt_solicitante (
	nombre text NULL,
	principal int8 NULL,
	"key" text NULL,
	cedula int8 NULL
);

CREATE OR REPLACE VIEW public.vw_rol_beneficiario
AS SELECT tgf.grupo,
    tgf.n_persona,
    tgf.name,
    tgf.key,
    tgf.cedula,
        CASE
            WHEN tgf.n_persona = '1'::text THEN 'Titular'::text
            ELSE 'Beneficiario'::text
        END AS rol
   FROM tt_grupo_familiar tgf;

CREATE OR REPLACE VIEW public.vw_tipo_sentencia_grupo
AS SELECT tmp_grp.key,
        CASE
            WHEN tmp_grp.c_grupos = '1'::text THEN 'Individual'::text
            ELSE 'Colectiva'::text
        END AS tipo
   FROM ( SELECT tgf.key,
            max(tgf.grupo) AS c_grupos
           FROM tt_grupo_familiar tgf
          GROUP BY tgf.key) tmp_grp;

CREATE OR REPLACE VIEW public.vw_tipo_zona
AS SELECT tl.certificado,
    tl.codigo_vereda,
    tmp_dane_cp.tipo_cp,
        CASE
            WHEN tl.codigo_vereda IS NOT NULL AND tl.codigo_vereda <> 'Not Found'::text THEN 'Rural'::text
            WHEN tmp_dane_cp.tipo_cp IS NOT NULL THEN
            CASE
                WHEN tmp_dane_cp.tipo_cp = 'CENTRO POBLADO'::text THEN 'Rural'::text
                WHEN tmp_dane_cp.tipo_cp = 'CABECERA MUNICIPAL'::text THEN 'Urbano'::text
                ELSE 'Rural (Probable)'::text
            END
            ELSE 'Rural (Probable)'::text
        END AS tipo
   FROM tt_localizacion tl
     LEFT JOIN ( SELECT DISTINCT mt_dane_geo.codigo_cp,
            mt_dane_geo.tipo_cp
           FROM mt_dane_geo) tmp_dane_cp ON tmp_dane_cp.codigo_cp = tl.codigo_corregimiento;

CREATE OR REPLACE VIEW public.vw_pendiente_modelo 
AS SELECT * 
FROM tt_resuelve
WHERE 
	(orden_vivienda is null or orden_vivienda = '') and
	(proyectos_productivos_beneficiarios_restitucion is null or proyectos_productivos_beneficiarios_restitucion = '') and
	(compensacion_victimas is null or compensacion_victimas = '') and
	(compensacion_terceros is null or compensacion_terceros = '') and
	(segundos_ocupantes is null or segundos_ocupantes = '') and
	(alivio_predial is null or alivio_predial = '') and
	(alivio_servicios_publicos is null or alivio_servicios_publicos = '') and
	(alivio_pasivos_financieros is null or alivio_pasivos_financieros = '') and
	(pagos_costas_gastos_judiciales is null or pagos_costas_gastos_judiciales = '') and
	(administracion_proyectos_productivos_agroindustriales is null or administracion_proyectos_productivos_agroindustriales = '') and
	(otras_ordenes is null or otras_ordenes = '') and
	(ordenes_direccion_social is null or ordenes_direccion_social = '') and
	(ordenes_catastrales is null or ordenes_catastrales = '')