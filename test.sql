-- ======================================================
-- 1️⃣ Create or update the summary view
-- Must be first statement in batch
-- ======================================================
GO
CREATE OR ALTER VIEW student_services_summary AS
SELECT s.grade_level,
       sv.service_name,
       COUNT(*) AS num_students
FROM students AS s
JOIN services AS sv
    ON s.service_code = sv.service_code
GROUP BY s.grade_level, sv.service_name;
GO

-- ======================================================
-- 2️⃣ View all students and their services
-- ======================================================
GO
SELECT s.student_id,
       s.first_name,
       s.last_name,
       sv.service_name
FROM students AS s
JOIN services AS sv
    ON s.service_code = sv.service_code
ORDER BY s.student_id;
GO

-- ======================================================
-- 3️⃣ Count services per student
-- ======================================================
GO
SELECT s.student_id,
       s.first_name,
       s.last_name,
       CASE 
           WHEN s.service_code IS NULL THEN 0
           ELSE 1
       END AS total_services
FROM students AS s
ORDER BY total_services DESC;
GO

-- ======================================================
-- 4️⃣ Count students per service (all grades)
-- ======================================================
GO
SELECT sv.service_name,
       COUNT(*) AS num_students
FROM students AS s
JOIN services AS sv
    ON s.service_code = sv.service_code
GROUP BY sv.service_name
ORDER BY num_students DESC;
GO

-- ======================================================
-- 5️⃣ Use the view for grade-level summary
-- ======================================================
GO
SELECT *
FROM student_services_summary
ORDER BY grade_level, service_name;
GO
