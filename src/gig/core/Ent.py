from gig.core.EntBase import EntBase
from gig.core.EntGIGMixin import EntGIGMixin
from gig.core.EntJSONMixin import EntJSONMixin
from gig.core.EntLoadMixin import EntLoadMixin


class Ent(EntBase, EntJSONMixin, EntLoadMixin, EntGIGMixin):
    pass
