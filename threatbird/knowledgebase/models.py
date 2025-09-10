from django.db import models
from django.utils import timezone
import uuid


# Create your models here.

class Technique(models.Model):
    """ A MITRE Technique. Techniques represent 'how' an adversary achieves a tactical goal by performing an action. For example, an adversary may dump credentials to achieve credential access. """

    id = models.CharField(
        max_length=120,
        unique=True,
        primary_key=True,
        blank=False,
        null=False,
        help_text="MITRE ID of the technique (ie. 'attack-pattern-xxxxx').",
    )
    created_at = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    modified = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    inserted = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    name = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        help_text="A name for the technique.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the technique.",
    )

    data_sources = models.TextField(
        blank=True,
        null=True,
        help_text="Technique data sources.",    # 'x_mitre_data_sources' comma separated
    )
    kill_chain_phases = models.TextField(
        blank=True,
        null=True,
        help_text="Technique platforms.",       # comma separated [p['phase_name'] for p in kill_chain_phases]
    )
    url = models.TextField(
        blank=True,
        null=True,
        help_text="Technique URL, comma separated.",    # f['url'] if f['source_name'] == "mitre-attack" for f in external_references else ""
    )
    detection = models.TextField(
        blank=True,
        null=True,
        help_text="Technique detection information.",   # x_mitre_detection
    )
    permissions_required = models.TextField(
        blank=True,
        null=True,
        help_text="Permissions required for this technique, comma separated.",   # comma separated: x_mitre_permissions_required if x_mitre_permissions_required else ""
    )
    platforms = models.TextField(
        blank=True,
        null=True,
        help_text="Technique platforms, comma separated.",   # x_mitre_patforms
    )
    subtechniques = models.ManyToManyField(
        "self",
        blank=True,
        help_text="Selection of techniques connected to this tactic.",
    )

    @property
    def has_subtechnique(self):
        return True if len(self.subtechniques) else False

    class Meta:
        verbose_name = "Technique"
        verbose_name_plural = "Techniques"

    def __str__(self):
        return f"Technique {self.name}"



class Tactic(models.Model):
    """ A MITRE Tactic. Tactics represent the "why" of an ATT&CK technique or sub-technique. It is the adversary's tactical goal: the reason for performing an action. For example, an adversary may want to achieve credential access. """

    id = models.CharField(
        max_length=120,
        unique=True,
        primary_key=True,
        blank=False,
        null=False,
        help_text="MITRE ID of the tactic (ie. 'x-mitre-tactic--xxxxxxx').",
    )
    created_at = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    modified = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    inserted = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    name = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        help_text="A name for the tactic.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the tactic.",
    )
    url = models.TextField(
        blank=True,
        null=True,
        help_text="Tactic URL, comma separated.",    # [f"{x['external_id']}|{x['url']}" for x in external_references]
    )
    techniques = models.ManyToManyField(
        Technique,
        related_name="tactictechnique",
        blank=True,
        help_text="Selection of techniques connected to this tactic.",
    )
    
    class Meta:
        verbose_name = "Tactic"
        verbose_name_plural = "Tactics"

    def __str__(self):
        return f"Tactic {self.name}"


class Group(models.Model):
    """ A MITRE APT Groupo. Groups are activity clusters that are tracked by a common name in the security community and terms such as threat groups, activity groups, and threat actors are being used. """

    id = models.CharField(
        max_length=120,
        unique=True,
        primary_key=True,
        blank=False,
        null=False,
        help_text="MITRE ID of the group (ie. 'intrusion-set-xxx').",
    )
    created_at = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    modified = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    inserted = models.DateTimeField(
        default=timezone.now,                   # 'auto_now_add' is not editable
    )
    name = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        help_text="A name for the game.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Description of the group.",
    )
    aliases = models.TextField(
        blank=True,
        null=True,
        help_text="Group aliases, comma separated.",
    )
    techniques = models.ManyToManyField(
        Technique,
        related_name="grouptechnique",
        blank=True,
        help_text="Selection of techniques used by this group.",
    )

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return f"Group {self.name}"


# class Update(models.Model):
#     """ A model for handling content/infra updates. """

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False,
#         unique=True,
#     )
#     created_at = models.DateTimeField(
#         default=timezone.now,           # 'auto_now_add' is not editable
#     )
#     updatetype = 
#     message = models.TextField(
#         blank=True,
#         null=True,
#         help_text="Update content.",
#     )

#     class Meta:
#         verbose_name = "DataUpdate"
#         verbose_name_plural = "DataUpdates"

#     def __str__(self):
#         return f"DataUpdate {self.created_at}"

