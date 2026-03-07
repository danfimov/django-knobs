from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from knobs.cache import _cache
from knobs.registry import _registry

knob_pre_change = Signal()  # kwargs: name, old_value, new_value
knob_post_change = Signal()  # kwargs: name, old_value, new_value


@receiver(post_save, sender="knobs.KnobValue")
def _on_knob_value_saved(sender, instance, **kwargs) -> None:
    name = instance.name
    if name not in _registry:
        return

    knob = _registry[name]
    new_value = knob.coerce(instance.raw_value)
    old_value = _cache.get(name, knob.default)

    knob_post_change.send(
        sender=sender,
        name=name,
        old_value=old_value,
        new_value=new_value,
    )
    _cache.set(name, new_value)
