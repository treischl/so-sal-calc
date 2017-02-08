INSERT OR IGNORE INTO Salary (
    CountryId,
    PositionId,
    ExperienceId,
    SkillId,
    WithCity,
    IsPulled
)
SELECT *
FROM (
    SELECT Country.Id AS CountryId,
        Position.Id AS PositionId,
        Experience.Id AS ExperienceId,
        Skill.Id AS SkillId,
        0 AS WithCity,
        0 AS IsPulled
    FROM Country, Position, Experience, Skill
    UNION ALL
    SELECT Country.Id,
        Position.Id,
        Experience.Id,
        Skill.Id,
        1,
        0
    FROM Country, Position, Experience, Skill
    WHERE Country.HasCity = 1
)
ORDER BY CountryId, PositionId, ExperienceId, SkillId, WithCity