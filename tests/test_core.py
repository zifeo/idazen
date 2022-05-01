from idazen import core


class TestCore:
    def test_conv(self) -> None:
        assert core.to_cm(core.to_native(140)) == 140
