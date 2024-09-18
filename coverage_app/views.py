from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from coverage_app.services.coverage import (
    get_nearest_results,
    get_results_in_the_same_city,
    aggregate_coverage_by_provider,
)
from coverage_app.services.data_loader import load_coverage_data_csv
from coverage_app.services.geocoding import get_user_location

GEOCODING_API_URL = "https://api-adresse.data.gouv.fr/search/"
REVERSE_GEOCODING_API_URL = "https://api-adresse.data.gouv.fr/reverse/"


class CoverageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        address = request.query_params.get("q")
        if not address:
            return self.error_response(
                'Query parameter "q" is required.', status.HTTP_400_BAD_REQUEST
            )
        try:
            user_location = get_user_location(address)

            coverage_data_csv = load_coverage_data_csv()

            nearest_coverage_results = get_nearest_results(
                user_location, coverage_data_csv
            )

            coverage_points_in_users_city = get_results_in_the_same_city(
                nearest_coverage_results, user_location["city"]
            )

            if coverage_points_in_users_city:
                response_data = aggregate_coverage_by_provider(
                    coverage_points_in_users_city
                )
            return Response(response_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return self.error_response(str(e), status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return self.error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    def error_response(self, message: str, status_code: int) -> Response:
        return Response({"error": message}, status=status_code)
