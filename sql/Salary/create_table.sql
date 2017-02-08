CREATE TABLE IF NOT EXISTS Salary (
    Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    CountryId INTEGER NOT NULL,
    PositionId INTEGER NOT NULL,
    ExperienceId INTEGER NOT NULL,
    SkillId INTEGER NOT NULL,
    WithCity INTEGER NOT NULL,
    Amount INTEGER,
    IsPulled INTEGER NOT NULL DEFAULT 0,
    UNIQUE (PositionId, ExperienceId, SkillId, CountryId, WithCity),
    FOREIGN KEY (PositionId) REFERENCES Position(Id),
    FOREIGN KEY (ExperienceId) REFERENCES Experience(Id),
    FOREIGN KEY (SkillId) REFERENCES Skill(Id),
    FOREIGN KEY (CountryId) REFERENCES Country(Id)
)