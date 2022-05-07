DROP TABLE IF EXISTS athlete_event CASCADE;
DROP TABLE IF EXISTS noc_region;

CREATE TABLE noc_region (
	noc varchar(10) primary key, 
	region text,
	note text
);

CREATE TABLE athlete_event (
    athlete_event_id serial primary key,
	id integer, 
	name text,
	sex varchar(1),  
	age integer,
	height numeric,
	weight numeric,
	team text, 
	noc varchar(10),
	games text, 
	year integer, 
	season varchar(10),
	city text,
	sport text,
	event text,
	medal text
);

-- TODO: run the sql above and import data

-- example import using client side \copy (note relative paths)
-- \copy noc_region from noc_regions.csv with csv null as 'NA' header
-- \copy athlete_event (id, name, sex, age, height, weight, team, noc, games, year, season, city, sport, event, medal) from athlete_events.csv with csv null as 'NA' header
