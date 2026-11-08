# AGENTS.md — Business Analytics project: my-analysis

Starter rules (from the course project brief):

1. Never modify anything in `data/raw/`.
2. After every filter, merge or drop, print the number of rows and the reason.
3. Every number in a write-up comes from a file in `results/`; name the script that made it.
4. Follow `plan.md`. Ask before changing anything in it, and list every analysis choice you make.
5. Fix random seeds, and log the prompt, output and model name of every model call in folder `calls/`. Its structure should be
calls/
├── call_001_initial_exploration/
│   ├── prompt.md
│   ├── model.md
│   └── output.md
│
├── call_002_data_preparation/
│   ├── prompt.md
│   ├── model.md
│   └── output.md
│
├── call_003_descriptive_analysis/
│   ├── prompt.md
│   ├── model.md
│   └── output.md
6. No causal claims unless the design supports them. Say "I am not sure" when you are not.
