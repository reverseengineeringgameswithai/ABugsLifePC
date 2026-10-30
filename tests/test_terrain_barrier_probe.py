"""Original-instruction differential and landing-seeded movement tests."""
import importlib.util
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("barrier_probe",ROOT/"scripts/terrain-barrier-probe.py")
probe=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


@pytest.fixture(scope="module")
def reference():
    if not probe.p.DEFAULT_BINARY.exists():
        pytest.skip("retail work-copy executable unavailable")
    for key in ("level01","plantter"):
        if not (probe.retail.SOURCE_ROOT/probe.retail.SOURCES[key][0]).exists():
            pytest.skip("retail work-copy terrain unavailable")
    return probe.BarrierProbe("level01",probe.p.load_text(probe.p.DEFAULT_BINARY))


@pytest.mark.parametrize("count", (4,16,17,32,33))
def test_native_collector_matches_decoded_blocks_and_caps_at_sixteen_pairs(reference,count):
    result=reference.collect(0,0,(0,0,0),synthetic=probe.fixed_strip(count))
    assert result["selected"]==[{"synthetic_offset":8+i*12} for i in range(min(count,16))]
    assert result["ordered_admission_matches"]


def test_far_query_rejects_bounds_and_segments(reference):
    result=reference.collect(1_000_000,1_000_000,(0,0,0),synthetic=probe.fixed_strip(17))
    assert result["selected"]==[]


@pytest.mark.parametrize("delta", ((0,0,0),(2048,0,0),(0,0,-16000)))
def test_real_list_order_blocks_and_remainders_match_original(reference,delta):
    for _,strip in reference.strips:
        for index in sorted({0,strip.segment_count//2,strip.segment_count-1}):
            a,b=strip.points[index:index+2]
            result=reference.collect((a.x+b.x)*16,(a.z+b.z)*16,delta)
            assert result["ordered_admission_matches"]


@pytest.mark.parametrize("surface,descriptor,cell", (("flat",110,87884),("barrier",104,62004),("steep",114,106336)))
def test_ground_contact_is_created_by_original_landing(reference,surface,descriptor,cell):
    result=reference.grounded_case(surface,"normal")
    landed=result["landing"]["after"]
    assert result["landing"]["before"]["flags"]==[0,0]
    assert landed["flags"]==[1,1]
    assert landed["contact_descriptor"]==descriptor
    assert landed["contact_cell"]=={"source":"level01","source_record":descriptor,"file_offset":cell}
    assert result["movement"]["execution"]["entry_visits"]["0x004aae30"]>=1
    assert result["movement"]["execution"]["entry_visits"]["0x004a9ba0"]>=1


def test_flat_floor_tangent_and_normal_projection(reference):
    tangent=reference.grounded_case("flat","normal")["movement"]
    assert tangent["after"]["position"]==[-176128,-80096,-342006]
    assert tangent["after"]["flags"]==[1,1]
    assert tangent["returns"]==[{"return_site":"0x004ab80d","eax":1},{"return_site":"0x004ab823","eax":0}]
    normal=reference.grounded_case("flat","normal_impulse")["movement"]
    released=reference.grounded_case("flat","clear_ground_flag")["movement"]
    assert normal["after"]["position"]==normal["before"]["position"]
    assert normal["after"]["velocity"]==[0,0,0]
    assert released["after"]["position"]==[-176384,-82144,-342006]
    assert released["after"]["flags"]==[0,0]
    assert "0x004aae30" not in released["execution"]["entry_visits"]


@pytest.mark.parametrize("surface,expected,unblocked", (
    ("barrier",[110280,-121089,-129357],[110479,-120635,-131756]),
    ("steep",[-7879,-88421,250264],[-7456,-88391,250998]),
))
def test_grounded_obstacle_response_is_removed_by_specific_geometry_control(reference,surface,expected,unblocked):
    positive=reference.grounded_case(surface,"normal")
    negative=reference.grounded_case(surface,"without_obstacle")
    assert positive["landing"]==negative["landing"]
    assert positive["movement"]["after"]["position"]==expected
    assert negative["movement"]["after"]["position"]==unblocked
    hit={"return_site":"0x004ab823","eax":2}
    assert hit in positive["movement"]["returns"]
    assert hit not in negative["movement"]["returns"]
    away=reference.grounded_case(surface,"moving_away")
    assert hit not in away["movement"]["returns"]
    if surface=="barrier":
        assert positive["movement"]["segment_updates"]==[0]
        assert positive["movement"]["after"]["flags"]==[1,1]
    else:
        assert positive["movement"]["triangle_updates"]==[{"source":"level01","source_record":87,"file_offset":1000,"update_site":"0x004a9df3"}]
        assert positive["movement"]["after"]["flags"]==[0,0]


def test_reset_prevents_prior_case_state_from_changing_grounded_result(reference):
    first=reference.grounded_case("barrier","normal")
    reference.collect(0,0,(0,0,0),synthetic=probe.fixed_strip(33))
    reference.grounded_case("steep","normal")
    assert reference.grounded_case("barrier","normal")==first


def test_previous_experiment_artifact_stays_pinned():
    assert probe.digest(ROOT/"reports/terrain/EXP-20260904-002.json")=="87392d332e5550cef104728887dfcae8fc5a776bd9c434283167d996cd47df3c"
    assert probe.digest(ROOT/"scripts/terrain-retail-probe.py")=="52ae78064bea79ec14de8f65e2529aa1b272b147b37e92599e4a9b0f24ec6980"
