"""Module to compute some jobs from the server.

API
---
.. compute_jobs:: compute_jobs

"""

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from subprocess import DEVNULL, check_call
from typing import Any, Dict

import yaml

from ..client import query_server
from ..client.mutations import create_job_status_mutation
from ..client.queries import create_jobs_query
from ..job_schedulers import create_pbs_script, create_slurm_script
from ..utils import Options

logger = logging.getLogger(__name__)


def compute_jobs(opts: Options) -> None:
    """Compute some jobs using the configuration."""
    query = create_jobs_query(opts.job_status, opts.collection_name, opts.max_jobs)
    jobs = query_server(opts.url, query)["jobs"]
    logger.info(f"Job scheduler: {opts.scheduler}")
    for j in jobs:
        succeeded = schedule_job(opts, j)
        print(succeeded)
        # if not succeeded:
        #     logger.warn(f"Job {jobs['id']} fails to be scheduled!")
        #     update_job_status(opts, j, "FAILED")
        # else:
        #     update_job_status(opts, j, "RUNNING")


def schedule_job(opts: Options, job: Dict[str, Any]) -> bool:
    """Schedule a job to run locally or using job scheduler."""
    job_id = job['_id']
    # Folder where the job data is going to be stored
    job_workdir = Path(opts.workdir) / f"job_{job_id}"
    if not job_workdir.exists():
        os.makedirs(job_workdir, exist_ok=True)

    # input used by the workflow runner
    input_file = write_input_file(job, job_workdir)

    # Generate the script to submit the job using the
    # user provide scheduler
    scheduler = opts.scheduler.name
    script_generator = {"slurm": create_slurm_script, "pbs": create_pbs_script}

    # Command to run the workflow
    if scheduler == "none":
        # Run locally
        cmd = f"{opts.command} {input_file.absolute().as_posix()} &"
    else:
        # Schedule the job
        cmd = script_generator[scheduler](opts, job, input_file)
    try:
        print("cmd: ", cmd)
        # run_command(cmd, job_workdir)
        return True
    except:
        msg = f"Job {job_id} failed with error:\n{sys.exc_info()[0]}"
        logger.warning(msg)
        return False


def write_input_file(job: Dict[str, Any], job_workdir: Path) -> Path:
    """Write input to run the workflow in YAML format."""
    input_file = job_workdir / f"input_file_job_{job['_id']}.yml"

    with open(input_file, 'w') as handler:
        settings = json.loads(job['settings'])
        yaml.dump(settings, handler, indent=4)

    return input_file.absolute()


def run_command(cmd: str, workdir: str) -> bool:
    """Run ``cmd`` as subprocess."""
    result = check_call(cmd, shell=True, stdout=DEVNULL, cwd=workdir)
    return result == 0


def update_job_status(opts: Options, job: Dict[str, Any], status: str) -> None:
    """Update status of `job`."""
    now = datetime.timestamp()
    completion = now if status == "FAILED" else None

    # Change job metadata
    info = {
        "job_id": job["_id"],
        "status": status,
        "schedule_time": now,
        "completion_time": completion
    }

    query = create_job_status_mutation(info)
    query_server(opts.url, query)
