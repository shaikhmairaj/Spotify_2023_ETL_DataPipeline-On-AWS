-- SQL QUERY FOR SPOTIFY DATASET-2023

SELECT * FROM datawarehouse limit 10;

SELECT followers FROM datawarehouse;

SELECT artist_4 FROM datawarehouse;

SELECT *
FROM datawarehouse
ORDER BY followers DESC
LIMIT 10;

SELECT popularity, COUNT(*) AS count
FROM tracks
GROUP BY popularity
ORDER BY popularity;

SELECT album_type, COUNT(*) AS total
FROM albums
GROUP BY album_type
ORDER BY total DESC;

SELECT name, duration_ms
FROM tracks
ORDER BY duration_ms DESC
LIMIT 10;

SELECT ar.name AS artist_name, AVG(t.popularity) AS avg_popularity
FROM tracks t
JOIN albums a ON t.album_id = a.id
JOIN artists ar ON a.artist_id = ar.id
GROUP BY ar.name
ORDER BY avg_popularity DESC
LIMIT 10;


