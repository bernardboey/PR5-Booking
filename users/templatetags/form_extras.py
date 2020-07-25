from django import template

register = template.Library()


@register.filter
def add_class(field, class_name):
    classes = field.field.widget.attrs.get("class", "")
    if field.errors:
        class_name += " is-invalid"
    return field.as_widget(attrs={
        "class": " ".join(classes.split() + class_name.split())
    })


@register.simple_tag
def styled_field(field, error_class=None, **kwargs):
    if field.errors and error_class:
        if "class" in kwargs:
            kwargs["class"] += " " + error_class
        else:
            kwargs["class"] = error_class
    return field.as_widget(attrs={
        attr_name: " ".join(field.field.widget.attrs.get(attr_name, "").split() + attr_values.split())
        for attr_name, attr_values in kwargs.items()
    })


@register.simple_tag
def styled_checkbox(field, error_class=None):
    if field.errors:
        classes = field.field.widget.attrs.get("class", "")
        classes = " ".join(classes.split() + error_class.split())
        field.field.widget.attrs["class"] = classes
    return ""
