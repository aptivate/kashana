from django.db import models


class Settings(models.Model):
    class Meta:
        verbose_name_plural = "Settings"

    max_result_level = models.PositiveSmallIntegerField(
        default=4,
        verbose_name="Result depth",
        help_text="Defines the depth of the result tree on MIS dashboard."
    )
    open_result_level = models.PositiveSmallIntegerField(
        default=2,
        verbose_name="Expanded level",
        help_text=(
            "Depth to which result elements are automatically expanded "
            "on MIS dashboard."
        )
    )

    def __str__(self):
        return "Settings"
