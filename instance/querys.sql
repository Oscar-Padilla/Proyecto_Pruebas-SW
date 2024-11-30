SELECT a.title, a.description, u.username, u.email 
FROM articles AS a
INNER JOIN users AS u ON a.user_id = u.id;


SELECT a.title, a.description, c.name AS "Categoria"
FROM articles AS a
INNER JOIN article_categories AS ac ON a.id = ac.article_id 
INNER JOIN categories AS c ON ac.category_id = c.id


SELECT a.title, u.username, ar.rating
FROM article_ratings AS ar
INNER JOIN articles AS a ON ar.article_id = a.id
INNER JOIN users AS u ON ar.user_id = u.id