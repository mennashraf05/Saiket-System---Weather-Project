import sys
import os
# أضف جذر المشروع لمكان البحث عن الحزمة
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from types import SimpleNamespace
import weather_open_meteo as w

class DummyResponse:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data

def test_get_coordinates_success(monkeypatch):
    sample = {"results":[{"latitude":10.5,"longitude":-20.2,"name":"TestCity","country":"TC"}]}
    monkeypatch.setattr(w, 'requests', SimpleNamespace(get=lambda *a,**k: DummyResponse(sample)))
    lat, lon, name, country = w.get_coordinates("TestCity", language="en")
    assert lat == 10.5
    assert lon == -20.2
    assert name == "TestCity"
    assert country == "TC"

def test_get_coordinates_no_results(monkeypatch):
    sample = {"results":[]}
    monkeypatch.setattr(w, 'requests', SimpleNamespace(get=lambda *a,**k: DummyResponse(sample)))
    with pytest.raises(ValueError):
        w.get_coordinates("UnknownCity")

def test_get_current_weather_success(monkeypatch):
    sample = {"current_weather":{"temperature":25,"windspeed":5,"weathercode":1}}
    monkeypatch.setattr(w, 'requests', SimpleNamespace(get=lambda *a,**k: DummyResponse(sample)))
    data = w.get_current_weather(0.0, 0.0, temp_unit="celsius")
    assert data["temperature"] == 25
    assert data["windspeed"] == 5
    assert data["weathercode"] == 1

def test_get_current_weather_no_data(monkeypatch):
    sample = {}
    monkeypatch.setattr(w, 'requests', SimpleNamespace(get=lambda *a,**k: DummyResponse(sample)))
    with pytest.raises(ValueError):
        w.get_current_weather(0.0, 0.0)

def test_get_weekly_forecast_success(monkeypatch):
    sample = {"daily":{"time":["2025-01-01"],"temperature_2m_max":[30],"temperature_2m_min":[20],"weathercode":[0]}}
    monkeypatch.setattr(w, 'requests', SimpleNamespace(get=lambda *a,**k: DummyResponse(sample)))
    data = w.get_weekly_forecast(0.0, 0.0, temp_unit="celsius")
    assert data["time"][0] == "2025-01-01"
    assert data["temperature_2m_max"][0] == 30

def test_display_current_weather_prints(capsys):
    weather = {"temperature":22,"windspeed":3,"weathercode":0}
    w.display_current_weather("SampleCity","SC",weather,temp_unit="celsius")
    captured = capsys.readouterr()
    assert "Current weather in SampleCity, SC:" in captured.out
    assert "Temperature: 22" in captured.out

def test_display_weekly_forecast_prints(capsys):
    daily = {"time":["2025-02-02"],"temperature_2m_max":[28],"temperature_2m_min":[18],"weathercode":[2]}
    w.display_weekly_forecast("SampleCity","SC",daily,temp_unit="celsius")
    captured = capsys.readouterr()
    assert "7-day forecast for SampleCity, SC:" in captured.out
    assert "2025-02-02 | Max: 28" in captured.out
