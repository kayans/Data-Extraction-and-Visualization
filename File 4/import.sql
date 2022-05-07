# Copy noc_regions.csv
\copy noc_region from /Users/kayanshih/Downloads/homework08-kayans/data/noc_regions.csv with csv null as 'NA' header

# Copy athlete_events.csv
\copy athlete_event (id, name, sex, age, height, weight, team, noc, games, year, season, city, sport, event, medal) from /Users/kayanshih/Downloads/homework08-kayans/data/athlete_events.csv with csv null as 'NA' header