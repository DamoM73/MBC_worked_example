SELECT p.state, SUM(i.units)
FROM Postcode p
JOIN Installs i
ON p.postcode = i.postcode
WHERE i.year = 2018
GROUP BY p.state
ORDER BY SUM(i.units) DESC