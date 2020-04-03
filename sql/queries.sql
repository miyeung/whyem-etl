-- In case of a tie between different organizations, they are all returned by the query
-- (DENSE_RANK() usage instead of RANK())

WITH top_organizations_by_profession AS (
    SELECT
        *,
        DENSE_RANK() OVER (
            PARTITION BY name
            ORDER BY total_candidates DESC
        ) rank_total_candidates
    FROM (
        SELECT
            professions.name,
            jobs.organization_reference,
            SUM(jobs.candidates)  AS total_candidates
        FROM
            public.jobs
        LEFT JOIN
            public.professions ON jobs.profession_id = professions.id
        GROUP BY
            professions.name,
            organization_reference
    ) candidates_by_profession_and_organization
)
SELECT
    *
FROM
    top_organizations_by_profession
WHERE
    rank_total_candidates <= 3
;
