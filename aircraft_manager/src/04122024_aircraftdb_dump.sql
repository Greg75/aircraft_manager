--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: aircrafttype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.aircrafttype AS ENUM (
    'Fighter',
    'Striker',
    'Bomber',
    'Trainer'
);


ALTER TYPE public.aircrafttype OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: aircrafts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aircrafts (
    aircraft_id integer NOT NULL,
    name character varying NOT NULL,
    manufacturer character varying NOT NULL,
    aircraft_type character varying,
    first_flight character varying
);


ALTER TABLE public.aircrafts OWNER TO postgres;

--
-- Name: aircrafts_aircraft_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.aircrafts_aircraft_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.aircrafts_aircraft_id_seq OWNER TO postgres;

--
-- Name: aircrafts_aircraft_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.aircrafts_aircraft_id_seq OWNED BY public.aircrafts.aircraft_id;


--
-- Name: aircrafts_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aircrafts_data (
    aircraft_data_id integer NOT NULL,
    fuel_consumption integer,
    ceiling integer,
    weight integer,
    fuel integer,
    take_off_weight integer,
    aircraft_id integer NOT NULL,
    max_speed integer,
    cruise_speed integer
);


ALTER TABLE public.aircrafts_data OWNER TO postgres;

--
-- Name: aircrafts_data_aircraft_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.aircrafts_data_aircraft_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.aircrafts_data_aircraft_data_id_seq OWNER TO postgres;

--
-- Name: aircrafts_data_aircraft_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.aircrafts_data_aircraft_data_id_seq OWNED BY public.aircrafts_data.aircraft_data_id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: aircrafts aircraft_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aircrafts ALTER COLUMN aircraft_id SET DEFAULT nextval('public.aircrafts_aircraft_id_seq'::regclass);


--
-- Name: aircrafts_data aircraft_data_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aircrafts_data ALTER COLUMN aircraft_data_id SET DEFAULT nextval('public.aircrafts_data_aircraft_data_id_seq'::regclass);


--
-- Data for Name: aircrafts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aircrafts (aircraft_id, name, manufacturer, aircraft_type, first_flight) FROM stdin;
1	C-152	Cessna	Trainer	1972-08-13
2	C-172	Cessna	Trainer	1976-06-18
3	3XTrim	Krosno	Trainer	1999-05-18
4	PZL-130	PZL Mielec	Trainer	1992-04-30
\.


--
-- Data for Name: aircrafts_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.aircrafts_data (aircraft_data_id, fuel_consumption, ceiling, weight, fuel, take_off_weight, aircraft_id, max_speed, cruise_speed) FROM stdin;
4	48	6000	1825	560	2217	4	480	300
3	12	2400	450	55	489	3	190	120
1	15	2800	750	120	834	1	270	190
2	18	3200	880	150	985	2	300	220
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
6d3d857e341e
\.


--
-- Name: aircrafts_aircraft_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.aircrafts_aircraft_id_seq', 4, true);


--
-- Name: aircrafts_data_aircraft_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.aircrafts_data_aircraft_data_id_seq', 4, true);


--
-- Name: aircrafts_data aircrafts_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aircrafts_data
    ADD CONSTRAINT aircrafts_data_pkey PRIMARY KEY (aircraft_data_id);


--
-- Name: aircrafts aircrafts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aircrafts
    ADD CONSTRAINT aircrafts_pkey PRIMARY KEY (aircraft_id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- PostgreSQL database dump complete
--

