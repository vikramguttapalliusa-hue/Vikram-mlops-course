# Week 02 Lab

Instrument a provided training script (`train.py`) with MLflow experiment tracking; log params, metrics, and artifacts across a few runs, then compare them in the MLflow UI.

Starter files for this week's lab are pulled into your repo via `git fetch upstream && git merge upstream/main`, as introduced in the Week 1 lab.
 Best Run: Run 3 (n_estimators=200, max_depth=None) performed best, achieving 97-98% accuracy compared to the baseline's 83% (an improvement of around 14-15%).
 Why it won: Increasing n_estimators provides better ensemble variance reduction, while setting max_depth=None lets individual decision trees grow fully to learn the non-linear pixel patterns of handwritten digits.
 Leg of Reproducibility: It covers Config (hyperparameters and tracked run metadata/metrics).
