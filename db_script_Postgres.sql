CREATE SCHEMA public AUTHORIZATION postgres;

CREATE TYPE _BK2_mt_sentencia (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = BK2_mt_sentencia,
	DELIMITER = ',');

CREATE TYPE _BK_mt_sentencia (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = BK_mt_sentencia,
	DELIMITER = ',');

CREATE TYPE _BK_mt_sentencia_region (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = BK_mt_sentencia_region,
	DELIMITER = ',');

CREATE TYPE _BK_tt_antecedente (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = BK_tt_antecedente,
	DELIMITER = ',');

CREATE TYPE _BK_tt_encabezado (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = BK_tt_encabezado,
	DELIMITER = ',');

CREATE TYPE _BK_tt_radicado (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = BK_tt_radicado,
	DELIMITER = ',');

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

CREATE TYPE _mt_sentencia_rest (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = mt_sentencia_rest,
	DELIMITER = ',');

CREATE TYPE _temp_new_resuelve (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = temp_new_resuelve,
	DELIMITER = ',');

CREATE TYPE _temp_test_resuelve (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = temp_test_resuelve,
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

CREATE TYPE _tt_log_transaccion (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_log_transaccion,
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

CREATE TYPE _tt_radicado_rest (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = tt_radicado_rest,
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

CREATE TYPE _vw_certificado_radicacion_finalizado (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = vw_certificado_radicacion_finalizado,
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

CREATE TYPE _vw_sentencia (
	INPUT = array_in,
	OUTPUT = array_out,
	RECEIVE = array_recv,
	SEND = array_send,
	ANALYZE = array_typanalyze,
	ALIGNMENT = 8,
	STORAGE = any,
	CATEGORY = A,
	ELEMENT = vw_sentencia,
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

CREATE TABLE mt_dane_censo_2018 (
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
	mujer_not_applicable int4 NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE mt_dane_estrato (
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
	no_sabe int4 NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE mt_dane_geo (
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
	nombre_area_metrop text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE mt_sentencia (
	certificado text NULL,
	clase text NULL,
	descargar text NULL,
	ciudad text NULL,
	estado text NULL DEFAULT 'Nuevo'::text,
	paginas text NULL,
	tipo_archivo text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_area (
	"key" text NULL,
	area text NULL,
	conteo int8 NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_carga_pdf (
	"key" text NULL,
	probability float8 NULL,
	error_ratio float8 NULL,
	low_quality text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_cedula_catastral (
	cedula_catastral text NULL,
	principal text NULL,
	"key" text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_encabezado (
	"key" text NULL,
	clase text NULL,
	descripcion text NULL,
	fecha text NULL,
	fecha_formato text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_grupo_familiar (
	grupo text NULL,
	n_persona text NULL,
	"name" text NULL,
	"key" text NULL,
	cedula text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_indice_sentencia (
	"key" text NULL,
	numeral text NULL,
	texto text NULL,
	linea int4 NULL,
	tipo text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_juez_magristrado (
	"key" text NULL,
	"index" int8 NULL,
	parte text NULL,
	original float8 NULL,
	nombre_jm text NULL,
	ponente int4 NULL,
	lead_sentence text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_localizacion (
	certificado text NULL,
	departamento text NULL,
	codigo_departamento text NULL,
	municipio text NULL,
	codigo_municipio text NULL,
	corregimiento text NULL,
	codigo_corregimiento text NULL,
	vereda text NULL,
	codigo_vereda text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_log_transaccion (
	operacion text NULL,
	comentario text NULL DEFAULT ''::text,
	fecha timestamp NULL DEFAULT now()
);

CREATE TABLE tt_matricula_inmobiliaria (
	matricula_inmobiliaria text NULL,
	principal text NULL,
	"key" text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_model_predict (
	accuracy float8 NULL,
	"precision" float8 NULL,
	sensitivity float8 NULL,
	specificity float8 NULL,
	f1_score float8 NULL,
	model text NULL,
	auc float8 NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_opositor (
	"key" text NULL,
	"index" int8 NULL,
	nombre_opositor text NULL,
	cedula text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_ordena_beneficios (
	"key" text NULL,
	contador int8 NULL,
	beneficio text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_ordena_entidades (
	"key" text NULL,
	contador int8 NULL,
	entidad text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_radicado (
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
	fecha_ultima_sentencia text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_resuelve (
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
	usa_modelo text NULL DEFAULT 'NO'::text,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_resuelve_text (
	"key" text NULL,
	contador int8 NULL,
	texto text NULL,
	orderna text NULL,
	beneficios text NULL,
	articulos text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_sentencia_geo (
	"key" text NULL,
	latitud text NULL,
	longitud text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE TABLE tt_solicitante (
	nombre text NULL,
	principal int8 NULL,
	"key" text NULL,
	cedula text NULL,
	fecha_creacion_registro timestamp NULL DEFAULT now()
);

CREATE OR REPLACE VIEW public.vw_certificado_radicacion_finalizado
AS SELECT ms.certificado AS "Certificado",
    tr.radicacion AS "Radicación"
   FROM mt_sentencia ms
     JOIN tt_radicado tr ON tr.certificado = ms.certificado;

CREATE OR REPLACE VIEW public.vw_pendiente_modelo
AS SELECT tt_resuelve.certificado,
    tt_resuelve.resuelve,
    tt_resuelve.radicado,
    tt_resuelve.orden_vivienda,
    tt_resuelve.proyectos_productivos_beneficiarios_restitucion,
    tt_resuelve.compensacion_victimas,
    tt_resuelve.compensacion_terceros,
    tt_resuelve.segundos_ocupantes,
    tt_resuelve.alivio_predial,
    tt_resuelve.alivio_servicios_publicos,
    tt_resuelve.alivio_pasivos_financieros,
    tt_resuelve.pagos_costas_gastos_judiciales,
    tt_resuelve.administracion_proyectos_productivos_agroindustriales,
    tt_resuelve.otras_ordenes,
    tt_resuelve.ordenes_direccion_social,
    tt_resuelve.ordenes_catastrales,
    tt_resuelve.usa_modelo
   FROM tt_resuelve
  WHERE (tt_resuelve.orden_vivienda IS NULL OR tt_resuelve.orden_vivienda = ''::text) AND (tt_resuelve.proyectos_productivos_beneficiarios_restitucion IS NULL OR tt_resuelve.proyectos_productivos_beneficiarios_restitucion = ''::text) AND (tt_resuelve.compensacion_victimas IS NULL OR tt_resuelve.compensacion_victimas = ''::text) AND (tt_resuelve.compensacion_terceros IS NULL OR tt_resuelve.compensacion_terceros = ''::text) AND (tt_resuelve.segundos_ocupantes IS NULL OR tt_resuelve.segundos_ocupantes = ''::text) AND (tt_resuelve.alivio_predial IS NULL OR tt_resuelve.alivio_predial = ''::text) AND (tt_resuelve.alivio_servicios_publicos IS NULL OR tt_resuelve.alivio_servicios_publicos = ''::text) AND (tt_resuelve.alivio_pasivos_financieros IS NULL OR tt_resuelve.alivio_pasivos_financieros = ''::text) AND (tt_resuelve.pagos_costas_gastos_judiciales IS NULL OR tt_resuelve.pagos_costas_gastos_judiciales = ''::text) AND (tt_resuelve.administracion_proyectos_productivos_agroindustriales IS NULL OR tt_resuelve.administracion_proyectos_productivos_agroindustriales = ''::text) AND (tt_resuelve.otras_ordenes IS NULL OR tt_resuelve.otras_ordenes = ''::text) AND (tt_resuelve.ordenes_direccion_social IS NULL OR tt_resuelve.ordenes_direccion_social = ''::text) AND (tt_resuelve.ordenes_catastrales IS NULL OR tt_resuelve.ordenes_catastrales = ''::text);

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
