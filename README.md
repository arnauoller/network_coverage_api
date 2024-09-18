# Cell Coverage Data API

This project provides an API for querying cell coverage data based on a user's location. The coverage data includes availability of 2G, 3G, and 4G networks from various providers.
At the moment of writing, the API only supports French addresses and French providers.

## Features
- Retrieves coverage information by querying with a user-provided address.
- Aggregates results by provider, showing available network coverages (2G, 3G, 4G) for each provider.
- Utilizes third-party geocoding APIs to convert user addresses into geographical coordinates.
- Computes distances from the user location to the nearest coverage points.

### Installation

1. Install the dependencies using `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

2. (Optional) Preprocess the coverage data to convert Lambert93 coordinates to GPS (it already exists, but it can be re-generated):
    ```bash
    python ./coverage_app/services/preprocess_coverage_data.py
    ```
   This script will generate a CSV file containing both Lambert93 and GPS coordinates, which is used by the API for coverage lookups.

### Running the API

To run the API locally, execute the following command:
```bash
python manage.py runserver
```

### Example Query

You can query the API using a URL like the following:

```plaintext
http://127.0.0.1:8000/api/coverage/?q=42+rue+papernest+75011+Paris
```
And you will have a response similar to this:
```GET /api/coverage/?q=42+rue+papernest+75011+Paris
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "Orange": {
        "2G": true,
        "3G": true,
        "4G": true
    },
    "SFR": {
        "2G": true,
        "3G": true,
        "4G": true
    },
    "Bouygues Telecom": {
        "2G": true,
        "3G": true,
        "4G": true
    },
    "Free": {
        "2G": false,
        "3G": true,
        "4G": true
    }
}
```


Alternatively, you can input the address in a more human-readable format:

```plaintext
http://127.0.0.1:8000/api/coverage/?q=Rue des Garosses 33310 Lormont, France
```