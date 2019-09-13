SELECT course_id, username, thread_id 
FROM forum_events
WHERE username IS NOT NULL AND thread_id IS NOT NULL AND forum_action = 'read'