import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

current_data = pd.read_csv("monitoring/predictions.csv")

reference_data = current_data.copy()

report = Report(metrics=[
    DataDriftPreset()
])

report.run(
    reference_data=reference_data,
    current_data=current_data
)

report.save_html("monitoring/drift_report.html")

print("Drift report generated!")