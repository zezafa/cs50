SELECT DISTINCT name FROM people
    JOIN stars
        ON stars.person_id = people.id
WHERE stars.movie_id IN (SELECT stars.movie_id FROM stars WHERE stars.person_id = 102)
AND
people.name <> "Kevin Bacon";

