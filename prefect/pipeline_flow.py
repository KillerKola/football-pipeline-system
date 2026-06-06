from prefect import flow, task
import subprocess

@task(retries=2, retry_delay_seconds=30)
def run_pipeline():
    result = subprocess.run(
        "python main.py fetch load",
        shell=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError("Pipeline failed")

@flow(name="daily-football-pipeline")
def daily_football_pipeline():
    run_pipeline()

if __name__ == "__main__":
    daily_football_pipeline.serve(
        name="daily-football-refresh",
        cron="0 3 * * *"
    )