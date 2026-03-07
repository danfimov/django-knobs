from simple_history import register

from knobs.models import KnobValue

register(KnobValue, app="knobs.contrib.history")
