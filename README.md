# SkillSprint

SkillSprint is a lightweight browser app for practicing short learning prompts in:

- Python
- Linear Algebra
- Probability
- Software Engineering Basics
- MLOps
- Transformers
- Deployment Basics

It includes:

- Bite-size question + hint + solution format
- Skip option
- XP + streak gamification
- Topic mastery tracking
- Adaptive question selection (weaker topics are prioritized)
- Local progress persistence via `localStorage`

## Run

No build step required.

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Notes

- To reset progress, use the **Reset Progress** button in the UI.
- All data stays in your browser.
