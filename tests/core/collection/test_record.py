import string

import hypothesis.strategies as st
from hypothesis import given

from papertrail.core.collection.record import ExampleRecord

st_python_var_names = st.text(alphabet=string.ascii_letters + "_", min_size=1, max_size=50)
st_any = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.floats(allow_nan=False),
    st.text(alphabet=string.ascii_letters, min_size=0, max_size=20),
    st.lists(st.integers(), max_size=5),
    st.dictionaries(
        keys=st_python_var_names,
        values=st.integers(),
        max_size=5,
    ),
)
st_module = st.text(alphabet=string.ascii_letters + "_.", min_size=1, max_size=100)
st_src_file = st.text(alphabet=string.ascii_letters + "_./", min_size=1, max_size=100)

st_example_record = st.fixed_dictionaries(
    {
        "fn_name": st_python_var_names,
        "module": st_module,
        "src_file": st_src_file,
        "args": st.lists(st_any, max_size=5).map(tuple),
        "kwargs": st.dictionaries(
            keys=st_python_var_names,
            values=st_any,
            max_size=5,
        ),
        "returned": st_any,
        "expected": st_any,
    }
)


@given(record=st_example_record)
def test_example_record(record):
    assert ExampleRecord(**record).to_dict() == record
