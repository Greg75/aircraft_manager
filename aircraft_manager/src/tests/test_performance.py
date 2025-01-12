# Third party imports
import pytest
import asyncio

# Internal imports
from API.schemas import InputAircraftPerformanceRangeSchema, OutputAircraftPerformanceRangeSchema, \
    InputAircraftPerformanceEnduranceSchema, OutputAircraftPerformanceEnduranceSchema
from API.use_cases.performance import Performance
from API.tests.conftest import load_data, db_session


class TestPerformance:

    @pytest.fixture
    def mock_input_aircraft_performance_range_schema(self, mocker):
        return mocker.patch('API.schemas.InputAircraftPerformanceRangeSchema',
                            InputAircraftPerformanceRangeSchema(aircraft_id=100, wind_speed=10.0, fuel=60.0))

    @pytest.fixture
    def mock_output_aircraft_performance_range_schema(self, mocker):
        return mocker.patch('API.schemas.OutputAircraftPerformanceRangeSchema',
                            OutputAircraftPerformanceRangeSchema(name='C-152', range=800.0))

    @pytest.fixture
    def mock_input_aircraft_performance_endurance_schema(self, mocker):
        return mocker.patch('API.schemas.InputAircraftPerformanceEnduranceSchema',
                            InputAircraftPerformanceEnduranceSchema(aircraft_id=100, fuel=60.0))

    @pytest.fixture
    def mock_output_aircraft_performance_endurance_schema(self, mocker):
        return mocker.patch('API.schemas.OutputAircraftPerformanceEnduranceSchema',
                            OutputAircraftPerformanceEnduranceSchema(name='C-152', endurance='04:00'))

    def test_calculate_range(self, mock_input_aircraft_performance_range_schema,
                             mock_output_aircraft_performance_range_schema, load_data, db_session):

        output = Performance(db_session).calculate_range(
            input_data=mock_input_aircraft_performance_range_schema)

        expected_output = mock_output_aircraft_performance_range_schema

        assert output == expected_output
        assert output.name == 'C-152'
        assert output.range == 800.0

    def test_calculate_endurance(self, mock_input_aircraft_performance_endurance_schema,
                                 mock_output_aircraft_performance_endurance_schema, load_data, db_session):

        output = Performance(db_session).calculate_endurance(
            input_data=mock_input_aircraft_performance_endurance_schema)

        expected_output = mock_output_aircraft_performance_endurance_schema

        assert output == expected_output
        assert output.name == 'C-152'
        assert output.endurance == '04:00'
