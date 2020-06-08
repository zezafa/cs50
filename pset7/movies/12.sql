--SQL query to list the titles of all movies in which both Johnny Depp and Helena Bonham Carter starred

SELECT movies.title
FROM movies
    JOIN stars
        ON stars.movie_id = movies.id
    JOIN people
        ON people.id = stars.person_id
WHERE people.name = "Johnny Depp"
INTERSECT -- very cool
SELECT movies.title
FROM movies
    JOIN stars
        ON stars.movie_id = movies.id
    JOIN people
        ON people.id = stars.person_id
WHERE people.name = "Helena Bonham Carter";