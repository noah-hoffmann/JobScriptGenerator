from pytest import fixture
from jobscriptgenerator.job import Job


@fixture
def job() -> Job:
    return Job(
        # attributes common for pbs and slurm
        account="user",
        partition="short",
        job_name="test",
        walltime="12:00:00",
        ntasks_per_nodes=10,
        mem="16G",
        nodes=5,
        mail_user="user@foo.com",
        # some slurm exclusives
        cpus_per_task=20,
        # some pbs exclusives
        node_type="rome",
        ompthreads=20,
    )


def test_to_slurm(job: Job):
    reference = """#!/bin/bash
#SBATCH --account=user
#SBATCH --cpus-per-task=20
#SBATCH --job-name=test
#SBATCH --mail-user=user@foo.com
#SBATCH --nodes=5
#SBATCH --partition=short
#SBATCH --time=12:00:00
#SBATCH --mem=16G"""
    assert job.to_slurm() == reference


def test_to_pbs(job: Job):
    reference = """#!/bin/bash
#PBS -A user
#PBS -M user@foo.com
#PBS -N test
#PBS -q short
#PBS -l walltime=12:00:00
#PBS -l select=5:mem=16G:ompthreads=20:node_type=rome"""
    assert job.to_pbs() == reference
