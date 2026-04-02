# PottyIQ Prototype

This prototype demonstrates the core workflow of PottyIQ:

1. Read pet activity events from a JSON file
2. Apply simple rule-based potty prediction
3. Generate an alert time for the pet owner

## Events supported
- wake
- water
- feed
- walk
- potty

## Rules used
- After wake: potty likely in 15-30 minutes
- After water: potty likely in 30-90 minutes
- After feed: potty likely in 90-180 minutes
- If potty happened recently, suppress alert

## Run

```bash
python predictor.py
```
## Example Output
=== PottyIQ Prototype ===

Prediction result:
- Rule used: feed-rule
- Next potty window: 09:30 AM – 11:00 AM
- Alert owner at: 09:20 AM
