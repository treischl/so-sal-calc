SELECT Salary.Id,
    Position.Value,
    Experience.Years,
    Skill.Level,
    Country.Value,
    Salary.WithCity
FROM Salary
JOIN Position ON Salary.PositionId = Position.Id
JOIN Experience ON Salary.ExperienceId = Experience.Id
JOIN Skill ON Salary.SkillId = Skill.Id
JOIN Country ON Salary.CountryId = Country.Id
WHERE Salary.IsPulled = 0
