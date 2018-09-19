# Prefix Analytics Sandbox

A Python-based model for predicting resolution codes of service incidents for the Optima CT660 machine.

## Architecture

![Imgur](https://i.imgur.com/Xwhw10K.png)

## Folder Structure
1. Resolution code prediction model is created on `model.ipynb`
2. Resolution code analysis is done on `resolution analytics.ipynb`
3. `/analytics` folder consist of model deployed to Predix Analytics Framework

## Building, deploying and running the analytic
1. Zip the contents of this directory
2. Create an analytic in Analytics Catalog with a name and version.
3. Upload the zip file and attach it to the created analytic.
4. Deploy and test the analytic on Predix Analytics platform.

## Input format
The expected JSON input data format is as follows:
```json
{
	"data": {
		"sr_id": "123456",
		"error_codes": [],
		"symptom": "Site power outage yesterday. UPS in bypass mode and battery breaker will not stay on."
	}
	
}
```

## Output format
The JSON output format from the analytic is as follows:
```json
{
  "predictions": [
  {
  	"label": "No structural problem found",
	"proba": 0.12126818536281116,
  },
  {
  	"label": "Clean_or_adjust_mylar_scan_window",
	"proba": 0.08320182650371911,
  },
  {
  	"label": "Configure_ConnectPro",
	"proba": 0.049685156406835136,
  }
  ]
}
```
