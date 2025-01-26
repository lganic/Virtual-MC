import pytest
from virtual_mc.data.fixed_point import convert_from_fixed_point, convert_to_fixed_point

@pytest.mark.parametrize("value", [
    -99.78316807922434,
    -89.77504381789467,
    -89.53731997788543,
    -83.93852761846972,
    -79.83608491238108,
    -78.97915691907912,
    -75.55608591664208,
    -75.01394112869748,
    -71.24616881567042,
    -70.26636736308791,
    -68.03013288041264,
    -67.52792009995166,
    -66.67009098974705,
    -66.48718619295443,
    -64.89191903161407,
    -63.61828758281263,
    -63.44872930064267,
    -63.228988830013066,
    -61.373654377526975,
    -61.29647961950635,
    -58.646108199608605,
    -57.019659318924234,
    -55.857961015146884,
    -52.45072375785147,
    -51.538686978573025,
    -50.86132348094359,
    -47.03861149246491,
    -41.41484569633018,
    -31.750104533769658,
    -24.032711401526655,
    -22.870012724143265,
    -22.211964562661876,
    -22.095844374070467,
    -21.203698163404724,
    -20.49796608951027,
    -18.174607925200263,
    -17.79832604836315,
    -16.834938183480247,
    -16.699908712372988,
    -15.24947460796946,
    -13.242755971581957,
    -12.351877656751938,
    -11.352914641288365,
    -10.162901188426886,
    -9.009916045455356,
    -8.331629986563357,
    -2.3434372850309444,
    -2.0510019303056026,
    -1.5970553599107546,
    0.07428594305957859,
    1.0336272820730983,
    1.4639795800749624,
    2.9526709359306977,
    4.592187806918773,
    5.575009075302972,
    7.883535277289823,
    11.944568282921125,
    13.01910596270855,
    16.4071357188232,
    16.431735422565737,
    19.001096331552205,
    23.25530523992458,
    23.38086253029317,
    24.413626251289685,
    26.83591922257915,
    28.714315455601906,
    35.66812729479631,
    37.10717191583416,
    37.275710483022465,
    38.35481940610373,
    38.917609468483505,
    41.6802354277998,
    44.12119029455263,
    44.307914905557396,
    47.98287461483261,
    49.080631866362324,
    49.277584118023555,
    49.441927970900025,
    51.67089499848106,
    55.5059680401007,
    56.297394429622244,
    59.08917166319472,
    61.97214722678444,
    62.16604073147195,
    67.30308746415614,
    71.18855787815173,
    76.02409727015868,
    76.27140423912527,
    77.25495107815169,
    80.16639411836562,
    80.65882239961988,
    81.35778474024531,
    87.71714191139691,
    97.1730127327709,
    97.30568667567701,
    98.3408933266845,
    98.86188928920313,
    99.05129182796964,
    99.2938566115505,
    99.67469912592455,
])
def test_value_conversion(value):

    allign = 32

    from_value = convert_to_fixed_point(value, allign)

    assert isinstance(from_value, int)

    to_value = convert_from_fixed_point(from_value, allign)

    assert to_value == pytest.approx(value)