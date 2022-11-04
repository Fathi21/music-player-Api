from rest_framework.test import APIClient

class TestModel1Api(unittest.TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_Model1_list(self):
        response = self.client.get(reverse('Model1-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Model1_detail(self):
        mm_objs = Model1.objects.all()
        if mm_objs:
            response = self.client.get(reverse('Model1-detail', args=[mm_objs[0].id]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)