with jobs as (
    select * from {{ ref('jobs') }}
),

professions as (
    select * from {{ ref('professions') }}
),

number_of_applications_by_profession_and_organization as (
    select
        professions.name,
        jobs.organization_reference,
        SUM(jobs.candidates)  as total_candidates
    from
        jobs
    left join
        professions on jobs.profession_id = professions.id
    group by
        professions.name,
        organization_reference
),

-- In case of a tie between different organizations, ie for the same professions
-- and organization we have the same number of applicants, both are returned
-- (DENSE_RANK() usage instead of RANK())
ranked_number_of_applications_by_profession_and_organization as (
    select *,
    dense_rank() over (
        partition by name
        order by total_candidates desc
    ) rank_total_candidates
    from number_of_applications_by_profession_and_organization
),

top3_popular_organizations_by_professions as (
    select *
    from ranked_number_of_applications_by_profession_and_organization
    where rank_total_candidates <= 3
)

select * from top3_popular_organizations_by_professions
