SELECT name
FROM Suburb
WHERE postcode IN (
	SELECT postcode
	FROM Installs
	GROUP BY postcode
	ORDER BY SUM(units) DESC
	LIMIT 1)