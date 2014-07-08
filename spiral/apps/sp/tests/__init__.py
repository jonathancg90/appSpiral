"""
Importar test para la ejcucion mediante el comando ./manage.py test sp
"""

from apps.sp.tests.model_has_commercial.CommercialView import CommercialViewTest
from apps.sp.tests.model_has_commercial.EntryView import EntryViewTest
from apps.sp.tests.model_has_commercial.BrandView import BrandViewTest
from apps.sp.tests.search.logic import SearchLogicTest
from apps.sp.tests.model.create_model import ModelCreateTest
from apps.sp.tests.admin.users import UsersTest
from apps.sp.tests.tasks.facebook import FacebookTaskTest
from apps.sp.tests.website.home import HomeTest