
# Get Splunk License Info

A CLI Script to show pretty-printed Splunk License Data.

This servers as a wrapper for `splunk list licenses`, but adds a few enchancements:

- Bytes are converted into MB and GB
- Dates are converted into human-readable formats
- Color coding is used so expired licenses show up in RED
- Any license that expires in less than 30 days will show up in YELLOW


## Requirements

- Python
- A running version of Splunk 6.x or greater
- Admin access to Splunk


## Usage

- Run the script: `./get-splunk-licenses.py`
- Enter your admin username and password if prompted


## Sample Output

<img src="./img/splunk-license-info.png" />


## Comments or Feedback

Feel free to email them to me (Douglas_Muth@comcast.com) or open a bug here.

Enjoy!


