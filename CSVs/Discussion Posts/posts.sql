SELECT course_id, username, slug_type, slug_id, thread_id, title 
FROM forum_posts
WHERE username IS NOT NULL AND title IS NOT NULL AND slug_id IS NOT NULL