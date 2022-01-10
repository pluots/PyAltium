from pyaltium.base import AltiumLibItemMixin


class PcbLibItem(AltiumLibItemMixin):
    def __init__(
        self,
        footprintref: str,
        description: str,
        height: float,
        file_name: str,
    ) -> None:
        super().__init__()
        self.footprintref = footprintref
        self.description = description
        self.height = height
        self.file_name = file_name

    def _run_load(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> dict:
        """Create a parsable dict."""
        return {
            "footprintref": self.footprintref,
            "description": self.description,
            "height": self.height,
        }

    # Need repr, str
