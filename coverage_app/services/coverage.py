from typing import Dict, Any, List

import numpy as np
import pandas as pd

from coverage_app.services.geocoding import reverse_geocode_city


def get_nearest_results(
    user_location: Dict[str, Any], coverage_data_csv: pd.DataFrame
) -> pd.DataFrame:
    # Convert longitude and latitude columns to numpy arrays
    coverage_longitudes = coverage_data_csv["Longitude"].to_numpy()
    coverage_latitudes = coverage_data_csv["Latitude"].to_numpy()

    # Compute Euclidean distances
    distances = np.sqrt(
        (coverage_longitudes - user_location["longitude"]) ** 2
        + (coverage_latitudes - user_location["latitude"]) ** 2
    )

    coverage_data_csv = coverage_data_csv.copy()
    coverage_data_csv["Distance"] = distances

    # why are getting only 40 nearest results? to not pass 3rd party API limits and because for the problem description
    # I considered it should be enough. Possible edge cases are not considered here.
    nearest_results = coverage_data_csv.nsmallest(40, "Distance")

    return nearest_results


def get_results_in_the_same_city(
    nearest_10_results: pd.DataFrame, user_city: str
) -> List[Dict[str, Any]]:
    results_in_same_city = []

    for _, row in nearest_10_results.iterrows():
        longitude = row["Longitude"]
        latitude = row["Latitude"]
        city = reverse_geocode_city(longitude, latitude)
        if city == user_city:
            results_in_same_city.append(row.to_dict())

    return results_in_same_city


def aggregate_coverage_by_provider(
    coverage_points: List[Dict[str, Any]]
) -> Dict[str, Dict[str, bool]]:
    provider_coverage = {}
    for point in coverage_points:
        provider_name = point["ProviderName"]
        coverage_info = {
            "2G": bool(point["2G"]),
            "3G": bool(point["3G"]),
            "4G": bool(point["4G"]),
        }
        # ( point of discussion ) what if we have 2G in one point and 3G in another point but in the same city?
        # I have considered that it since we are checking "city coverage" might make sense,
        # but only given the task description probably this would not be a real use case like this
        if provider_name in provider_coverage:
            for key in ["2G", "3G", "4G"]:
                provider_coverage[provider_name][key] = (
                    provider_coverage[provider_name][key] or coverage_info[key]
                )
        else:
            provider_coverage[provider_name] = coverage_info
    return provider_coverage
