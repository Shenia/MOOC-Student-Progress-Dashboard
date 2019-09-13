SELECT course_id, ID_TABLE.user_id, ID_TABLE.username, quizzes.numCompleted AS numQuizzesCompleted, numQuizzesAvailable, timeliness as quizTimeliness, numVidUnique, numVidUniqueWatched, numVidRewatches, availableQuizzes.module
FROM
    (SELECT course_id, user_id, username 
    FROM person_course
    WHERE completed = true) as ID_TABLE

CROSS JOIN

    (SELECT count(*) as numQuizzesAvailable, p.module
    FROM (SELECT distinct(vertical_name), 
            CASE 
                WHEN course_item.vertical_name LIKE '%Module%1%Quiz' THEN 1
                WHEN course_item.vertical_name LIKE '%Module%2%Quiz' THEN 2
                WHEN course_item.vertical_name LIKE '%Module%3%Quiz' THEN 3
                WHEN course_item.vertical_name LIKE '%Module%4%Quiz' THEN 4
            END AS module
            FROM course_item) AS p
    WHERE p.module IS NOT NULL
    GROUP BY p.module) AS availableQuizzes

LEFT JOIN
    
    (SELECT count(*) AS numVidUnique,
        CASE
            WHEN chapter_name LIKE '%1:%' THEN 1
            WHEN chapter_name LIKE '%2:%' THEN 2
            WHEN chapter_name LIKE '%3:%' THEN 3
            WHEN chapter_name LIKE '%4:%' THEN 4
        END AS module
    FROM video_axis AS video_axis
    GROUP BY module) AS availableVideos

ON availableVideos.module = availableQuizzes.module

LEFT JOIN

    (SELECT user_id, numCompleted, timeliness, module
    FROM(SELECT user_id, 
            count(distinct vertical_name) as numCompleted, 
            avg(timestamp_diff(course_item.due_date, person_problem.date, hour)) as timeliness,
            CASE 
                WHEN course_item.vertical_name LIKE '%Module%1%Quiz' THEN 1
                WHEN course_item.vertical_name LIKE '%Module%2%Quiz' THEN 2
                WHEN course_item.vertical_name LIKE '%Module%3%Quiz' THEN 3
                WHEN course_item.vertical_name LIKE '%Module%4%Quiz' THEN 4
            END AS module  
        FROM course_item as course_item, 
            person_problem as person_problem 
        WHERE course_item.problem_nid = person_problem.problem_nid
        GROUP BY person_problem.user_id, module) AS q
    WHERE module IS NOT NULL) as quizzes   

ON ID_TABLE.user_id = quizzes.user_id AND availableQuizzes.module = quizzes.module

LEFT JOIN

    (SELECT username, 
        CASE
            WHEN video_axis.chapter_name LIKE '%1:%' THEN 1
            WHEN video_axis.chapter_name LIKE '%2:%' THEN 2
            WHEN video_axis.chapter_name LIKE '%3:%' THEN 3
            WHEN video_axis.chapter_name LIKE '%4:%' THEN 4
        END AS module,
        count(distinct video_stats_day.video_id) as numVidUniqueWatched
    FROM video_stats_day AS video_stats_day, video_axis AS video_axis
    WHERE video_stats_day.video_id = video_axis.video_id 
    GROUP BY username, module) AS videos

ON ID_TABLE.username = videos.username AND availableVideos.module = videos.module

LEFT JOIN

        (SELECT username, (count(*) - count(distinct v1.video_id)) as numVidRewatches, 
            CASE 
                WHEN video_axis.chapter_name LIKE '%1:%' THEN 1
                WHEN video_axis.chapter_name LIKE '%2:%' THEN 2
                WHEN video_axis.chapter_name LIKE '%3:%' THEN 3
                WHEN video_axis.chapter_name LIKE '%4:%' THEN 4
            END AS module
        FROM video_stats_day AS v1, video_axis AS video_axis
        WHERE EXISTS (SELECT * 
                        FROM video_stats_day as v2 
                        WHERE v2.date <> v1.date AND v2.username = v1.username AND v2.video_id = v1.video_id) 
                AND video_axis.video_id = v1.video_id
        GROUP BY username, chapter_name) AS rewatchesByPerson

ON ID_TABLE.username = rewatchesByPerson.username AND availableVideos.module = rewatchesByPerson.module