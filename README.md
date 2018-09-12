# Prefix Analytics Sandbox

A Python-based model for predicting resolution codes of service incidents for the Optima CT660 machine.

## Architecture

![Imgur](https://i.imgur.com/01DxkKH.png)

## Building, deploying and running the analytic
1. Zip the contents of this directory
2. Create an analytic in Analytics Catalog with the name "prefix-model" and the version "v1".
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
  "predicted": "Perform_software_reconfig"
}
```
