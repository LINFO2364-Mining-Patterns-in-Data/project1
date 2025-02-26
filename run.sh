#!/bin/bash

LOG_FILE="output.log"

run_command() {
    CMD=$1
    echo "----------------------------------------" | tee -a $LOG_FILE
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Running: $CMD" | tee -a $LOG_FILE
    echo "----------------------------------------" | tee -a $LOG_FILE
    $CMD >> $LOG_FILE 2>&1
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Finished: $CMD" | tee -a $LOG_FILE
    echo "" | tee -a $LOG_FILE
}

run_command "python run_experiment.py retail" 5
run_command "python run_experiment.py pumsb" 5
run_command "python run_experiment.py mushroom" 5

echo "All experiments completed. Check $LOG_FILE for details."
