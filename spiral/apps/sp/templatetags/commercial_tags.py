from django import template

from apps.sp.models.Project import Project
from apps.sp.models.Casting import CastingDetailParticipate
from apps.sp.models.Extras import ExtraDetailParticipate
from apps.sp.models.PhotoCasting import PhotoCastingDetailParticipate
from apps.sp.models.Representation import RepresentationDetailModel

register = template.Library()


def project_model_participate(commercial, model):
    try:
        project = Project.objects.get(commercial=commercial)
        if project.line_productions == Project.LINE_CASTING:
            casting_detail_participate = CastingDetailParticipate.objects.get(model=model)
            return casting_detail_participate.detail_model.get_character_display()
        if project.line_productions == Project.LINE_PHOTO:
            photo_casting_detail_participate = PhotoCastingDetailParticipate.objects.get(model=model)
            return photo_casting_detail_participate.detail_model.get_character_display()
        if project.line_productions == Project.LINE_EXTRA:
            extra_detail_participate = ExtraDetailParticipate.objects.get(model=model)
            return extra_detail_participate.detail_model.get_character_display()
        if project.line_productions == Project.LINE_REPRESENTATION:
            representation_detail_model = RepresentationDetailModel.objects.get(model=model)
            return representation_detail_model.get_character_display()
    except Exception, e:
        return None

register.filter(project_model_participate)