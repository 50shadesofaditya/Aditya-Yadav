import splunklib.client as client
import splunklib.results as results

def fetch_logs_from_splunk(host, port, username, password, query, earliest="-5m", latest="now"):
    svc = client.connect(host=host, port=port, username=username, password=password, scheme="https")
    job = svc.jobs.create(f"{query} earliest={earliest} latest={latest}")
    while not job.is_done():
        pass
    reader = results.ResultsReader(job.results())
    return [r for r in reader if isinstance(r, dict)]
