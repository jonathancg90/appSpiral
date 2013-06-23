from django.test.testcases import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.contenttypes.models import ContentType
 
class CommercialViewTest(TestCase):
 
    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = Client()
 
    def _insert_data(self):
        self.language = Language()
        self.language.save()
 
 
    def _insert_buyer(self):
        self.buyer = Buyer()
        self.buyer.save()
 
        self.user_buyer = User(
            email='buyer@gmail.com',
            username='buyer'
        )
        self.user_buyer.save()
 
        self.user_buyer.add_related_entity(self.buyer)
        self.user_buyer.current_role = getattr(User, 'ROLE_BUYER')
        self.content_type_buyer = ContentType.objects.get(model='buyer')
        self.content_type_buyer.model = 'BUYER'
        self.content_type_buyer.save()
 
    def _insert_manufacturer(self):
        self.manufacturer = Manufacturer()
        self.manufacturer.save()
 
        self.user_manufacturer = User(
            email='manufacturer@gmail.com',
            username='manufacturer'
        )
        self.user_manufacturer.save()
 
        self.user_manufacturer.add_related_entity(self.manufacturer)
        self.user_manufacturer.current_role = getattr(User, 'ROLE_MANUFACTURER')
        self.content_type_manufacturer = ContentType.objects.get(model='manufacturer')
        self.content_type_manufacturer.model = 'MANUFACTURER'
        self.content_type_manufacturer.save()
 
        manufacturer_fake = Manufacturer()
        manufacturer_fake.save()
 
        user_manufacturer_fake = User(
            email='manufacturer_fake@gmail.com',
            username='manufacturer_fake'
        )
        user_manufacturer_fake.save()
 
        user_manufacturer_fake.add_related_entity(manufacturer_fake)
        user_manufacturer_fake.current_role = getattr(User, 'ROLE_MANUFACTURER')
 
    def test_data_complete(self):
        self._insert_data()
        self._insert_manufacturer()
        self._insert_buyer()
        self.assertTrue(Language.objects.all().count()>0)
        self.assertTrue(Manufacturer.objects.all().count()>0)
        self.assertTrue(User.objects.all().count()>0)
        self.assertTrue(Buyer.objects.all().count()>0)
 
    def test_view_private_link(self):
        self._insert_data()
        self._insert_manufacturer()
        view = ManufacturerPrivateBuyerListView.as_view()
        request = self.request_factory.get(
            reverse('manufacturer_private_buyer_list')
        )
        request.user = self.user_manufacturer
        request.session = {'lang_active': 1}
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(),0)
        self._insert_buyer()
        buyer_private = BuyerPrivate(
            buyer =  self.buyer,
            manufacturer = self.manufacturer
        )
        buyer_private.save()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(),1)
 
    def test_view_pending_invitation(self):
        self._insert_data()
        self._insert_manufacturer()
        view = ManufacturerPendingInvitationListView.as_view()
        request = self.request_factory.get(
            reverse('manufacturer_private_buyer_list')
        )
        request.user = self.user_manufacturer
        request.session = {'lang_active': 1}
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'].count(),0)
        pending_invitation = PendingInvitation(
            content_type=self.content_type_manufacturer,
            object_id=self.manufacturer.id,
            email='buyer_invited@gmail.com',
        )
        pending_invitation.save()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(),1)
        pending_invitation = PendingInvitation(
            content_type=self.content_type_manufacturer,
            object_id=2,
            email='other_invited@gmail.com',
        )
        pending_invitation.save()
        response = view(request)
        self.assertEqual(response.context_data['object_list'].count(),1)
 
    def test_add_pending_buyer(self):
        self._insert_data()
        self._insert_manufacturer()
        self.assertTrue(PendingInvitation.objects.all().count()==0)
        self.assertTrue(BuyerPrivate.objects.all().count()==0)
        data = {
            'email': 'nuevo_buyer@gmail.com'
        }
        view = ManufacturerBuyerCreateView.as_view()
        request = self.request_factory.post(
            reverse('manufacturer_private_buyer_list'),data
        )
        request.user = self.user_manufacturer
        request.session = {'lang_active': 1}
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PendingInvitation.objects.all().count()==1)
        self.assertTrue(BuyerPrivate.objects.all().count()==0)
 
    def test_add_special_buyer(self):
        self._insert_data()
        self._insert_manufacturer()
        self._insert_buyer()
        self.assertTrue(PendingInvitation.objects.all().count()==0)
        self.assertTrue(BuyerPrivate.objects.all().count()==0)
        data = {
            'email': 'buyer@gmail.com'
        }
        view = ManufacturerBuyerCreateView.as_view()
        request = self.request_factory.post(
            reverse('manufacturer_private_buyer_list'),data
        )
        request.user = self.user_manufacturer
        request.session = {'lang_active': 1}
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PendingInvitation.objects.all().count()==0)
        self.assertTrue(BuyerPrivate.objects.all().count()==1)
 
 
    def test_verify_invited(self):
        self._insert_data()
        self._insert_manufacturer()
        self._insert_buyer()
        #Invited buyer
        pending_invitation = PendingInvitation(
            content_type=self.content_type_manufacturer,
            object_id=self.manufacturer.id,
            email='buyer_invited@gmail.com',
        )
        pending_invitation.save()
        self.assertTrue(PendingInvitation.objects.all().count()==1)
        self.assertTrue(BuyerPrivate.objects.all().count()==0)
        #Register new buyer
        buyer_invited = Buyer()
        buyer_invited.save()
 
        user_invited = User(
            email='buyer_invited@gmail.com',
            username='buyer_invited'
        )
        user_invited.save()
 
        user_invited.add_related_entity(buyer_invited)
        user_invited.current_role = getattr(User, 'ROLE_BUYER')
 
        pending_invitation.verify_invited(buyer_invited,'buyer_invited@gmail.com')
 
        self.assertTrue(PendingInvitation.objects.all().count()==0)
        self.assertTrue(BuyerPrivate.objects.all().count()==1)