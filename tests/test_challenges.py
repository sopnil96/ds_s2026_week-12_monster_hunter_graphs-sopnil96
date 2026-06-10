"""Public tests for Week 12: Monster Hunter Graphs.

Run with:
    pytest -q
"""

import pytest

from src.challenges import (
    build_hunter_map,
    build_weighted_hunter_map,
    map_summary,
    most_connected_location,
    priority_hunt_order,
)


def normalize_graph(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    """Sort neighbor lists so tests do not depend on list order."""
    return {location: sorted(neighbors) for location, neighbors in graph.items()}


def test_build_hunter_map_adds_both_directions():
    edges = [
        ("Old Theater", "Train Station"),
        ("Train Station", "Library Basement"),
    ]

    graph = normalize_graph(build_hunter_map(edges))

    assert graph == {
        "Old Theater": ["Train Station"],
        "Train Station": ["Library Basement", "Old Theater"],
        "Library Basement": ["Train Station"],
    }


def test_build_hunter_map_avoids_duplicate_neighbors():
    edges = [
        ("Old Theater", "Train Station"),
        ("Old Theater", "Train Station"),
        ("Train Station", "Old Theater"),
    ]

    graph = normalize_graph(build_hunter_map(edges))

    assert graph == {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater"],
    }


def test_build_hunter_map_empty_edges_returns_empty_graph():
    assert build_hunter_map([]) == {}


def test_build_weighted_hunter_map_adds_both_directions():
    edges = [
        ("Old Theater", "Train Station", 4),
        ("Train Station", "Library Basement", 7),
    ]

    graph = build_weighted_hunter_map(edges)

    assert graph["Old Theater"]["Train Station"] == 4
    assert graph["Train Station"]["Old Theater"] == 4
    assert graph["Train Station"]["Library Basement"] == 7
    assert graph["Library Basement"]["Train Station"] == 7


def test_build_weighted_hunter_map_keeps_lowest_duplicate_weight():
    edges = [
        ("Old Theater", "Train Station", 8),
        ("Old Theater", "Train Station", 4),
        ("Train Station", "Old Theater", 6),
    ]

    graph = build_weighted_hunter_map(edges)

    assert graph["Old Theater"]["Train Station"] == 4
    assert graph["Train Station"]["Old Theater"] == 4


def test_build_weighted_hunter_map_rejects_non_positive_weights_zero():
    edges = [("Old Theater", "Train Station", 0)]
    with pytest.raises(ValueError):
        build_weighted_hunter_map(edges)

def test_build_weighted_hunter_map_rejects_non_positive_weights_negative_one():
    edges = [("Old Theater", "Train Station", -1)]
    with pytest.raises(ValueError):
        build_weighted_hunter_map(edges)

def test_build_weighted_hunter_map_rejects_non_positive_weights_negative_ten():
    edges = [("Old Theater", "Train Station", -10)]
    with pytest.raises(ValueError):
        build_weighted_hunter_map(edges)

def test_map_summary_counts_locations_and_undirected_routes():
    graph = {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater", "Library Basement", "Abandoned Pier"],
        "Library Basement": ["Train Station"],
        "Abandoned Pier": ["Train Station"],
    }

    assert map_summary(graph) == {"locations": 4, "routes": 3}


def test_map_summary_empty_graph():
    assert map_summary({}) == {"locations": 0, "routes": 0}


def test_most_connected_location_returns_highest_degree_location():
    graph = {
        "Old Theater": ["Train Station"],
        "Train Station": ["Old Theater", "Library Basement", "Abandoned Pier"],
        "Library Basement": ["Train Station"],
        "Abandoned Pier": ["Train Station"],
    }

    assert most_connected_location(graph) == "Train Station"


def test_most_connected_location_tie_returns_alphabetically_first():
    graph = {
        "Crypt": ["Library Basement"],
        "Old Theater": ["Train Station"],
        "Library Basement": ["Crypt"],
        "Train Station": ["Old Theater"],
    }

    assert most_connected_location(graph) == "Crypt"


def test_most_connected_location_empty_graph_returns_none():
    assert most_connected_location({}) is None


def test_priority_hunt_order_returns_locations_by_priority():
    reports = [
        (3, "Old Theater"),
        (1, "Library Basement"),
        (2, "Train Station"),
    ]

    assert priority_hunt_order(reports) == [
        "Library Basement",
        "Train Station",
        "Old Theater",
    ]


def test_priority_hunt_order_empty_reports():
    assert priority_hunt_order([]) == []


def test_priority_hunt_order_handles_ties_alphabetically():
    reports = [
        (2, "Old Theater"),
        (1, "Crypt"),
        (1, "Abandoned Pier"),
    ]

    assert priority_hunt_order(reports) == [
        "Abandoned Pier",
        "Crypt",
        "Old Theater",
    ]
