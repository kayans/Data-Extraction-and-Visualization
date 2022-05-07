-- TODO: write the task number and description followed by the query

# 1. Write a View

CREATE VIEW event_region AS
SELECT n.region, a.event, a.year, a.height, a.medal FROM noc_region n
INNER JOIN athlete_event a on n.noc=a.noc;

# 2. Use the Window Function, rank(): Show the top 3 ranked regions for each fencing 🤺 event based on the number of total gold medals 🥇 that region had for that fencing event

CREATE VIEW gold_count AS
WITH fencing_gold AS
(SELECT region, event, medal FROM event_region
WHERE medal ILIKE 'gold' AND event ILIKE '%fencing%')
SELECT region, event, COUNT(*) FROM fencing_gold
GROUP BY region, event;

SELECT region, event, count as gold_medals, rank() over (partition by event order by count desc) as rank FROM gold_count;

# 3. Using Aggregate Functions as Window Functions: Show the rolling sum of medals per region, per year, and per medal type.

SELECT region, year, medal, COUNT(*) AS c, SUM(COUNT(*)) OVER (PARTITION BY region, medal ORDER BY year) FROM event_region
GROUP BY region, year, medal
HAVING medal is NOT NULL
ORDER BY region, year, medal
LIMIT 10;

# 4. Use the Window Function, lag(): Show the height of every gold medalist for pole valut events, along with the height of the gold medalist for that same pole value event in the previous year.

WITH polevalut_gold AS
(SELECT event, year, height FROM event_region
WHERE medal ILIKE 'gold' AND event ILIKE '%vault%')
SELECT event, year, height, LAG(height, 1) OVER(PARTITION BY event ORDER BY year) as previous_height FROM polevalut_gold;
